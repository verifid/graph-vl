#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphvl.db.base_class import Base
from graphvl.db.session import engine


def init_db():
    Base.metadata.create_all(engine)
