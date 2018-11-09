#!/usr/bin/env python

"""
Example Usage:

    ./list-rds-instances.py
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

    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List RDS Instances')

    parser.add_argument('-r', '--region', help='The aws region')
    return parser


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_db_instances()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'DBInstances' in response:
            for parts in response['DBInstances']:
                if 'AvailabilityZone' in parts:
                    if 'SecondaryAvailabilityZone' in parts:
                        AZS = '%s & %s' % (parts['AvailabilityZone'], parts['SecondaryAvailabilityZone'])
                    else:
                        AZS = parts['AvailabilityZone']
                else:
                    AZS = unknown_string

                results.append({
                                'InstanceName': parts['DBInstanceIdentifier'] if 'DBInstanceIdentifier' in parts else unknown_string,
                                'InstanceClass': parts['DBInstanceClass'] if 'DBInstanceClass' in parts else unknown_string,
                                'Status': parts['DBInstanceStatus'] if 'DBInstanceStatus' in parts else unknown_string,
                                'AvailabilityZone': AZS,
                                'PubliclyAccessible': parts['PubliclyAccessible'] if 'PubliclyAccessible' in parts else unknown_string,
                                'AllocatedStorage': parts['AllocatedStorage'] if 'AllocatedStorage' in parts else unknown_string,
                                'StorageEncrypted': parts['StorageEncrypted'] if 'StorageEncrypted' in parts else unknown_string,
                                'Engine': parts['Engine'] if 'Engine' in parts else unknown_string,
                                'EngineVersion': parts['EngineVersion'] if 'EngineVersion' in parts else unknown_string,
                                'PerformanceInsightsEnabled': parts['PerformanceInsightsEnabled'] if 'PerformanceInsightsEnabled' in parts else unknown_string,
                               })
    return results


def display_results(results):
    """
    Display the results
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

    for parts in results:
        table.add_row([
                       parts['InstanceName'],
                       parts['InstanceClass'],
                       parts['Status'],
                       parts['AvailabilityZone'],
                       parts['PubliclyAccessible'],
                       '%s GB' % parts['AllocatedStorage'],
                       parts['StorageEncrypted'],
                       parts['Engine'],
                       parts['EngineVersion'],
                       parts['PerformanceInsightsEnabled']
                      ])

    table.sortby = 'Instance Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
