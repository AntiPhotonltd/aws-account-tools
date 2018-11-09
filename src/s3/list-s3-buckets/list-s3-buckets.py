#!/usr/bin/env python

"""
This is a simple script for listing all S3 buckets

Example Usage:

    ./list-s3-buckets.py
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

    client = boto3.client('s3')

    s3_buckets = get_s3_buckets(client)
    display_s3_buckets(s3_buckets)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List S3 Buckets')

    return parser


def get_s3_buckets(client):
    """
    Query a list of current buckets
    """

    s3_buckets = []

    try:
        response = client.list_buckets()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Buckets' in response:
            for bucket in response['Buckets']:
                s3_buckets.append({
                                   'Name': bucket['Name'] if 'Name' in bucket else unknown_string,
                                   'CreationDate': bucket['CreationDate'] if 'CreationDate' in bucket else unknown_string,
                                  })
    return s3_buckets


def display_s3_buckets(s3_buckets):
    """
    Display all the buckets
    """

    table = PrettyTable()

    table.field_names = [
                         'Name',
                         'Date Created'
                        ]

    for bucket in s3_buckets:
        table.add_row([
                       bucket['Name'],
                       bucket['CreationDate']
                      ])

    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
