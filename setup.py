#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           setup.py
Author:         Adeel Ahmad
Description:    Setup Files required for the cli app.
"""
from setuptools import setup

setup(
    name='RDS',
    version='0.1',
    py_modules=['latest_snapshot'],
    install_requires=[
        'Click',
        'Boto3',
        ],
    entry_points='''
        [console_scripts]
        latest_snapshot=latest_snapshot:cli
    '''
    )
