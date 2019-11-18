#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import graphene
import base64

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
                        date_of_birth='1990-10-10',
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
        doc = verification_utils.get_doc(texts=texts, language='en_core_web_sm')
        expected_list = [('1234567', 'DATE'),
                         ('Card Identity National Henderso', 'ORG'),
                         ('Elizabeth', 'PERSON'),
                         ('British', 'NORP'),
                         ('London', 'GPE'),
                         ('11-08', 'DATE')]
        self.assertEqual(doc, expected_list)


    def main(self):
        self.test_create_image_file()
        self.test_get_texts()
        self.test_get_doc()


if __name__ == "__main__":
    verification_tests = VerificationUtilsTest()
    verification_tests.main()
