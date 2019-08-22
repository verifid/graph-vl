#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from graphvl.scalar import Date

class User(graphene.ObjectType):
    country = graphene.String(required=True, description='Living country of user')
    date_of_birth = Date(required=True, description='Born date of user in format of dd-MM-yyyy')
    name = graphene.String(required=True, description='Name of user')
    surname = graphene.String(required=True, description='Surname of user')

class CreateUser(graphene.Mutation):
    class Arguments:
        country = graphene.String(required=True, description='Living country of user')
        date_of_birth = Date(required=True, description='Born date of user in format of dd-MM-yyyy')
        name = graphene.String(required=True, description='Name of user')
        surname = graphene.String(required=True, description='Surname of user')

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User)

    def mutate(root, info, country, date_of_birth, name, surname):
        user = User(country=country,
                    date_of_birth=date_of_birth,
                    name=name,
                    surname=surname)
        ok = True
        return CreateUser(user=user, ok=ok)

class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()

class Query(graphene.ObjectType):
    user = graphene.Field(User, description='User object')
