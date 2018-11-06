#!/usr/bin/env python

"""
This is a simple script for checking if there are solution stack upgrades available.
"""

from __future__ import print_function

import argparse
import boto3
import sys
import requests

from prettytable import PrettyTable


def main(cmdline=None):

    """
    The main function. This takes the command line arguments provided and parse them.
    """

    client = boto3.client('elasticbeanstalk')

    parser = make_parser()

    args = parser.parse_args(cmdline)

    available_versions, latest_version = get_available_versions(client, args.platform_name, args.os_version, args.verbose)
    current_versions = get_current_versions(client, latest_version, args.verbose)
    possible_upgrades = get_possible_upgrades(latest_version, current_versions)

    display_upgrades(possible_upgrades)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Check Soution Stack Version')

    parser.add_argument('-o', '--os-version', type=str, help='Operating system version')
    parser.add_argument('-p', '--platform-name', type=str, help='Current platform stack name', required=True)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    return parser


def get_available_versions(client, platform_name, os_version, verbose):

    """
    Retrieve the actual list
    """

    available_versions = []

    if verbose:
        if os_version:
            print("Retrieving details for %s (%s)" % (platform_name, os_version))
        else:
            print("Retrieving details for %s" % platform_name)

    response = client.list_platform_versions(Filters=[{
                                                       'Type': 'PlatformName',
                                                       'Operator': 'contains',
                                                       'Values': [platform_name]
                                                      }])

    if verbose:
        print("Available Platform Versions:")
        print("Search: %s:" % platform_name)

    for result in response['PlatformSummaryList']:
        if not os_version or result['OperatingSystemVersion'] == os_version:
            parts = str(result['PlatformArn']).split('/')
            available_versions.append(parts[-1])

    return available_versions, available_versions[0]


def get_current_versions(client, latest_version, verbose):
    """
    Stuff
    """
    current_versions = []

    response = client.describe_environments()

    for result in response['Environments']:
        arn_parts = str(result['PlatformArn']).split('/')
        current_versions.append({
            'ApplicationName': result['ApplicationName'],
            'EnvironmentId': result['EnvironmentId'],
            'EnvironmentName': result['EnvironmentName'],
            'PlatformArn': result['PlatformArn'],
            'PlatformVersion': arn_parts[-1],
            'LatestPlatformVersion': latest_version
        })

    return current_versions


def get_possible_upgrades(latest_version, current_versions):
    """
    more stuff
    """

    upgrades = []

    for version in current_versions:
        if version['PlatformVersion'] != version['LatestPlatformVersion']:
            upgrades.append(version)
    return upgrades


def display_upgrades(current_upgrades):
    """
    stuff
    """

    x = PrettyTable()

    x.field_names = [
                     'Application Name',
                     'Environment Name',
                     'Current Platform Version',
                     'Latest Platform Version',
                     'Environment Id',
                     'Platform Arn'
                    ]

    for upgrade in current_upgrades:
        x.add_row([
                   upgrade['ApplicationName'],
                   upgrade['EnvironmentName'],
                   upgrade['PlatformVersion'],
                   upgrade['LatestPlatformVersion'],
                   upgrade['EnvironmentId'],
                   upgrade['PlatformArn']
                  ])

    print(x)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
