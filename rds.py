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
    """Querying whether DB is Clustered or not
    """
    try:
        response = RDS.describe_db_instances(
            DBInstanceIdentifier=instance_id
            )
        return response['DBInstances'][0]['DBClusterIdentifier']
    except KeyError:
        return False


def snapshot(instance_id):
    """This function is essentially the same as the clone function below
    however has a return statement to use with the restore function
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
            return response['DBClusterSnapshot']['DBClusterSnapshotArn']
        except ClientError as error:
            click.echo(error)

    else:
        snapshot_id = str(instance_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_snapshot(
                DBInstanceIdentifier=instance_id,
                DBSnapshotIdentifier=snapshot_id
                )
            return response['DBSnapshot']['DBSnapshotArn']
        except ClientError as error:
            click.echo(error)


@click.group()
def cli():
    """Command Line Tool to clone and restore RDS DB instance
    or cluster for Blue-Green deployments.  Please the sub commands
    below.  You can also use the options below to get more help.
    """
    pass


@cli.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
def clone(instance_id):
    """Prints the ARN of the snapshot to stdout.
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
            click.secho(response['DBSnapshot']
                        ['DBSnapshotArn'], fg='green')
        except ClientError as error:
            click.echo(error)


@cli.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
@click.option('--new_db_id', prompt=True,
              help='The ID of the new DB.')
def deploy(instance_id, new_db_id):
    """Deploy new DB from snapshot and print ARN to stdout.
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
#     cli()
#     import doctest
#     doctest.testmod()
