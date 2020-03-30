#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from graphene.types import Scalar
from graphql.language import ast


class Date(Scalar):
    '''Date Scalar Description'''

    @staticmethod
    def serialize(dt):
        return Date.to_str(dt)


    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, '%d-%m-%Y')


    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, '%d-%m-%Y')


    @staticmethod
    def to_str(value):
        return value.strftime('%d-%m-%Y')
