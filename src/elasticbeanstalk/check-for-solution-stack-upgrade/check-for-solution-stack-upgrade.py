#!/usr/bin/env python

"""
This is a simple script for checking if there are solution stack upgrades available.

Example Usage:

     ./check-for-solution-stack-upgrade.py

Based on an original idea by https://github.com/adamdodev
"""

from __future__ import print_function

import argparse
import boto3
import re
import requests
import sys

from prettytable import PrettyTable


def cmp_version(version1, version2):
    """
    Compare 2 version strings
    """

    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
    return cmp(normalize(version1), normalize(version2))


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

    current_versions = get_current_versions(client)

    possible_upgrades, real_upgrades = get_possible_upgrades(current_versions, args.all_beanstalks)

    if not args.silent:
        display_upgrades(possible_upgrades)

    if args.exit_code:
        sys.exit(real_upgrades)
    else:
        sys.exit(0)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Check for Soution Stack Upgrades')

    parser.add_argument('-a', '--all-beanstalks', help='List all beanstalks (even if not upgradable)', action='store_true')
    parser.add_argument('-e', '--exit-code', help='Set exit code to number of available upgrades', action='store_true')
    parser.add_argument('-r', '--region', help='The aws region')
    parser.add_argument('-s', '--silent', help='Surpress all output', action='store_true')
    return parser


def get_latest_available_version(client, platform_name, os_version):

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
        if result['OperatingSystemVersion'] == os_version:
            parts = str(result['PlatformArn']).split('/')
            available_versions.append(parts[-1])

    return available_versions[0]


def get_operating_system_version(client, PlatformArn):
    response = client.describe_platform_version(PlatformArn=PlatformArn)

    OSVersion = response['PlatformDescription']['OperatingSystemVersion']
    PlatformName = response['PlatformDescription']['PlatformName']
    PlatformVersion = response['PlatformDescription']['PlatformVersion']

    return OSVersion, PlatformName, PlatformVersion


def get_current_versions(client):
    """
    Get the current list of beanstalks and their versions
    """
    current_versions = []
    previous_arn = ''

    response = client.describe_environments()

    for result in response['Environments']:

        if previous_arn != result['PlatformArn']:
            """
              Attempt to speed things up with a little bit of caching - only relookup details if the ARN changes
            """
            os_version, platform_name, platform_version = get_operating_system_version(client, result['PlatformArn'])
            previous_arn = result['PlatformArn']

        latest_version = get_latest_available_version(client, platform_name, os_version)

        current_versions.append({
            'ApplicationName': result['ApplicationName'],
            'EnvironmentName': result['EnvironmentName'],
            'SolutionStackName': result['SolutionStackName'],
            'PlatformName': platform_name,
            'PlatformVersion': platform_version,
            'OSVersion': os_version,
            'LatestPlatformVersion': latest_version
        })

    return current_versions


def get_possible_upgrades(current_versions, all_beanstalks):
    """
    Calculate which beanstalks can be upgraded
    """

    upgrades = []
    real_upgrades = 0

    for version in current_versions:
        if cmp_version(version['LatestPlatformVersion'], version['PlatformVersion']) > 0:
            upgrade_available = True
            real_upgrades += 1
        else:
            upgrade_available = False

        if all_beanstalks or upgrade_available:
            upgrades.append({
                             'ApplicationName': version['ApplicationName'],
                             'EnvironmentName': version['EnvironmentName'],
                             'SolutionStackName': version['SolutionStackName'],
                             'PlatformName': version['PlatformName'],
                             'PlatformVersion': version['PlatformVersion'],
                             'OSVersion': version['OSVersion'],
                             'LatestPlatformVersion': version['LatestPlatformVersion'],
                             'UpgradeAvailable': upgrade_available
                            })

    return upgrades, real_upgrades


def display_upgrades(current_upgrades):
    """
    Display a list of stacks that have avilable upgrades
    """

    table = PrettyTable()

    table.field_names = [
                         'Application Name',
                         'Environment Name',
                         'Solution Stack',
                         'Current Version',
                         'Latest Version',
                         'Upgrade Available',
                        ]

    for upgrade in current_upgrades:
        table.add_row([
                       upgrade['ApplicationName'],
                       upgrade['EnvironmentName'],
                       upgrade['SolutionStackName'],
                       upgrade['PlatformVersion'],
                       upgrade['LatestPlatformVersion'],
                       upgrade['UpgradeAvailable']
                      ])

    table.sortby = 'Environment Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
