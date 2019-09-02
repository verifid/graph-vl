#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import os
import re
import codecs

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    with codecs.open(os.path.join(cwd, filename), 'rb', 'utf-8') as h:
        return h.read()

metadata = read(os.path.join(cwd, 'graphvl', '__init__.py'))

def extract_metaitem(meta):
    meta_match = re.search(r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta),
                           metadata, re.MULTILINE)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements.testing.txt') as f:
    requirements_testing = f.read().splitlines()

setup(
    name='graph-vl',
    version=extract_metaitem('version'),
    license=extract_metaitem('license'),
    description=extract_metaitem('description'),
    long_description=(read('README.rst')),
    author=extract_metaitem('author'),
    author_email=extract_metaitem('email'),
    maintainer=extract_metaitem('author'),
    maintainer_email=extract_metaitem('email'),
    url=extract_metaitem('url'),
    download_url=extract_metaitem('download_url'),
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    platforms=['Any'],
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=requirements_testing,
    python_requires='>=3.6',
    keywords='identity, verification, self deployed api, graphql',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
