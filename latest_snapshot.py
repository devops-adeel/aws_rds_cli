#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_restore.py
Author:         Adeel Ahmad
Description:    Python Script to restore from RDS Backup
"""

from __future__ import absolute_import, \
        division, print_function, unicode_literals
from botocore.exceptions import ClientError
import boto3
import click

__version__ = "0.1"

click.disable_unicode_literals_warning = True
RDS = boto3.client('rds')


@click.command()
@click.option('--instanceid', prompt='Please provide DB ID',
              help='The ID of the DB Instance.')
def cli(instanceid):
    """
    This is a cli tool to find the latest snapshot for a given RDS instanceid
    """
    try:
        snapshots = RDS.describe_db_snapshots(
            DBInstanceIdentifier=instanceid
            )
        print(snapshots)
    except ClientError as error:
        print(error)

if __name__ == '__main__':
    cli()
    import doctest
    doctest.testmod()