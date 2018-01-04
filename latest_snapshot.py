#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_restore.py
Author:         Adeel Ahmad
Description:    Python Script to restore from RDS Backup
"""

from botocore.exceptions import ClientError
import boto3
import click

__version__ = "0.1"

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


@click.command()
@click.option('--instanceid', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
def cli(instanceid):
    """This is a cli tool to find the latest snapshot for a given RDS instanceid
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
            click.secho(latest, fg='green')
        except ClientError as error:
            click.secho(error, fg='red')
    else:
        try:
            snapshots = RDS.describe_db_snapshots(
                DBInstanceIdentifier=instanceid
                )
            latest = sorted(snapshots['DBSnapshots'], key=lambda item:
                            item['SnapshotCreateTime'],
                            reverse=True)[0]['DBSnapshotIdentifier']
            click.secho(latest, fg='green')
        except ClientError as error:
            click.secho(error, fg='red')


if __name__ == '__main__':
    cli()
    import doctest
    doctest.testmod()
