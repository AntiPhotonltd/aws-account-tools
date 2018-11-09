#!/usr/bin/env python

"""
Example Usage:

    ./list-ebs-volumes.py
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

    parser = argparse.ArgumentParser(description='List EBS Volumes')
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


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_volumes()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Volumes' in response:
            for parts in response['Volumes']:
                results.append({
                                'Name': get_tag_value(parts['Tags'], 'Name') if 'Tags' in parts else unknown_string,
                                'AvailabilityZone': parts['AvailabilityZone'] if 'AvailabilityZone' in parts else unknown_string,
                                'Encrypted': parts['Encrypted'] if 'Encrypted' in parts else unknown_string,
                                'VolumeId': parts['VolumeId'] if 'VolumeId' in parts else unknown_string,
                                'State': parts['State'] if 'State' in parts else unknown_string,
                                'InstanceId': parts['Attachments'][0]['InstanceId'] if 'InstanceId' in parts['Attachments'][0] else empty_string,
                                'Size': parts['Size'] if 'Size' in parts else unknown_string,
                                'CreateTime': parts['CreateTime'] if 'CreateTime' in parts else unknown_string,
                               })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Name',
                         'Availability Zone',
                         'Encrypted',
                         'VolumeId',
                         'State',
                         'Attached To',
                         'Size',
                         'Time Created',
                        ]

    for parts in results:
        table.add_row([
                       parts['Name'],
                       parts['AvailabilityZone'],
                       parts['Encrypted'],
                       parts['VolumeId'],
                       parts['State'],
                       parts['InstanceId'],
                       '%s GB' % parts['Size'],
                       parts['CreateTime'],
                      ])



    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
