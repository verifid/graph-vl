#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import graphene
import base64
import datetime

from collections import OrderedDict
from graphene.test import Client

from graphvl import crud
from graphvl.models.user import UserCreate
from graphvl.schema import UserQuery, UserMutation
from graphvl.schema import ImageQuery, ImageMutation
from graphvl.models.image import ImageCreate, ImageType
from graphvl.utils import verification_utils, utils
from graphvl.db.session import db_session


class VerificationUtilsTest(unittest.TestCase):

    def db_create_rows(self):
        user_id = utils.create_user_id()
        user = UserCreate(user_id=user_id,
                        name='name',
                        surname='surname',
                        date_of_birth=datetime.date(1990, 10, 10),
                        country='country')

        crud.user.create(db_session=db_session, user_in=user)

        image_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')
        image_in = ImageCreate(user_id=user_id,
                               image_str=image_str,
                               image_type=ImageType.identity)
        crud.image.create(db_session=db_session, image_in=image_in)

        return user_id


    def test_create_image_file(self):
        user_id = self.db_create_rows()
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(os.path.isfile(face_image_path))


    def test_get_texts(self):
        user_id = self.db_create_rows()
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        verification_utils.create_image_file(user_id=user_id, image_type=ImageType.identity)
        texts = verification_utils.get_texts(user_id=user_id)
        self.assertTrue(len(texts) > 0)


    def test_get_doc(self):
        user_id = self.db_create_rows()
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        verification_utils.create_image_file(user_id=user_id, image_type=ImageType.identity)
        texts = verification_utils.get_texts(user_id=user_id)
        print(texts)
        doc = verification_utils.get_doc(texts=texts, language='en_core_web_sm')
        expected_list = [('1234567', 'DATE'),
                         ('Card Identity National Henderso', 'ORG'),
                         ('Elizabeth', 'PERSON'),
                         ('British', 'NORP'),
                         ('London', 'GPE'),
                         ('11-08', 'DATE')]
        self.assertEqual(doc, expected_list)


    def test_create_user_text_label(self):
        user_id = self.db_create_rows()
        user = crud.user.get(db_session=db_session, user_id=user_id)
        user_text_label = verification_utils.create_user_text_label(user=user)
        self.assertEqual(user_text_label, {'PERSON': ['name', 'surname'], 'DATE': datetime.date(1990, 10, 10), 'GPE': 'country'})


    def test_validate_text_label(self):
        user_id = utils.create_user_id()
        user = UserCreate(user_id=user_id,
                          name='Elizabeth',
                          surname='Henderson',
                          date_of_birth=datetime.date(1977, 4, 14),
                          country='London')
        crud.user.create(db_session=db_session, user_in=user)

        image_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')
        image_in = ImageCreate(user_id=user_id,
                               image_str=image_str,
                               image_type=ImageType.identity)
        crud.image.create(db_session=db_session, image_in=image_in)

        user = crud.user.get(db_session=db_session, user_id=user_id)
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        texts = verification_utils.get_texts(user_id=user_id)
        doc_text_label = verification_utils.get_doc(texts, language='en_core_web_sm')
        user_text_label = verification_utils.create_user_text_label(user)
        text_validation_point = verification_utils.validate_text_label(doc_text_label, user_text_label)
        self.assertEqual(text_validation_point, 0.5)


    def test_validate_text_label_simple(self):
        user_id = utils.create_user_id()
        user = UserCreate(user_id=user_id,
                          name='Elizabeth',
                          surname='Henderson',
                          date_of_birth=datetime.date(1977, 4, 14),
                          country='London')
        user_text_label = verification_utils.create_user_text_label(user)
        doc_text_label = [('1234567', 'DATE'),
                         ('Card Identity National Henderso', 'ORG'),
                         ('Elizabeth', 'PERSON'),
                         ('British', 'NORP'),
                         ('London', 'GPE'),
                         ('11-08', 'DATE')]
        text_validation_point = verification_utils.validate_text_label(doc_text_label, user_text_label)
        self.assertEqual(text_validation_point, 0.50)


    def test_recognize_face(self):
        user_id = utils.create_user_id()
        user = UserCreate(user_id=user_id,
                          name='Elizabeth',
                          surname='Henderson',
                          date_of_birth=datetime.date(1977, 4, 14),
                          country='London')
        crud.user.create(db_session=db_session, user_in=user)

        image_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')
        image_in = ImageCreate(user_id=user_id,
                               image_str=image_str,
                               image_type=ImageType.identity)
        crud.image.create(db_session=db_session, image_in=image_in)

        user = crud.user.get(db_session=db_session, user_id=user_id)
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        names = verification_utils.recognize_face(user_id=user_id)
        self.assertIsNotNone(names)


    def test_point_on_recognition_succeed(self):
        user_id = utils.create_user_id()
        user = UserCreate(user_id=user_id,
                          name='Elizabeth',
                          surname='Henderson',
                          date_of_birth=datetime.date(1977, 4, 14),
                          country='London')
        crud.user.create(db_session=db_session, user_in=user)

        image_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')
        image_in = ImageCreate(user_id=user_id,
                               image_str=image_str,
                               image_type=ImageType.identity)
        crud.image.create(db_session=db_session, image_in=image_in)

        user = crud.user.get(db_session=db_session, user_id=user_id)
        (file_path, face_image_path) = verification_utils.create_image_file(user_id=user_id,
                                                                            image_type=ImageType.identity)
        names = verification_utils.recognize_face(user_id=user_id)
        face_validation_point = verification_utils.point_on_recognition(names, user_id)
        self.assertEqual(face_validation_point, 0.25)


    def test_point_on_recognition_fails(self):
        face_validation_point = verification_utils.point_on_recognition(None, 'user_id')
        self.assertEqual(face_validation_point, 0.0)
        face_validation_point = verification_utils.point_on_recognition(['test'], 'user_id')
        self.assertEqual(face_validation_point, 0.0)

    def main(self):
        self.test_create_image_file()
        self.test_get_texts()
        self.test_get_doc()
        self.test_create_user_text_label()
        self.test_validate_text_label()
        self.test_validate_text_label_simple()
        self.test_recognize_face()
        self.test_point_on_recognition_succeed()
        self.test_point_on_recognition_fails()


if __name__ == "__main__":
    verification_tests = VerificationUtilsTest()
    verification_tests.main()
