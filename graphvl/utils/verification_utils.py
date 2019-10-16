#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import cv2

from mocr import face_detection
from mocr import TextRecognizer

from graphvl import crud
from graphvl.db.session import db_session
from graphvl.models.image import ImageCreate, ImageType


east_path = os.getcwd() + '/graphvl' + '/' + 'text_detection_model/frozen_east_text_detection.pb'

def create_image_file(user_id, image_type):
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


def get_texts(user_id):
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
