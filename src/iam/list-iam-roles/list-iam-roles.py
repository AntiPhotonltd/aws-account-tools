#!/usr/bin/env python

"""
Example Usage:

    ./list-iam-roles.py
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

    client = boto3.client('iam')

    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List IAM Roles')

    return parser


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.list_roles()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Roles' in response:
            for role in response['Roles']:
                results.append({
                                'RoleName': role['RoleName'] if 'RoleName' in role else unknown_string,
                                'RoleId': role['RoleId'] if 'RoleId' in role else unknown_string,
                                'Path': role['Path'] if 'Path' in role else unknown_string,
                                'Arn': role['Arn'] if 'Arn' in role else unknown_string,
                                'CreateDate': role['CreateDate'] if 'CreateDate' in role else unknown_string,
                               })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'RoleName',
                         'RoleId',
                         'Path',
                         'Arn',
                         'Date Created'
                        ]

    for item in results:
        table.add_row([
                       item['RoleName'],
                       item['RoleId'],
                       item['Path'],
                       item['Arn'],
                       item['CreateDate']
                      ])

    table.sortby = 'RoleName'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
