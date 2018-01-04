#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_copy.py
Author:         Adeel Ahmad
Description:    Python Script to copy snapshot and deploy
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
            return latest
        except KeyError:
            click.secho('Previous Snapshot Still Creating', fg='red')
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
            return latest
        except KeyError:
            click.secho('Previous Snapshot Still Creating', fg='red')
        except ClientError as error:
            click.secho(error, fg='red')


@click.command()
@click.option('--instanceid', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
@click.option('--newid', prompt=True, type=str,
              help='The ID of the DB Instance.')
def cli(instanceid, newid):
    """This command will restore RDS DB from latest snapshot.
    """
    snapshotid = retrieve_latest_snapshot(instanceid)
    if query_db_cluster(instanceid):
        try:
            response = RDS.copy_db_cluster_snapshot(
                SourceDBClusterSnapshotIdentifier=snapshotid,
                TargetDBClusterSnapshotIdentifier=newid
                )
            click.secho(response['DBClusterSnapshot'][0]['Status'], fg='green')
        except ClientError as error:
            click.secho(error, fg='red')
    else:
        try:
            response = RDS.copy_db_snapshot(
                SourceDBSnapshotIdentifier=snapshotid,
                TargetDBSnapshotIdentifier=newid
                )
            click.secho(response['DBSnapshot'][0]['Status'], fg='green')
        except KeyError:
            click.secho(response['DBSnapshot']['Status'], fg='green')
        except ClientError as error:
            click.secho(error, fg='red')


if __name__ == '__main__':
    cli()
    import doctest
    doctest.testmod()
