#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import graphene

with open('env-postgres.env') as f:
    for line in f:
        key, value = line.replace('export ', '', 1).strip().split('=', 1)
        os.environ[key] = value

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.schema import Query
from graphvl.schema import UserMutation


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query, mutation=UserMutation)))
