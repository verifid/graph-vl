#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import base64

from datetime import date

from graphvl import crud
from graphvl.db.session import db_session
from graphvl.models.user import UserCreate
from graphvl.models.image import ImageCreate, ImageType
from graphvl.utils import utils


class ImageTest(unittest.TestCase):
    def test_create_image(self):
        user_id = utils.create_user_id()
        user_in = UserCreate(
            user_id=user_id,
            name="name",
            surname="surname",
            date_of_birth=date(1990, 10, 10),
            country="Turkey",
        )
        crud.user.create(db_session, user_in=user_in)
        image_path = (
            os.path.dirname(os.path.dirname(__file__))
            + "/resources/sample_uk_identity_card.png"
        )
        with open(image_path, "rb") as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode("utf-8")
        image_in = ImageCreate(
            user_id=user_id, image_str=image_str, image_type=ImageType.identity.value
        )
        crud.image.create(db_session, image_in=image_in)
        image_out = crud.image.get(
            db_session, user_id=user_id, image_type=image_in.image_type
        )
        self.assertIsNotNone(image_out)
        self.assertEqual(image_out.user_id, user_id)
        self.assertEqual(image_out.image_str, image_str)
        self.assertEqual(image_out.image_type, ImageType.identity.value)

    def main(self):
        self.test_create_image()


if __name__ == "__main__":
    image_tests = ImageTest()
    image_tests.main()
