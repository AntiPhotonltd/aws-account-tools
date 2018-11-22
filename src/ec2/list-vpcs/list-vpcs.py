#!/usr/bin/env python

"""
Example Usage:

    ./list-vpcs.py
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

    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List VPCs')
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def get_tag_value(tags, key):
    """
    Process tags and look for a Name
    """

    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

    return unknown_string


def get_tags(tags):
    """
      Return the tags a string.
    """

    tag_str = ''

    sorted_tags = sorted(tags, key=lambda k: k['Key'], reverse=False)
    for tag in sorted_tags:
        tag_str += '%s = %s\n' % (tag['Key'], tag['Value'])
    tag_str = tag_str.rstrip('\n')

    return tag_str


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_vpcs()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Vpcs' in response:
            for parts in response['Vpcs']:
                tags = get_tags(parts['Tags']) if 'Tags' in parts else unknown_string
                results.append({
                                'Name': get_tag_value(parts['Tags'], 'Name') if 'Tags' in parts else unknown_string,
                                'CidrBlock': parts['CidrBlock'] if 'CidrBlock' in parts else unknown_string,
                                'VpcId': parts['VpcId'] if 'VpcId' in parts else unknown_string,
                                'State': parts['State'] if 'State' in parts else unknown_string,
                                'Tags': tags,
                               })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Name',
                         'CidrBlock',
                         'VpcId',
                         'State',
                         'Tags',
                        ]

    for parts in results:
        table.add_row([
                       parts['Name'],
                       parts['CidrBlock'],
                       parts['VpcId'],
                       parts['State'],
                       parts['Tags'],
                      ])

    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
