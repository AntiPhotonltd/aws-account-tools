#!/usr/bin/env python

"""
This is a simple script for listing all EC2 Key Pairs

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

    if args.region:
        client = boto3.client('ec2', region_name=args.region)
    else:
        client = boto3.client('ec2')

    key_pairs = get_key_pairs(client)
    display_key_pairs(key_pairs)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List Key Pairs')
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def get_key_pairs(client):
    """
    Query a list of current key pairs
    """

    key_pairs = []

    try:
        response = client.describe_key_pairs()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'KeyPairs' in response:
            for kp in response['KeyPairs']:
                key_pairs.append({
                                  'KeyName': kp['KeyName'] if 'KeyName' in kp else unknown_string,
                                  'KeyFingerprint': kp['KeyFingerprint'] if 'KeyFingerprint' in kp else unknown_string
                                 })
    return key_pairs


def display_key_pairs(key_pairs):
    """
    Display all the key pairs
    """

    table = PrettyTable()

    table.field_names = [
                         'Key Name',
                         'Fingerprint'
                        ]

    for kp in key_pairs:
        table.add_row([
                       kp['KeyName'],
                       kp['KeyFingerprint'],
                      ])

    table.sortby = 'Key Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
