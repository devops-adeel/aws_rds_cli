#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           setup.py
Author:         Adeel Ahmad
Description:    Setup Files required for the cli app.
"""
from setuptools import setup

setup(
    name='Hello',
    version='0.1',
    py_modules=['hello'],
    install_requires=[
        'Click',
        ],
    entry_points='''
        [console_scripts]
        hello=hello:hello
    '''
    )
