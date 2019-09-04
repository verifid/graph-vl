#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse


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
        os.system('source ./set_environment_variables.sh env-postgres.env')
        init_db.init_db()