#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import unittest
import graphene
import pytest

from collections import OrderedDict
from graphene.test import Client
from graphvl.schema import UserQuery, UserMutation
from graphvl.schema import ImageQuery, ImageMutation
from graphvl.schema import VerifyQuery, VerifyMutation
from graphvl.models.image import ImageType


class SchemaTest(unittest.TestCase):


    def test_create_user(self):
        schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
        client = Client(schema)
        executed = client.execute('''mutation {
                                        createUser(country: "country", dateOfBirth: "01-01-1960", name: "name", surname: "surname") {
                                            ok
                                            user {
                                                country
                                                dateOfBirth
                                                name
                                                surname
                                            }
                                        }
                                    }''')
        assert executed == {'data':
                                OrderedDict(
                                    [('createUser',
                                        OrderedDict([('ok', True),
                                        ('user',
                                            OrderedDict([('country', 'country'),
                                            ('dateOfBirth', '1960-01-01'),
                                            ('name', 'name'),
                                            ('surname', 'surname')])
                                        )])
                                    )]
                                )
                            }


    def test_create_image(self):
        user_schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
        user_client = Client(user_schema)
        executed = user_client.execute('''mutation {
                                            createUser(country: "country", dateOfBirth: "01-01-1960", name: "name", surname: "surname") {
                                                ok
                                                user {
                                                    country
                                                    dateOfBirth
                                                    name
                                                    surname
                                                    userId
                                                }
                                            }
                                        }''')
        self.assertIsNotNone(executed['data']['createUser']['user'])
        user_id = executed['data']['createUser']['user']['userId']
        schema = graphene.Schema(query=ImageQuery, mutation=ImageMutation)
        client = Client(schema)
        executed = client.execute('''mutation {
                                        createImage(imageStr: "txt", imageType: identity, userId: "%s") {
                                            ok
                                            image {
                                                userId
                                            }
                                        }
                                    }''' % user_id)
        assert executed == {'data':
                                OrderedDict(
                                    [('createImage',
                                        OrderedDict([('ok', True),
                                        ('image', OrderedDict([('userId', '%s' % user_id)]))]
                                        )
                                    )]
                                )
                            }


    def test_verify_user(self):
        user_schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
        user_client = Client(user_schema)
        executed = user_client.execute('''mutation {
                                            createUser(country: "country", dateOfBirth: "01-01-1960", name: "name", surname: "surname") {
                                                ok
                                                user {
                                                    country
                                                    dateOfBirth
                                                    name
                                                    surname
                                                    userId
                                                }
                                            }
                                        }''')
        self.assertIsNotNone(executed['data']['createUser']['user'])
        user_id = executed['data']['createUser']['user']['userId']
        schema = graphene.Schema(query=ImageQuery, mutation=ImageMutation)
        client = Client(schema)

        image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_data = base64.b64encode(imageFile.read()).decode('utf-8')

        executed = client.execute('''mutation {
                                        createImage(imageStr: "%s", imageType: identity, userId: "%s") {
                                            ok
                                            image {
                                                userId
                                            }
                                        }
                                    }''' % (image_data, user_id))
        assert executed == {'data':
                                OrderedDict(
                                    [('createImage',
                                        OrderedDict([('ok', True),
                                        ('image', OrderedDict([('userId', '%s' % user_id)]))]
                                        )
                                    )]
                                )
                            }

        image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/selfie.jpg'
        with open(image_path, 'rb') as imageFile:
            image_data = base64.b64encode(imageFile.read()).decode('utf-8')

        executed = client.execute('''mutation {
                                        createImage(imageStr: "%s", imageType: profile, userId: "%s") {
                                            ok
                                            image {
                                                userId
                                            }
                                        }
                                    }''' % (image_data, user_id))
        assert executed == {'data':
                                OrderedDict(
                                    [('createImage',
                                        OrderedDict([('ok', True),
                                        ('image', OrderedDict([('userId', '%s' % user_id)]))]
                                        )
                                    )]
                                )
                            }

        verification_schema = graphene.Schema(query=VerifyQuery, mutation=VerifyMutation)
        verification_client = Client(verification_schema)
        executed = verification_client.execute('''mutation {
                                                    verify(language: "en_core_web_sm", userId: "%s") {
                                                        ok
                                                    }
                                                }
                                               ''' % user_id)
        print(executed)
