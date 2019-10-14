#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from enum import Enum


class ImageType(Enum):
    identity = 1
    profile = 2

    def __int__(self):
        return self.value


class ImageCreate(BaseModel):
    image_id: int = None
    user_id: str = None
    image_str: str = None
    image_type: int = None
