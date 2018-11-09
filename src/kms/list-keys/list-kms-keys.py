#!/usr/bin/env python

"""
This is a simple script for listing all KSM keys

Example Usage:

    ./list-kms-keys.py
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
        client = boto3.client('kms', region_name=args.region)
    else:
        client = boto3.client('kms')

    kms_keys = get_kms_keys(client)
    display_kms_keys(kms_keys)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List KMS Keys')
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def get_kms_keys(client):
    """
    Query a list of KMS keys
    """

    kms_keys = []

    try:
        response = client.list_keys()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Keys' in response:
            for key in response['Keys']:
                kms_keys.append({
                                 'KeyId': key['KeyId'] if 'KeyId' in key else unknown_string,
                                 'KeyArn': key['KeyArn'] if 'KeyArn' in key else unknown_string,
                                })
    return kms_keys


def display_kms_keys(kms_keys):
    """
    Display all the KMS keys
    """

    table = PrettyTable()

    table.field_names = [
                         'Key ID',
                         'Key ARN'
                        ]

    for key in kms_keys:
        table.add_row([
                       key['KeyId'],
                       key['KeyArn']
                      ])

    table.sortby = 'Key ID'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
