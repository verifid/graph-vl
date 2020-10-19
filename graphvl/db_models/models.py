#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Date, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from graphvl.db.base_class import Base


class User(Base):
    user_id = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    date_of_birth = Column(Date)
    country = Column(String)


class Image(Base):
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.user_id"), index=True)
    image_str = Column(String)
    image_type = Column(Integer)
