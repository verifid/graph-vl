#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import cv2
import datetime

from mocr import face_detection
from mocr import TextRecognizer
from nerd import ner

from graphvl import crud
from graphvl.db.session import db_session
from graphvl.models.image import ImageCreate, ImageType
from graphvl.db_models.models import User

from re import search
from typing import List


east_path = os.getcwd() + '/graphvl' + '/' + 'text_detection_model/frozen_east_text_detection.pb'

def create_image_file(user_id: str, image_type: ImageType):
    image = crud.image.get(db_session, user_id=user_id, image_type=image_type)
    if image:
        photo_data = base64.b64decode(image.image_str)

        if image_type == ImageType.identity:
            path = 'identity/'
        else:
            path = 'profile/'

        directory = os.getcwd() + '/testsets/' + path +  user_id + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + 'image' + '.jpg'
        with open(file_path, 'wb') as f:
            f.write(photo_data)

        # detect face from identity image
        face_image_path = None
        if image_type == ImageType.identity:
            face_image = face_detection.detect_face(file_path)
            face_directory = os.getcwd() + '/testsets/' + 'face/' + user_id + '/'
            if not os.path.exists(face_directory):
                os.makedirs(face_directory)
            face_image_path = face_directory + 'image.jpg'
            cv2.imwrite(face_image_path, face_image)
    return (file_path, face_image_path)


def get_texts(user_id: str):
    image_path = os.getcwd() + '/testsets/' + 'identity' + '/' + user_id + '/' + 'image.jpg'
    text_recognizer = TextRecognizer(image_path, east_path)
    (image, _, _) = text_recognizer.load_image()
    (resized_image, ratio_height, ratio_width, _, _) = text_recognizer.resize_image(image, 320, 320)
    (scores, geometry) = text_recognizer.geometry_score(east_path, resized_image)
    boxes = text_recognizer.boxes(scores, geometry)
    results = text_recognizer.get_results(boxes, image, ratio_height, ratio_width)
    if results:
        texts = ''
        for text_bounding_box in results:
            text = text_bounding_box[1]
            texts += text + ' '
        return texts
    return ''


def create_user_text_label(user: User):
    user_text_label = {'PERSON': [user.name, user.surname],
                       'DATE': user.date_of_birth,
                       'GPE': user.country}
    return user_text_label


def get_doc(texts: str, language: str):
    doc = ner.name(texts, language=language)
    text_label = [(X.text, X.label_) for X in doc]
    return text_label


def point_on_texts(text: str, value: str):
    if isinstance(value, datetime.date):
        value = value.strftime('%d/%m/%Y')

    val_len = len(value)
    text_len = len(text)
    if text_len > val_len:
        match = search(value, text)
    else:
        match = search(text, value)
    point = 0
    if match:
        (start, end) = match.span()
        point = int(((100 * (end - start)) / val_len) / 4)
    return point


def validate_text_label(text_label, user_text_label):
    result = 0
    for (text, label) in text_label:
        if label in user_text_label:
            value = user_text_label[label]
            # check for name and surname
            if isinstance(value, list):
                for val in value:
                    result += point_on_texts(text, val)
            else:
                result += point_on_texts(text, value)
    return result
