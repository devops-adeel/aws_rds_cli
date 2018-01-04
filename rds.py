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


def query_db_cluster(instanceid):
    """
    Querying whether DB is Clustered or not
    """
    try:
        db_instance = RDS.describe_db_instances(
            DBInstanceIdentifier=instanceid
            )
        return db_instance['DBInstances'][0]['DBClusterIdentifier']
    except KeyError:
        return False


@click.group()
def cli():
    """
    This command line tool will allow you to clone RDS snapshots for
    Blue/Green Deployment as well carrying out restore.
    There are several options and commands to use.  Please see below options.
    """
    pass


@click.command()
@click.option('--instanceid', prompt='Please provide DB ID',
              help='The ID of the DB Instance.')
@click.option('--newid', prompt='Please provide the new target id',
              help='The ID of the DB Instance.')
def clone(instanceid):
    """
    Function to clone RDS instance/cluster
    for Blue/Green Deployement.
    """
    return instanceid


cli.add_command(clone)

if __name__ == '__main__':
    cli()
    import doctest
    doctest.testmod()
