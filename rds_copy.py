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

__version__ = "0.1"

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
            newest = max(snapshots['DBClusterSnapshots'].itervalues(),
                         key=lambda latest: latest['SnapshotCreateTime']
                         if isinstance(latest, datetime) else datetime.min)
            return newest
        except ClientError as error:
            print(error)
    else:
        try:
            snapshots = RDS.describe_db_snapshots(
                DBInstanceIdentifier=instanceid
                )
            newest = max(snapshots['DBSnapshots'].itervalues(),
                         key=lambda latest: latest['SnapshotCreateTime'] if
                         isinstance(latest, datetime) else datetime.min)
            return newest
        except ClientError as error:
            print(error)


def clone(instanceid, newid):
    """
    This command will restore RDS DB from latest snapshot.
    """
    if query_db_cluster(instanceid):
        clusterid = query_db_cluster(instanceid)
        try:
            response = RDS.copy_db_cluster_snapshot(
                SourceDBClusterSnapshotIdentifier=clusterid,
                TargetDBClusterSnapshotIdentifier=newid
                )
            return response['DBClusterSnapshot'][0]['Status']
        except ClientError as error:
            print(error)
    else:
        try:
            response = RDS.copy_db_snapshot(
                SourceDBSnapshotIdentifier=instanceid,
                TargetDBSnapshotIdentifier=newid
                )
            return response['DBSnapshot'][0]['Status']
        except ClientError as error:
            print(error)


if __name__ == '__main__':
    clone(INSTANCEID, NEWID)
    import doctest
    doctest.testmod()
