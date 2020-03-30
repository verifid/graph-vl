#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

from datetime import date

from graphvl import crud
from graphvl.db.session import db_session
from graphvl.models.user import UserCreate
from graphvl.utils import utils


class UserTest(unittest.TestCase):

    def test_create_user(self):
        user_id = utils.create_user_id()
        user_in = UserCreate(user_id=user_id,
                             name='name',
                             surname='surname',
                             date_of_birth=date(1990, 10, 10),
                             country='Turkey')
        crud.user.create(db_session, user_in=user_in)
        user_out = crud.user.get(db_session, user_id=user_id)
        self.assertIsNotNone(user_out)
        self.assertEqual(user_out.user_id, user_in.user_id)
        self.assertEqual(user_out.name, user_in.name)
        self.assertEqual(user_out.surname, user_in.surname)
        self.assertEqual(user_out.country, user_in.country)


    def main(self):
        self.test_create_user()


if __name__ == '__main__':
    user_tests = UserTest()
    user_tests.main()
