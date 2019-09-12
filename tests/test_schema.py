#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import graphene
import pytest

from collections import OrderedDict
from graphene.test import Client
from graphvl.schema import UserQuery, UserMutation
from graphvl.schema import ImageQuery, ImageMutation


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
                                        createImage(imageStr: "txt", imageType: 1, userId: "%s") {
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
