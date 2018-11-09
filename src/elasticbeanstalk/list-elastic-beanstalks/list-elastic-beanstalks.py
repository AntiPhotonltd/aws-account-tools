#!/usr/bin/env python

"""
Example Usage:

    ./list-elastic-beanstalks.py
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
        client = boto3.client('elasticbeanstalk', region_name=args.region)
    else:
        client = boto3.client('elasticbeanstalk')

    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List Elastic Beanstalks')

    parser.add_argument('-r', '--region', help='The aws region')
    return parser


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_environments()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Environments' in response and len(response['Environments']) > 0:
            for parts in response['Environments']:
                results.append({
                                'ApplicationName': parts['ApplicationName'] if 'ApplicationName' in parts else unknown_string,
                                'EnvironmentName': parts['EnvironmentName'] if 'EnvironmentName' in parts else unknown_string,
                                'SolutionStackName': parts['SolutionStackName'] if 'SolutionStackName' in parts else unknown_string,
                                'VersionLabel': parts['VersionLabel'] if 'VersionLabel' in parts else empty_string,
                                'Status': parts['Status'] if 'Status' in parts else unknown_string,
                                'Health': parts['Health'] if 'Health' in parts else unknown_string,
                                'HealthStatus': parts['HealthStatus'] if 'HealthStatus' in parts else unknown_string,
                               })

    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Application',
                         'Environment',
                         'Solution Stack',
                         'Version Label',
                         'Status',
                         'Health',
                         'HealthStatus'
                        ]

    for parts in results:
        table.add_row([
                       parts['ApplicationName'],
                       parts['EnvironmentName'],
                       parts['SolutionStackName'],
                       parts['VersionLabel'],
                       parts['Status'],
                       parts['Health'],
                       parts['HealthStatus'],
                      ])

    table.sortby = 'Application'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
