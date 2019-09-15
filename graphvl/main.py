#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import graphene

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.schema import UserQuery, ImageQuery
from graphvl.schema import UserMutation, ImageMutation
from graphvl.router.api_router import router


app = FastAPI()
app.include_router(router)
