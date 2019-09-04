#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel


class Image(BaseModel):
    image_id: int = None
    user_id: str = None
    image_str: str = None
    image_type: int = None
