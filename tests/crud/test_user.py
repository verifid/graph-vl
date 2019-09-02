#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import uuid


with open('env-postgres.env') as f:
    for line in f:
        key, value = line.replace('export ', '', 1).strip().split('=', 1)
        os.environ[key] = value


from graphvl import crud
from graphvl.db.session import db_session
from graphvl.models.user import UserCreate
from graphvl.db import init_db


init_db.init_db()


class UserTest(unittest.TestCase):

    def test_create(self):
        user_id = str(uuid.uuid4)
        user_in = UserCreate(user_id=user_id,
                             name='name',
                             surname='surname',
                             date_of_birth='10.10.1990',
                             country='Turkey')
        crud.user.create(db_session, user_in=user_in)
        user_out = crud.user.get(db_session, user_id=user_id)
        self.assertIsNotNone(user_out)
        self.assertEqual(user_out.user_id, user_in.user_id)
        self.assertEqual(user_out.name, user_in.name)
        self.assertEqual(user_out.surname, user_in.surname)
        self.assertEqual(user_out.country, user_in.country)
