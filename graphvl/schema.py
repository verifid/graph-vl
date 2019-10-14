#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import graphene
import base64
import cv2

from mocr import face_detection

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphvl.scalar import Date
from graphvl.utils import utils
from graphvl.models.user import UserCreate
from graphvl.models.image import ImageCreate, ImageType
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

    def mutate(self, info, country, date_of_birth, name, surname):
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


class UserQuery(graphene.ObjectType):
    user = graphene.Field(User, description='User object')


class Image(graphene.ObjectType):
    user_id = graphene.String(required=True, description='UserId created with a new user')
    image_str = graphene.String(required=True, description='Base64 encoded binary string of image')
    image_type = graphene.Int(required=True, description='Image file type identity = 1, profile = 2')


class CreateImage(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True, description='UserId created with a new user')
        image_str = graphene.String(required=True, description='Base64 encoded binary string of image')
        image_type = graphene.Enum.from_enum(ImageType)(required=True, description='Image file type identity = 1, profile = 2')

    ok = graphene.Boolean()
    image = graphene.Field(lambda: Image)

    def mutate(self, info, user_id, image_str, image_type):
        image_in = ImageCreate(user_id=user_id,
                               image_str=image_str,
                               image_type=image_type)
        image = crud.image.create(db_session, image_in=image_in)
        ok = True
        return CreateImage(image=image, ok=ok)


class ImageMutation(graphene.ObjectType):
    create_image = CreateImage.Field()


class ImageQuery(graphene.ObjectType):
    image = graphene.Field(Image, description='Image object')


def create_image_file(user_id, image_type):
    image = crud.image.get(db_session, user_id=user_id, image_type=image_type)
    if image:
        photo_data = base64.b64decode(image.image_str)

        if image_type == ImageType.identity:
            path = 'identity/'
        else:
            path = 'profile/'

        directory = os.getcwd() + '/testsets/' + path +  user_id + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + 'image' + '.jpg'
        with open(file_path, 'wb') as f:
            f.write(photo_data)

        # detect face from identity image
        if image_type == ImageType.identity:
            face_image = face_detection.detect_face(file_path)
            face_directory = os.getcwd() + '/testsets/' + 'face/' + user_id + '/'
            if not os.path.exists(face_directory):
                os.makedirs(face_directory)
            cv2.imwrite(face_directory + 'image.jpg', face_image)


class Verify(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True, description='UserId created with a new user')
        language = graphene.String(required=True, description='Language model for verification')

    ok = graphene.Boolean()
    verify = graphene.Field(lambda: Verify)

    def mutate(self, info, user_id, language):
        user = crud.user.get(db_session, user_id=user_id)
        create_image_file(user_id=user_id, image_type=ImageType.identity)
        create_image_file(user_id=user_id, image_type=ImageType.profile)
        ok = True
        verify = None


class VerifyMutation(graphene.ObjectType):
    verify = Verify.Field()


class VerifyQuery(graphene.ObjectType):
    verify = graphene.Field(Verify, description='Verify object')
