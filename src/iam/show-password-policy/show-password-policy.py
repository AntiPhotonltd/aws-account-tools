#!/usr/bin/env python

"""
Example Usage:

    ./show-password-policy.py
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

    parser = argparse.ArgumentParser(description='Show Password Policy')

    return parser


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.get_account_password_policy()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'PasswordPolicy' in response:
            for parts in response['PasswordPolicy']:
                results.append({
                                'Attribute': parts,
                                'Value': response['PasswordPolicy'].get(parts),
                               })
    return results


def display_results(results):
    """
    Display  the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Attribute',
                         'Value',
                        ]

    for parts in results:
        table.add_row([
                       parts['Attribute'],
                       parts['Value'],
                      ])

    table.sortby = 'Attribute'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
