#!/usr/bin/env python

"""
Example Usage:

    ./list-all-parameters.py
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

    parser = argparse.ArgumentParser(description='List All Parameters')
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def get_value(client, name, encrypted=True):
    try:
        result = client.get_parameter(Name=name, WithDecryption=encrypted)
    except ClientError as e:
        #print(e.response['Error']['Code'])
        return None
    except Exception as e:
        #print(e.response['Error']['Code'])
        return None

    type = result['Parameter']['Type']
    value = result['Parameter']['Value']
    if type == 'StringList':
        value = value.split(',')

    return SSMValue(name, value, type)


def query_api(client, arg, next_token=None):
    """
    Query the API
    """
    results = []

    try:
        if next_token:
            query_result = client.describe_parameters(NextToken=next_token)
        else:
            query_result = client.describe_parameters()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'ResponseMetadata' in query_result:
            if 'HTTPStatusCode' in query_result['ResponseMetadata']:
                if query_result['ResponseMetadata']['HTTPStatusCode'] == 200:
                    if 'NextToken' in query_result:
                        results.extend(query_api(client, arg, next_token=query_result['NextToken']))
                    else:
                        results.extend(query_result['Parameters'])

    for parts in results:
        value = None
        value_results = get_value(client, parts['Name']) if parts['Type'] == 'SecureString' else get_value(client, parts['Name'], False)
        if value_results is not None:
            value = value_results.value
        parts['Value'] = value

    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Name',
                         'Value',
                         'Type',
                         'Key ID',
                         'Last Modified',
                         'By',
                         'Version',
                        ]

    for parts in results:
        table.add_row([
                       parts['Name'],
                       parts['Value'],
                       parts['Type'],
                       parts['KeyId'] if 'KeyId' in parts else '',
                       parts['LastModifiedDate'] if 'LastModifiedDate' in parts else 'Unknown',
                       parts['LastModifiedUser'] if 'LastModifiedUser' in parts else 'Unknown',
                       parts['Version'] if 'Version' in parts else '',
                      ])

    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
