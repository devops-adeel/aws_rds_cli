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


@click.option('--count', default=1, help='Number of clones.')
@click.option('--name', prompt='Please provide DB ID',
              help='The ID of the DB Instance or Cluster')
@click.group()
def cli():
    """
    This will the  main
    """
    pass


@click.command()
@click.argument('--instanceid', prompt='Please provide DB ID',
                help='The ID of the DB Instance.')
@click.argument('--newid', prompt='Please provide the new target id',
                help='The ID of the DB Instance.')
def restore(instanceid, newid):
    """
    Main function restore from latest snapshot.
    """
    if query_db_cluster(instanceid):
        cluster_id = query_db_cluster(instanceid)
        try:
            response = RDS.restore_db_cluster_to_point_in_time(
                DBClusterIdentifier=newid,
                SourceDBClusterIdentifier=cluster_id,
                UseLatestRestorableTime=True
                )
            return response['DBCluster'][0]['Status']
        except ClientError as error:
            print(error)
    else:
        try:
            response = RDS.restore_db_instance_to_point_in_time(
                SourceDBInstanceIdentifier=instanceid,
                TargetDBInstanceIdentifier=newid,
                UseLatestRestorableTime=True
                )
            return response['DBInstance'][0]['DBInstanceStatus']
        except ClientError as error:
            print(error)


@click.command()
def clone(instanceid):
    """
    Function to clone RDS instance/cluster for Blue/Green Deployement.
    """
    return instanceid


cli.add_command(restore)
cli.add_command(clone)
