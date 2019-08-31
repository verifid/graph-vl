#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    name: str = None
    surname: str = None
    date_of_birth: str = None
    country: str = None


class UserBaseInDB(UserBase):
    id: int = None


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    user_id: str
