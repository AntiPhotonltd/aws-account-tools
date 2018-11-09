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
vpc_cache = []


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

    load_vpcs_into_cache(client)
    results = query_api(client, args)
    display_results(results)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List VPC Peers')
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


def get_vpc_by_id(vpcid):
    """
    Process tags and look for a Name
    """

    for vpc in vpc_cache:
        if vpc['VpcId'] == vpcid:
            return vpc['Name']

    return empty_string


def load_vpcs_into_cache(client):
    """
    Load the VPC details into a cache
    """

    try:
        response = client.describe_vpcs()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Vpcs' in response:
            for parts in response['Vpcs']:
                vpc_cache.append({
                                'Name': get_tag_value(parts['Tags'], 'Name') if 'Tags' in parts else unknown_string,
                                'VpcId': parts['VpcId'] if 'VpcId' in parts else unknown_string,
                               })


def query_api(client, args):
    """
    Query the API
    """

    results = []

    try:
        response = client.describe_vpc_peering_connections()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'VpcPeeringConnections' in response:
            for parts in response['VpcPeeringConnections']:
                results.append({
                                'A_Name': get_vpc_by_id(parts['AccepterVpcInfo']['VpcId']) if 'VpcId' in parts['AccepterVpcInfo'] else unknown_string,
                                'A_VpcId': parts['AccepterVpcInfo']['VpcId'] if 'VpcId' in parts['AccepterVpcInfo'] else unknown_string,
                                'A_Region': parts['AccepterVpcInfo']['Region'] if 'Region' in parts['AccepterVpcInfo'] else unknown_string,
                                'A_OwnerId': parts['AccepterVpcInfo']['OwnerId'] if 'OwnerId' in parts['AccepterVpcInfo'] else unknown_string,
                                'A_CidrBlock': parts['AccepterVpcInfo']['CidrBlock'] if 'CidrBlock' in parts['AccepterVpcInfo'] else unknown_string,

                                'R_Name': get_vpc_by_id(parts['RequesterVpcInfo']['VpcId']) if 'VpcId' in parts['RequesterVpcInfo'] else unknown_string,
                                'R_VpcId': parts['RequesterVpcInfo']['VpcId'] if 'VpcId' in parts['RequesterVpcInfo'] else unknown_string,
                                'R_Region': parts['RequesterVpcInfo']['Region'] if 'Region' in parts['RequesterVpcInfo'] else unknown_string,
                                'R_OwnerId': parts['RequesterVpcInfo']['OwnerId'] if 'OwnerId' in parts['RequesterVpcInfo'] else unknown_string,
                                'R_CidrBlock': parts['RequesterVpcInfo']['CidrBlock'] if 'CidrBlock' in parts['RequesterVpcInfo'] else unknown_string,

                                'Status': parts['Status']['Message'] if 'Message' in parts['Status'] else unknown_string,
                               })
    return results


def display_results(results):
    """
    Display the results
    """

    table = PrettyTable()

    table.field_names = [
                         'Accepter Vpc Name',
                         'Accepter Vpc ID',
                         'Accepter Vpc CIDR',
                         'Accepter Vpc Region',
                         'Accepter Vpc Owner ID',
                         'Requester Vpc Name',
                         'Requester Vpc ID',
                         'Requester Vpc CIDR',
                         'Requester Vpc Region',
                         'Requester Vpc Owner ID',
                         'Status',
                        ]

    for parts in results:
        table.add_row([
                       parts['A_Name'],
                       parts['A_VpcId'],
                       parts['A_CidrBlock'],
                       parts['A_Region'],
                       parts['A_OwnerId'],
                       parts['R_Name'],
                       parts['R_VpcId'],
                       parts['R_CidrBlock'],
                       parts['R_Region'],
                       parts['R_OwnerId'],
                       parts['Status'],
                      ])

#    table.sortby = 'Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
