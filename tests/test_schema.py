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

    @pytest.mark.run(order=1)
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
        self.user_id = executed['data']['createUser']['user']['userId']


    @pytest.mark.run(order=2)
    def test_create_image(self):
        schema = graphene.Schema(query=ImageQuery, mutation=ImageMutation)
        client = Client(schema)
        executed = client.execute('''mutation {
                                        createImage(imageStr: "txt", imageType: 1, userId: "{}") {
                                            ok
                                            image {
                                            userId
                                            }
                                        }
                                    }'''.format(self.user_id))
        assert executed == {'data':
                                OrderedDict(
                                    [('createImage',
                                        OrderedDict([('ok', True),
                                        ('image', OrderedDict([('userId', '1145b78f-5b7a-43e0-9437-2033bd880769')]))]
                                        )
                                    )]
                                )
                            }
