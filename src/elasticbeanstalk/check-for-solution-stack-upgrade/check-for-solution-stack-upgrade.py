#!/usr/bin/env python

"""
This is a simple script for checking if there are solution stack upgrades available.

Example Usage:

     ./check-for-solution-stack-upgrade.py -p "Python 3.4 running on 64bit Amazon Linux" -o "2018.03"

Based on an original idea by https://github.com/adamdodev
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

    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.region:
        client = boto3.client('elasticbeanstalk', region_name=args.region)
    else:
        client = boto3.client('elasticbeanstalk')

    available_versions, latest_version = get_available_versions(client, args.platform_name, args.os_version)
    current_versions = get_current_versions(client, latest_version)
    possible_upgrades = get_possible_upgrades(latest_version, current_versions, args.all_beanstalks)

    display_upgrades(possible_upgrades)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Check Soution Stack Version')

    parser.add_argument('-a', '--all-beanstalks', help='List all beanstalks (even if not upgradable)', action='store_true')
    parser.add_argument('-o', '--os-version', type=str, help='Operating system version')
    parser.add_argument('-p', '--platform-name', type=str, help='Current platform stack name', required=True)
    parser.add_argument('-r', '--region', type=str, help='The aws region')
    return parser


def get_available_versions(client, platform_name, os_version):

    """
    Get the list of available versions for a given platform name
    """

    available_versions = []

    response = client.list_platform_versions(Filters=[{
                                                       'Type': 'PlatformName',
                                                       'Operator': 'contains',
                                                       'Values': [platform_name]
                                                      }])

    for result in response['PlatformSummaryList']:
        if not os_version or result['OperatingSystemVersion'] == os_version:
            parts = str(result['PlatformArn']).split('/')
            available_versions.append(parts[-1])

    return available_versions, available_versions[0]


def get_current_versions(client, latest_version):
    """
    Get the current list of beanstalks and their versions
    """
    current_versions = []

    response = client.describe_environments()

    for result in response['Environments']:
        arn_parts = str(result['PlatformArn']).split('/')
        current_versions.append({
            'ApplicationName': result['ApplicationName'],
            'EnvironmentName': result['EnvironmentName'],
            'PlatformVersion': arn_parts[-1],
            'LatestPlatformVersion': latest_version
        })

    return current_versions


def get_possible_upgrades(latest_version, current_versions, all_beanstalks):
    """
    Calculate which beanstalks can be upgraded
    """

    upgrades = []

    for version in current_versions:
        if version['PlatformVersion'] != version['LatestPlatformVersion']:
            upgrade_available = 1
        else:
            upgrade_available = 0

        if all_beanstalks or upgrade_available == 1:
            upgrades.append({
                             'ApplicationName': version['ApplicationName'],
                             'EnvironmentName': version['EnvironmentName'],
                             'PlatformVersion': version['PlatformVersion'],
                             'LatestPlatformVersion': version['LatestPlatformVersion'],
                             'UpgradeAvailable': upgrade_available
                            })

    return upgrades


def display_upgrades(current_upgrades):
    """
    Display a list of stacks that have avilable upgrades
    """

    x = PrettyTable()

    x.field_names = [
                     'Application Name',
                     'Environment Name',
                     'Current Platform Version',
                     'Latest Platform Version',
                     'Upgrade Available',
                    ]

    for upgrade in current_upgrades:
        x.add_row([
                   upgrade['ApplicationName'],
                   upgrade['EnvironmentName'],
                   upgrade['PlatformVersion'],
                   upgrade['LatestPlatformVersion'],
                   upgrade['UpgradeAvailable']
                  ])

    x.sortby = 'Environment Name'
    print(x)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
