#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene


from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.scalar import Date
from graphvl.utils import utils
from graphvl.models.user import UserCreate
from graphvl import crud
from graphvl.db.session import db_session

from datetime import datetime


class User(graphene.ObjectType):
    country = graphene.String(required=True, description='Living country of user')
    date_of_birth = Date(required=True, description='Born date of user in format of dd-MM-yyyy')
    name = graphene.String(required=True, description='Name of user')
    surname = graphene.String(required=True, description='Surname of user')
    user_id = graphene.String(description='Unique id defined by api')


class CreateUser(graphene.Mutation):
    class Arguments:
        country = graphene.String(required=True, description='Living country of user')
        date_of_birth = Date(required=True, description='Born date of user in format of dd-MM-yyyy')
        name = graphene.String(required=True, description='Name of user')
        surname = graphene.String(required=True, description='Surname of user')

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User)

    def mutate(root, info, country, date_of_birth, name, surname):
        user_id = utils.create_user_id()
        date = date_of_birth.strftime('%d/%m/%Y')
        user_in = UserCreate(user_id=user_id,
                             name=name,
                             surname=surname,
                             date_of_birth=date,
                             country=country)
        user = crud.user.create(db_session, user_in=user_in)
        ok = True
        return CreateUser(user=user, ok=ok)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    user = graphene.Field(User, description='User object')
