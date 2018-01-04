#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_copy.py
Author:         Adeel Ahmad
Description:    Python Script to copy snapshot and deploy
"""

from __future__ import absolute_import, \
        division, print_function, unicode_literals
from datetime import datetime
from botocore.exceptions import ClientError
import boto3
import click

__version__ = "0.1"

click.disable_unicode_literals_warning = True
RDS = boto3.client('rds')
INSTANCEID = "instanceid"
NEWID = "newid"


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


def retrieve_latest_snapshot(instanceid):
    """
    Function to retrieve latest snapshot
    """
    if query_db_cluster(instanceid):
        clusterid = query_db_cluster(instanceid)
        try:
            snapshots = RDS.describe_db_cluster_snapshots(
                DBClusterIdentifier=clusterid
                )
            latest = sorted(snapshots['DBClusterSnapshots'], key=lambda item:
                            item['SnapshotCreateTime'],
                            reverse=True)[0]['DBClusterSnapshotIdentifier']
            click.echo(latest)
        except ClientError as error:
            click.echo(error)
    else:
        try:
            snapshots = RDS.describe_db_snapshots(
                DBInstanceIdentifier=instanceid
                )
            latest = sorted(snapshots['DBSnapshots'], key=lambda item:
                            item['SnapshotCreateTime'],
                            reverse=True)[0]['DBSnapshotIdentifier']
            click.echo(latest)
        except ClientError as error:
            click.echo(error)


@click.command()
@click.option('--instanceid', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
@click.option('--newid', prompt=True,
              help='The ID of the DB Instance.')
def cli(instanceid, newid):
    """
    This command will restore RDS DB from latest snapshot.
    """
    snapshotid = retrieve_latest_snapshot(instanceid)
    if query_db_cluster(instanceid):
        try:
            response = RDS.copy_db_cluster_snapshot(
                SourceDBClusterSnapshotIdentifier=snapshotid,
                TargetDBClusterSnapshotIdentifier=newid
                )
            return response['DBClusterSnapshot'][0]['Status']
        except ClientError as error:
            click.echo(error)
    else:
        try:
            response = RDS.copy_db_snapshot(
                SourceDBSnapshotIdentifier=snapshotid,
                TargetDBSnapshotIdentifier=newid
                )
            return response['DBSnapshot'][0]['Status']
        except ClientError as error:
            click.echo(error)


if __name__ == '__main__':
    clone(INSTANCEID, NEWID)
    import doctest
    doctest.testmod()
