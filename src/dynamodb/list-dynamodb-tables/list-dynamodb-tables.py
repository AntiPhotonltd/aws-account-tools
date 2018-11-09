#!/usr/bin/env python

"""
Example Usage:

    ./list-dynamodb-tables.py
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
        client = boto3.client('dynamodb', region_name=args.region)
    else:
        client = boto3.client('dynamodb')

    results = query_api(client, args)
    display_results(results)


def make_parser():
    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List Dynamodb Tables')

    parser.add_argument('-r', '--region', help='The aws region')
    return parser


def get_table_details(client, name):
    """
    Get details about a specific table
    """

    results = {}

    try:
        response = client.describe_table(TableName=name)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Table' in response:
            parts = response['Table']
            results['TableStatus'] = parts['TableStatus'] if 'TableStatus' in parts else unknown_string
            results['ItemCount'] = parts['ItemCount'] if 'ItemCount' in parts else unknown_int
            results['TableId'] = parts['TableId'] if 'TableId' in parts else unknown_int
            results['TableSizeBytes'] = parts['TableSizeBytes'] if 'TableSizeBytes' in parts else unknown_int

    return results


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.list_tables()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'TableNames' in response:
            for parts in response['TableNames']:
                details = get_table_details(client, parts)
                results.append({
                                'TableName': parts,
                                'TableId': details['TableId'],
                                'TableStatus': details['TableStatus'],
                                'ItemCount': details['ItemCount'],
                                'TableSizeBytes': details['TableSizeBytes'],
                               })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Table Name',
                         'Table ID',
                         'Table Status',
                         'Item Count',
                         'Table Size (Bytes)',
                        ]

    for parts in results:
        table.add_row([
                       parts['TableName'],
                       parts['TableId'],
                       parts['TableStatus'],
                       parts['ItemCount'],
                       parts['TableSizeBytes'],
                      ])

    table.sortby = 'Table Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
