#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import graphene
import base64
import cv2

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.scalar import Date
from graphvl.utils import utils, verification_utils
from graphvl.models.user import UserCreate
from graphvl.models.image import ImageCreate, ImageType
from graphvl import crud
from graphvl.db.session import db_session

from datetime import datetime


class User(graphene.ObjectType):
    country = graphene.String(required=True, description="Living country of user")
    date_of_birth = Date(
        required=True, description="Born date of user in format of dd-MM-yyyy"
    )
    name = graphene.String(required=True, description="Name of user")
    surname = graphene.String(required=True, description="Surname of user")
    user_id = graphene.String(description="Unique id defined by api")


class CreateUser(graphene.Mutation):
    class Arguments:
        country = graphene.String(required=True, description="Living country of user")
        date_of_birth = Date(
            required=True, description="Born date of user in format of dd-MM-yyyy"
        )
        name = graphene.String(required=True, description="Name of user")
        surname = graphene.String(required=True, description="Surname of user")

    ok = graphene.Boolean(description="Defines success or fail")
    user = graphene.Field(lambda: User, description="Details of user")

    def mutate(self, info, country, date_of_birth, name, surname):
        user_id = utils.create_user_id()
        user_in = UserCreate(
            user_id=user_id,
            name=name,
            surname=surname,
            date_of_birth=date_of_birth,
            country=country,
        )
        user = crud.user.create(db_session, user_in=user_in)
        ok = True
        return CreateUser(user=user, ok=ok)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field(
        description="Creates a new user with given parameters"
    )


class UserQuery(graphene.ObjectType):
    user = graphene.Field(
        User, user_id=graphene.String(), description="Query user by user id"
    )

    def resolve_user(self, info, user_id):
        return crud.user.get(db_session=db_session, user_id=user_id)


class Image(graphene.ObjectType):
    user_id = graphene.String(
        required=True, description="UserId created with a new user"
    )
    image_str = graphene.String(
        required=True, description="Base64 encoded binary string of image"
    )
    image_type = graphene.Int(
        required=True, description="Image file type identity = 1, profile = 2"
    )


class CreateImage(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(
            required=True, description="UserId created with a new user"
        )
        image_str = graphene.String(
            required=True, description="Base64 encoded binary string of image"
        )
        image_type = graphene.Enum.from_enum(ImageType)(
            required=True, description="Image file type identity = 1, profile = 2"
        )

    ok = graphene.Boolean(description="Defines success or fail")
    image = graphene.Field(lambda: Image, description="Details of image")

    def mutate(self, info, user_id, image_str, image_type):
        image_in = ImageCreate(
            user_id=user_id, image_str=image_str, image_type=image_type
        )
        image = crud.image.create(db_session, image_in=image_in)
        ok = True
        return CreateImage(image=image, ok=ok)


class ImageMutation(graphene.ObjectType):
    create_image = CreateImage.Field(
        description="Uploads user image with given parameters"
    )


class ImageQuery(graphene.ObjectType):
    image = graphene.Field(
        Image, user_id=graphene.String(), description="Query image by user id"
    )

    def resolve_image(self, info, user_id):
        return crud.image.get(
            db_session=db_session, user_id=user_id, image_type=ImageType.identity
        )


class Verify(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(
            required=True, description="UserId created with a new user"
        )
        language = graphene.String(
            required=True, description="Language model for verification"
        )

    ok = graphene.Boolean(description="Defines success or fail")
    verification_rate = graphene.Float(
        description="Value of verification between 0 and 1"
    )

    def mutate(self, info, user_id, language):
        user = crud.user.get(db_session, user_id=user_id)
        verification_utils.create_image_file(
            user_id=user_id, image_type=ImageType.identity
        )
        verification_utils.create_image_file(
            user_id=user_id, image_type=ImageType.profile
        )
        texts = verification_utils.get_texts(user_id=user_id)
        doc_text_label = verification_utils.get_doc(texts=texts, language=language)
        if not doc_text_label:
            ok = False
            return Verify(verification_rate=0, ok=ok)

        user_text_label = verification_utils.create_user_text_label(user)
        text_validation_point = verification_utils.validate_text_label(
            doc_text_label, user_text_label
        )
        print("text_validation_point: " + str(text_validation_point))
        names = verification_utils.recognize_face(user_id)
        if not names:
            ok = False
            return Verify(verification_rate=0, ok=ok)

        face_validation_point = verification_utils.point_on_recognition(names, user_id)
        print("face_validation_point: " + str(face_validation_point))
        verification_rate = text_validation_point + face_validation_point

        ok = True
        return Verify(verification_rate=verification_rate, ok=ok)


class VerifyMutation(graphene.ObjectType):
    verify = Verify.Field(description="Verify user identity with given parameters")


class VerifyQuery(graphene.ObjectType):
    verify = graphene.Field(Verify, description="Verify object")


class Query(UserQuery, ImageQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, ImageMutation, VerifyMutation, graphene.ObjectType):
    pass
