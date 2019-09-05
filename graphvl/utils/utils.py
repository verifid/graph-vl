#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid


def create_user_id():
    uid_str = uuid.uuid4().urn
    user_id = uid_str[9:]
    return user_id
