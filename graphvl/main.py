#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import graphene


from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.schema import UserQuery, ImageQuery
from graphvl.schema import UserMutation, ImageMutation


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query, mutation=UserMutation)))
