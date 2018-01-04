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


def snapshot(instance_id):
    """This command will create point in time snapshot.
    """
    now = datetime.now()
    if query_db_cluster(instance_id):
        cluster_id = query_db_cluster(instance_id)
        snapshot_id = str(cluster_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_cluster_snapshot(
                DBClusterSnapshotIdentifier=snapshot_id,
                DBClusterIdentifier=cluster_id
                )
            # click.secho(response['DBClusterSnapshot']
            #             ['DBClusterSnapshotArn'], fg='green')
            status = response['DBClusterSnapshot']['Status']
            with click.progressbar(status) as state:
                while state == 'creating':
                    click.echo('checking to see if the progress bar is there')
                    if state == 'available':
                        return response['DBClusterSnapshot']['DBClusterSnapshotArn']
        except ClientError as error:
            click.secho(error, fg='red')
    else:
        snapshot_id = str(snapshot_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_snapshot(
                DBSnapshotIdentifier=snapshot_id,
                DBInstanceIdentifier=instance_id
                )
            # click.secho(response['DBSnapshot']
            #             ['DBSnapshotArn'], fg='green')
            status = response['DBSnapshot']['Status']
            with click.progressbar(status) as state:
                while state == 'creating':
                    click.echo('checking to see if the progress bar is there')
                    if state == 'available':
                        return response['DBSnapshot']['DBSnapshotArn']
        except ClientError as error:
            click.secho(error, fg='red')


@click.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
@click.option('--new_db_id', prompt=True,
              help='The ID of the new DB.')
def deploy(instance_id, new_db_id):
    """
    Deploying new cluster or instance from latest snapshot.
    """
    snapshot_arn = snapshot(instance_id)
    if query_db_cluster(instance_id):
        try:
            response = RDS.restore_db_cluster_from_snapshot(
                DBClusterIdentifier=new_db_id,
                SnapshotIdentifier=snapshot_arn
                )
            click.secho(response['DBCluster']['DBClusterArn'], fg='green')
        except ClientError as error:
            click.secho(error, fg='red')
    else:
        try:
            response = RDS.restore_db_instance_from_db_snapshot(
                DBInstanceIdentifier=new_db_id,
                DBSnapshotIdentifier=snapshot_arn
                )
            click.secho(response['DBInstance']['DBInstanceArn'], fg='green')
        except ClientError as error:
            click.secho(error, fg='red')


# if __name__ == '__main__':
#     deploy()
#     import doctest
#     doctest.testmod()
