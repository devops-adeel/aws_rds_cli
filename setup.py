#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           setup.py
Author:         Adeel Ahmad
Description:    Setup Files required for the cli app.
"""
from setuptools import find_packages, setup

setup(
    name='RDS',
    version='0.1',
    py_modules=['rds'],
    install_requires=[
        'Click',
        'Boto3',
        'Botocore',
        ],
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        rds=rds:cli
    '''
    )
