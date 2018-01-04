#!/usr/bin/env python
# -- coding: utf-8 --
"""
File:           rds_copy.py
Author:         Adeel Ahmad
Description:    Python Script to copy snapshot and deploy
"""

from datetime import datetime
from botocore.exceptions import ClientError
import boto3
import click

__version__ = "0.1"

RDS = boto3.client('rds')


def query_db_cluster(instance_id):
    """
    Querying whether DB is Clustered or not
    """
    try:
        response = RDS.describe_db_instances(
            DBInstanceIdentifier=instance_id
            )
        return response['DBInstances'][0]['DBClusterIdentifier']
    except KeyError:
        return False


@click.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
def snapshot(instance_id):
    """This command will create point in time snapshot.
    """
    now = datetime.now()
    if query_db_cluster(instance_id):
        cluster_id = query_db_cluster(instance_id)
        snapshot_id = str(cluster_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_cluster_snapshot(
                DBClusterIdentifier=cluster_id,
                DBClusterSnapshotIdentifier=snapshot_id
                )
            status = response['DBClusterSnapshot']['Status']
            # return response['DBClusterSnapshot']['DBClusterSnapshotArn']
            click.secho(response['DBClusterSnapshot']
                        ['DBClusterSnapshotArn'], fg='green')
        except ClientError as error:
            click.echo(error)
    else:
        snapshot_id = str(instance_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_snapshot(
                DBInstanceIdentifier=instance_id,
                DBSnapshotIdentifier=snapshot_id
                )
            status = response['DBSnapshot']['Status']
            progress = response['DBSnapshot']['PercentProgress']
            # return response['DBSnapshot']['DBSnapshotArn']
            while True:
                click.echo(progress)
                if status == 'available':
                    break

            click.secho(response['DBSnapshot']
                        ['DBSnapshotArn'], fg='green')
        except ClientError as error:
            click.echo(error)


if __name__ == '__main__':
    snapshot()
    import doctest
    doctest.testmod()
