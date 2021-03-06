#!/usr/bin/env python

"""
Example Usage:

    ./list-ec2-instances.py
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

    parser = argparse.ArgumentParser(description='List EC2 Instances')
    parser.add_argument('-a', '--all', help='Show all instances', action='store_true')
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


def query_api(client, arg):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_instances()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Reservations' in response:
            reservations = response['Reservations']
            for reservation in reservations:
                if 'Instances' in reservation:
                    for parts in reservation['Instances']:
                        if parts['State']['Name'] == 'running' or args.all:
                            results.append({
                                            'Name': get_tag_value(parts['Tags'], 'Name') if 'Tags' in parts else unknown_string,
                                            'InstanceId': parts['InstanceId'] if 'InstanceId' in parts else unknown_string,
                                            'InstanceType': parts['InstanceType'] if 'InstanceType' in parts else unknown_string,
                                            'PrivateIpAddress': parts['PrivateIpAddress'] if 'PrivateIpAddress' in parts else unknown_string,
                                            'AvailabilityZone': parts['Placement']['AvailabilityZone'] if 'AvailabilityZone' in parts['Placement'] else unknown_string,
                                            'State': parts['State']['Name'] if 'Name' in parts['State'] else unknown_string,
                                            'VpcId': parts['VpcId'] if 'VpcId' in parts else unknown_string,
                                            'KeyName': parts['KeyName'] if 'KeyName' in parts else unknown_string,
                                           })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Name',
                         'State',
                         'Availability Zone',
                         'Instance ID',
                         'Instance Type',
                         'Private IP',
                         'VPC ID',
                         'SSH Key Name',
                        ]

    for parts in results:
        table.add_row([
                       parts['Name'],
                       parts['State'],
                       parts['AvailabilityZone'],
                       parts['InstanceId'],
                       parts['InstanceType'],
                       parts['PrivateIpAddress'],
                       parts['VpcId'],
                       parts['KeyName'],
                      ])

    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
