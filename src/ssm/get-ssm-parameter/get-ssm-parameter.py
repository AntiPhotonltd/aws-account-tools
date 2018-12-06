#!/usr/bin/env python

"""
Example Usage:

    ./get-ssm-parameter.py
"""

from __future__ import print_function

import argparse
import boto3
import collections
import requests
import sys

from botocore.exceptions import ClientError, EndpointConnectionError
from prettytable import PrettyTable

empty_string = ''
unknown_string = 'Unknown'
unknown_version = '0.0.0'
unknown_int = 0

SSMValue = collections.namedtuple('SSMValue', 'name, value, type')


def main(cmdline=None):

    """
    The main function. This takes the command line arguments provided and parse them.
    """

    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.region:
        client = boto3.client('ssm', region_name=args.region)
    else:
        client = boto3.client('ssm')

    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Get SSM Parameter')
    parser.add_argument('-n', '--name', help='The name of the parameter to lookup', required=True)
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def query_api(client, arg):
    """
    Query the API
    """
    try:
        result = client.get_parameter(Name=arg.name, WithDecryption=True)
    except ClientError as e:
        print(e.response['Error']['Code'])
        return None
    except Exception as e:
        print(e.response['Error']['Code'])
        return None

    type = result['Parameter']['Type']
    value = result['Parameter']['Value']
    if type == 'StringList':
        value = value.split(',')

    return SSMValue(arg.name, value, type)


def display_results(results):
    """
    Display the results
    """

    if results is None:
        print("Failed to find Parameter")
    else:
        print('Name: %s' % results.name)
        print('Value: %s' % results.value)
        print('Type: %s' % results.type)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
