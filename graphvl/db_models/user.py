#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Date, Column, Integer, String
from sqlalchemy.orm import relationship

from graphvl.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    date_of_birth = Column(Date)
    country = Column(String)
    user_id = Column(String, index=True)
