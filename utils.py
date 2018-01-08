#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File:           utils.py
Author:         Adeel Ahmad
Description:    Python Script contains util functions to call from main.
"""

import boto3

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
        db_subnet = response['DBInstances'][0]['DBSubnetGroup']['DBSubnetGroupName']
        return [False, db_subnet]
