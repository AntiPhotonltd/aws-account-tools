#!/usr/bin/env python

"""
This is a simple script for listing all available RDS instances.

Example Usage:

    ./list-all-rds-instances.py
"""

from __future__ import print_function

import argparse
import boto3
import requests
import sys

from botocore.exceptions import ClientError, EndpointConnectionError
from prettytable import PrettyTable

empty_string = ''
unknown_string = 'Unknown'
unknown_version = '0.0.0'
unknown_int = 0


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

    try:
        response = client.describe_db_instances()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'DBInstances' in response:
            for instance in response['DBInstances']:
                if 'AvailabilityZone' in instance:
                    if 'SecondaryAvailabilityZone' in instance:
                        AZS = '%s & %s' % (instance['AvailabilityZone'], instance['SecondaryAvailabilityZone'])
                    else:
                        AZS = instance['AvailabilityZone']
                else:
                    AZS = unknown_string

                rds_instances.append({
                                      'InstanceName': instance['DBInstanceIdentifier'] if 'DBInstanceIdentifier' in instance else unknown_string,
                                      'InstanceClass': instance['DBInstanceClass'] if 'DBInstanceClass' in instance else unknown_string,
                                      'Status': instance['DBInstanceStatus'] if 'Status' in instance else unknown_string,
                                      'AvailabilityZone': AZS,
                                      'PubliclyAccessible': instance['PubliclyAccessible'] if 'PubliclyAccessible' in instance else unknown_string,
                                      'AllocatedStorage': instance['AllocatedStorage'] if 'AllocatedStorage' in instance else unknown_string,
                                      'StorageEncrypted': instance['StorageEncrypted'] if 'StorageEncrypted' in instance else unknown_string,
                                      'Engine': instance['Engine'] if 'Engine' in instance else unknown_string,
                                      'EngineVersion': instance['EngineVersion'] if 'EngineVersion' in instance else unknown_string,
                                      'PerformanceInsightsEnabled': instance['PerformanceInsightsEnabled'] if 'PerformanceInsightsEnabled' in instance else unknown_string,
                                     })
    return rds_instances


def display_rds_instances(rds_instances):
    """
    Display all the RDS instances
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
                         'Engine Version',
                         'Performance Insights'
                        ]

    for instance in rds_instances:
        table.add_row([
                       instance['InstanceName'],
                       instance['InstanceClass'],
                       instance['Status'],
                       instance['AvailabilityZone'],
                       instance['PubliclyAccessible'],
                       '%s GB' % instance['AllocatedStorage'],
                       instance['StorageEncrypted'],
                       instance['Engine'],
                       instance['EngineVersion'],
                       instance['PerformanceInsightsEnabled']
                      ])

    table.sortby = 'Instance Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
