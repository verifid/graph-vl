#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphvl import crud
from graphvl.core import config
from graphvl.db import session
from graphvl.models.user import UserCreate

from sqlalchemy import Table, Column, String, Date, Integer, MetaData


def init_db(db_session):
    meta = MetaData(db_session)
    user_table = Table('Users', meta,  
                        Column('name', String, index=True),
                        Column('surname', String, index=True),
                        Column('date_of_birth', Date),
                        Column('country', String),
                        Column('user_id', String, index=True))

    with session.engine.connect() as conn:
        # Create
        user_table.create()
        # insert_statement = user_table.insert().values()
        # conn.execute(insert_statement)
