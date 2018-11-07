#!/usr/bin/env python

"""
This is a simple script for listing all users from AIM

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

    all_users = get_all_users(client)
    display_all_users(all_users)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List all Users')

    return parser


def get_all_users(client):
    """
    Query a list of current local users from IAM
    """

    all_users = []

    try:
        response = client.list_users()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Users' in response:
            for user in response['Users']:
                all_users.append({
                                  'UserName': user['UserName'] if 'UserName' in user else unknown_string,
                                  'Path': user['Path'] if 'Path' in user else unknown_string,
                                  'CreateDate': user['CreateDate'] if 'CreateDate' in user else unknown_string,
                                  'UserId': user['UserId'] if 'UserId' in user else unknown_string,
                                  'Arn': user['Arn'] if 'Arn' in user else unknown_string,
                                  'PasswordLastUsed': user['PasswordLastUsed'] if 'PasswordLastUsed' in user else empty_string,
                                 })
    return all_users


def display_all_users(all_users):
    """
    Display all the users
    """

    table = PrettyTable()

    table.field_names = [
                         'UserName',
                         'Path',
                         'Date Created',
                         'User Id',
                         'Arn',
                         'Password Last Used'
                        ]

    for user in all_users:
        table.add_row([
                       user['UserName'],
                       user['Path'],
                       user['CreateDate'],
                       user['UserId'],
                       user['Arn'],
                       user['PasswordLastUsed']
                      ])

    table.sortby = 'UserName'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
