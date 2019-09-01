#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Date, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from graphvl.db.base_class import Base


class User(Base):
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    date_of_birth = Column(Date)
    country = Column(String)


class Image(Base):
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user.user_id'), primary_key=True, index=True)
    image_str = Column(String)
    image_type = Column(Integer)
