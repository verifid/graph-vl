#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse


with open('env-postgres.env') as f:
    for line in f:
        key, value = line.replace('export ', '', 1).strip().split('=', 1)
        os.environ[key] = value


from graphvl.db import init_db


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CLI - Self deployed identity verification layer with GraphQL.')
    parser.add_argument('-t', '--table', help='Creates database tables', action='store_true')
    args = parser.parse_args()

    # Optional bash tab completion support
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()
    if args.table:
        init_db.init_db()
