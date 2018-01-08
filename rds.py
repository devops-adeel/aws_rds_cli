#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File:           rds_copy.py
Author:         Adeel Ahmad
Description:    Python Script to copy snapshot and deploy
"""

from datetime import datetime
from botocore.exceptions import ClientError
import boto3
import click
from utils import query_db_cluster
from __version__ import __version__


RDS = boto3.client('rds')


@click.group()
@click.version_option(prog_name='rds', version=__version__)
def cli():
    """Command Line Tool to clone and restore RDS DB instance
    or cluster for Blue-Green deployments.  Please the sub commands
    below.  You can also use the options below to get more help.

    NOTE: Please ensure the RDS instance ID is stored in your environment
    variable as DBINSTANCEID
    """
    pass


@cli.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='Retrieved from ENV')
def clone(instance_id):
    """Prints the ARN of the snapshot to stdout.

    NOTE: Please ensure the RDS instance ID is stored in your environment
    variable as DBINSTANCEID
    """
    now = datetime.now()
    if isinstance(query_db_cluster(instance_id), str):
        cluster_id = query_db_cluster(instance_id)
        snapshot_id = str(cluster_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_cluster_snapshot(
                DBClusterIdentifier=cluster_id,
                DBClusterSnapshotIdentifier=snapshot_id
                )
            clone_arn = response['DBClusterSnapshot']['DBClusterSnapshotArn']
            click.secho(clone_arn, fg='green')
        except ClientError as error:
            click.echo(error)

    else:
        snapshot_id = str(instance_id) + now.strftime("%Y-%m-%d-%H-%M-%S")
        try:
            response = RDS.create_db_snapshot(
                DBInstanceIdentifier=instance_id,
                DBSnapshotIdentifier=snapshot_id
                )
            clone_arn = response['DBSnapshot']['DBSnapshotArn']
            click.secho(clone_arn, fg='green')
        except ClientError as error:
            click.echo(error)


@cli.command()
@click.option('--instance_id', envvar='DBINSTANCEID',
              help='The ID of the DB Instance.')
@click.option('--new_db_id', prompt=True,
              help='The ID of the new DB.')
def deploy(instance_id, new_db_id):
    """Deploy new DB from snapshot and print ARN to stdout.

    NOTE: Please ensure the RDS instance ID is stored in your environment
    variable as DBINSTANCEID
    """
    if isinstance(query_db_cluster(instance_id), str):
        cluster_id = query_db_cluster(instance_id)
        try:
            response = RDS.restore_db_cluster_to_point_in_time(
                DBClusterIdentifier=new_db_id,
                SourceDBClusterIdentifier=cluster_id,
                UseLatestRestorableTime=True
                )
            click.secho(response['DBCluster']['DBClusterArn'], fg='green')
        except ClientError as error:
            click.echo(error)
    else:
        db_subnet = query_db_cluster(instance_id)
        try:
            response = RDS.restore_db_instance_to_point_in_time(
                SourceDBInstanceIdentifier=instance_id,
                TargetDBInstanceIdentifier=new_db_id,
                UseLatestRestorableTime=True,
                PubliclyAccessible=False,
                DBSubnetGroupName=db_subnet[1]
                )
            click.secho(response['DBInstance']['DBInstanceArn'], fg='green')
        except ClientError as error:
            click.echo(error)
