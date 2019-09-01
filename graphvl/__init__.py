#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Self deployed identity verification layer with GraphQL.'''

from __future__ import absolute_import

__author__       = 'Abdullah Selek'
__email__        = 'abdullahselek@gmail.com'
__copyright__    = 'Copyright (c) 2019 Abdullah Selek'
__license__      = 'MIT License'
__version__      = '0.1'
__url__          = 'https://github.com/verifid/graph-vl'
__download_url__ = 'https://github.com/verifid/graph-vl'
__description__  = 'Self deployed identity verification layer with GraphQL.'

from graphvl import (
    schema,
    scalar
)

from graphvl.schema import (
    Query,
    UserMutation
)

from graphvl.core import config
from graphvl.db.base_class import CustomBase
from graphvl.db import (
    session,
    init_db
)

from graphvl.models import user
from graphvl.crud import user
