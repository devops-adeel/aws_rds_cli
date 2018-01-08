#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           setup.py
Author:         Adeel Ahmad
Description:    Setup Files required for the cli app.
"""
from setuptools import find_packages, setup

about = {}
with open("__version__.py") as f:
    exec(f.read(), about)

setup(
    name='RDS',
    version=about['__version__'],
    description='AWS CLi for RDS Blue/Green',
    author='Adeel Ahmad',
    py_modules=['rds'],
    install_requires=[
        'Click',
        'Boto3',
        'Botocore',
        ],
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    entry_points='''
        [console_scripts]
        rds=rds:cli
    ''',
    )
