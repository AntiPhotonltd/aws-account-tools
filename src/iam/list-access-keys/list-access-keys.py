#!/usr/bin/env python

"""
This is a simple script for listing all access keys from IAM

Example Usage:

    ./list-all-users.py
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

    access_keys = get_all_access_keys(client)
    display_all_access_keys(access_keys)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List all Access Keys')

    return parser


def get_all_access_keys(client):
    """
    Query a list of current access keys
    """

    access_keys = []

    try:
        response = client.list_access_keys()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'AccessKeyMetadata' in response:
            for key in response['AccessKeyMetadata']:
                access_keys.append({
                                    'UserName': key['UserName'] if 'UserName' in key else unknown_string,
                                    'Status': key['Status'] if 'Status' in key else unknown_string,
                                    'CreateDate': key['CreateDate'] if 'CreateDate' in key else unknown_string,
                                    'AccessKeyId': key['AccessKeyId'] if 'AccessKeyId' in key else unknown_string,
                                   })
    return access_keys


def display_all_access_keys(access_keys):
    """
    Display all the users
    """

    table = PrettyTable()

    table.field_names = [
                         'UserName',
                         'Status',
                         'Date Created',
                         'Access Key ID'
                        ]

    for key in access_keys:
        table.add_row([
                       key['UserName'],
                       key['Status'],
                       key['CreateDate'],
                       key['AccessKeyId'],
                      ])

    table.sortby = 'UserName'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
