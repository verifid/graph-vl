#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene

from fastapi import APIRouter
from starlette.graphql import GraphQLApp

from graphvl.schema import UserQuery, ImageQuery
from graphvl.schema import UserMutation, ImageMutation


router = APIRouter() 
router.add_route('/user', GraphQLApp(schema=graphene.Schema(query=UserQuery, mutation=UserMutation)))
router.add_route('/image', GraphQLApp(schema=graphene.Schema(query=ImageQuery, mutation=ImageMutation)))
