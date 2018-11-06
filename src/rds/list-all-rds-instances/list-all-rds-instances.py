#!/usr/bin/env python

"""
This is a simple script for checking if there are upgrades available for your RDS.

Example Usage:

    ./check-all-rds-instances.py
"""

from __future__ import print_function

import argparse
import boto3
import requests
import sys

from prettytable import PrettyTable


def main(cmdline=None):

    """
    The main function. This takes the command line arguments provided and parse them.
    """

    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.region:
        client = boto3.client('rds', region_name=args.region)
    else:
        client = boto3.client('rds')

    rds_instances = get_all_rds_instances(client)

    display_rds_instances(rds_instances)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List all RDS Instances')

    parser.add_argument('-r', '--region', help='The aws region')
    return parser


def get_all_rds_instances(client):
    """
    Query a list of current RDS instances and their details
    """

    rds_instances = []

    response = client.describe_db_instances()

    if 'DBInstances' in response:
        for instance in response['DBInstances']:
            if 'SecondaryAvailabilityZone' in instance:
                    AZS = '%s & %s' % (instance['AvailabilityZone'], instance['SecondaryAvailabilityZone'])
            else:
                    AZS = instance['AvailabilityZone']

            rds_instances.append({
                                  'InstanceName': instance['DBInstanceIdentifier'],
                                  'InstanceClass': instance['DBInstanceClass'],
                                  'Status': instance['DBInstanceStatus'],
                                  'AvailabilityZone': AZS,
                                  'PubliclyAccessible': instance['PubliclyAccessible'],
                                  'AllocatedStorage': instance['AllocatedStorage'],
                                  'StorageEncrypted': instance['StorageEncrypted'],
                                  'Engine': instance['Engine'],
                                  'EngineVersion': instance['EngineVersion'],
                                 })

    return rds_instances


def display_rds_instances(rds_instances):
    """
    Display the databases which can be upgraded (or all if flat is set)
    """

    table = PrettyTable()

    table.field_names = [
                         'Instance Name',
                         'Instance Class',
                         'Status',
                         'Availability Zone(s)',
                         'Publicly Accessible',
                         'Allocated Storage',
                         'Storage Encrypted',
                         'Engine',
                         'Engine Version'
                        ]

    for instance in rds_instances:
        table.add_row([
                       instance['InstanceName'],
                       instance['InstanceClass'],
                       instance['Status'],
                       instance['AvailabilityZone'],
                       instance['PubliclyAccessible'],
                       '%sGB' % instance['AllocatedStorage'],
                       instance['StorageEncrypted'],
                       instance['Engine'],
                       instance['EngineVersion']
                      ])

    table.sortby = 'Instance Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
