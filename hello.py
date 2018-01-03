#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_restore.py
Author:         Adeel Ahmad
Description:    Python Script to restore from RDS Backup
"""

from __future__ import absolute_import, \
        division, print_function, unicode_literals
import unittest
import click

__version__ = "0.1"

click.disable_unicode_literals_warning = True

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')


def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for amount in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    hello()
    import doctest
    doctest.testmod()
    class MyTest(unittest.TestCase):
        """
        Class to initiate to test function
        """
        def test(self):
            """
            Test Function
            """
            self.assertEqual(hello(3, 'Anas'), 'Anas')
