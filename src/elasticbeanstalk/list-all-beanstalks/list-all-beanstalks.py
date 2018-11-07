#!/usr/bin/env python

"""
This is a simple script for liting all available beanstalks.

Example Usage:

    ./list-all-beanstalks.py
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

    all_beanstalks = get_all_beanstalks(client)
    display_all_beanstalks(all_beanstalks)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List all Beanstalks')

    parser.add_argument('-r', '--region', help='The aws region')
    return parser


def get_all_beanstalks(client):
    """
    Query a list of current beanstalks and their details
    """

    beanstalks = []

    try:
        response = client.describe_environments()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Environments' in response and len(response['Environments']) > 0:
            for result in response['Environments']:
                beanstalks.append({
                                   'ApplicationName': result['ApplicationName'] if 'ApplicationName' in result else unknown_string,
                                   'EnvironmentName': result['EnvironmentName'] if 'EnvironmentName' in result else unknown_string,
                                   'SolutionStackName': result['SolutionStackName'] if 'SolutionStackName' in result else unknown_string,
                                   'VersionLabel': result['VersionLabel'] if 'VersionLabel' in result else empty_string,
                                   'Status': result['Status'] if 'Status' in result else unknown_string,
                                   'Health': result['Health'] if 'Health' in result else unknown_string,
                                   'HealthStatus': result['HealthStatus'] if 'HealthStatus' in result else unknown_string,
                                  })

    return beanstalks


def display_all_beanstalks(all_beanstalks):
    """
    Display thr beanstalk information
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

    for instance in all_beanstalks:
        table.add_row([
                       instance['ApplicationName'],
                       instance['EnvironmentName'],
                       instance['SolutionStackName'],
                       instance['VersionLabel'],
                       instance['Status'],
                       instance['Health'],
                       instance['HealthStatus'],
                      ])

    table.sortby = 'Application'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
