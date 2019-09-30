#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene

from fastapi import APIRouter
from starlette.graphql import GraphQLApp
from starlette.responses import Response

from graphvl.schema import UserQuery, ImageQuery
from graphvl.schema import UserMutation, ImageMutation
from graphvl.schema import VerifyMutation, VerifyQuery


router = APIRouter()


@router.get("/")
async def read_links():
    response = Response('''<html>
                            <body>
                                <head>
                                    <style>
                                        h2 {
                                            color: black;
                                            font-family: arial;
                                        }
                                        a {
                                            color: black;
                                            font-family: arial;
                                        }
                                    </style>
                                </head>
                                <h2>VerifID - Identity Verification Layer</h2>
                                <ul>
                                    <li><a href="/user">User endpoint</a></li>
                                    <li><a href="/image">Image endpoint</a></li>
                                    <li><a href="/user/verify">User verification endpoint</a></li>
                                </ul>
                             </body>
                            </html>''', media_type='text/html')
    return response


router.add_route('/user', GraphQLApp(schema=graphene.Schema(query=UserQuery, mutation=UserMutation)))
router.add_route('/image', GraphQLApp(schema=graphene.Schema(query=ImageQuery, mutation=ImageMutation)))
router.add_route('/user/verify', GraphQLApp(schema=graphene.Schema(query=VerifyQuery, mutation=VerifyMutation)))
