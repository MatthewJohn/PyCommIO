#!/usr/bin/env python

from setuptools import setup, find_packages

import pycommio

with open('VERSION', 'r') as version_fh:
    version = version_fh.read()

setup(
    name='pycommio',
    version=version,
    license='GNU GENERAL PUBLIC LICENSE',
    author='Matt Comben',
    platforms='any',
    author_email='matthew@dockstudios.co.uk',
    packages=list(find_packages())
)
