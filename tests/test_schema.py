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

    def create_user(self, include_user_id=False):
        schema = graphene.Schema(query=UserQuery, mutation=UserMutation)
        client = Client(schema)
        user_id = ''
        if include_user_id:
            user_id = 'userId'
        executed = client.execute('''mutation {
                                        createUser(country: "country", dateOfBirth: "01-01-1960", name: "name", surname: "surname") {
                                            ok
                                            user {
                                                country
                                                dateOfBirth
                                                name
                                                surname
                                                %s
                                            }
                                        }
                                    }''' % user_id)
        return executed


    def create_image(self, image_str, image_type, user_id):
        schema = graphene.Schema(query=ImageQuery, mutation=ImageMutation)
        client = Client(schema)
        if image_type == ImageType.identity:
            image_type = 'identity'
        else:
            image_type = 'profile'
        executed = client.execute('''mutation {
                                        createImage(imageStr: "%s", imageType: %s, userId: "%s") {
                                            ok
                                            image {
                                                userId
                                            }
                                        }
                                    }''' % (image_str, image_type, user_id))
        return executed


    def test_create_user(self):
        executed = self.create_user()
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
        executed = self.create_user(include_user_id=True)
        self.assertIsNotNone(executed['data']['createUser']['user'])
        user_id = executed['data']['createUser']['user']['userId']
        executed = self.create_image(image_str='image', image_type=ImageType.identity, user_id=user_id)
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
        executed = self.create_user(include_user_id=True)
        self.assertIsNotNone(executed['data']['createUser']['user'])
        user_id = executed['data']['createUser']['user']['userId']
        schema = graphene.Schema(query=ImageQuery, mutation=ImageMutation)
        client = Client(schema)

        image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')

        executed = self.create_image(image_str=image_str, image_type=ImageType.identity, user_id=user_id)
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
            image_str = base64.b64encode(imageFile.read()).decode('utf-8')

        executed = self.create_image(image_str=image_str, image_type=ImageType.profile, user_id=user_id)
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
                                                        ok,
                                                        verificationRate
                                                    }
                                                }
                                               ''' % user_id)
        assert executed == {'data':
                                OrderedDict(
                                    [('verify',
                                        OrderedDict([('ok', True),
                                        ('verificationRate', 25)])
                                    )]
                                )
                            }


    def main(self):
        self.test_verify_user()


if __name__ == "__main__":
    schema_tests = SchemaTest()
    schema_tests.main()