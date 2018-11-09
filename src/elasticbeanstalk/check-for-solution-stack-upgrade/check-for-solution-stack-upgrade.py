#!/usr/bin/env python

"""
Example Usage:

     ./check-for-solution-stack-upgrade.py
"""

from __future__ import print_function

import argparse
import boto3
import re
import requests
import sys

from botocore.exceptions import ClientError, EndpointConnectionError
from prettytable import PrettyTable

empty_string = ''
unknown_string = 'Unknown'
unknown_version = '0.0.0'
unknown_int = 0
platform_cache = []


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


def get_latest_available_platform_version(client, platform_name, os_version):

    """
    Get the list of available versions for a given platform name
    """

    available_versions = []
    try:
        response = client.list_platform_versions(Filters=[{
                                                           'Type': 'PlatformName',
                                                           'Operator': 'contains',
                                                           'Values': [platform_name]
                                                          }])
    except ClientError as e:
        print("ERROR: Unexpected error: %s" % e)
    else:
        if 'PlatformSummaryList' in response:
            for result in response['PlatformSummaryList']:
                if 'OperatingSystemVersion' in result and result['OperatingSystemVersion'] == os_version and 'PlatformArn' in result:
                    parts = str(result['PlatformArn']).split('/')
                    available_versions.append(parts[-1])

    if (len(available_versions) > 0):
        return available_versions[0]
    return unknown_version


def get_platform_information(client, PlatformArn):
    """
    Stuff
    """
    for cache in platform_cache:
        if cache['PlatformArn'] == PlatformArn:
            return cache['OperatingSystemVersion'], cache['PlatformName'], cache['PlatformVersion'], cache['LatestVersion']

    OSVersion = unknown_string
    PlatformName = unknown_string
    PlatformVersion = unknown_version
    LatestVersion = unknown_version

    try:
        response = client.describe_platform_version(PlatformArn=PlatformArn)
    except ClientError as e:
        print("ERROR: Unexpected error: %s" % e)
    else:
        if 'PlatformDescription' in response:
            instance = response['PlatformDescription']
            OSVersion = instance['OperatingSystemVersion'] if 'OperatingSystemVersion' in instance else unknown_string
            PlatformName = instance['PlatformName'] if 'PlatformName' in instance else unknown_string
            PlatformVersion = instance['PlatformVersion'] if 'PlatformVersion' in instance else unknown_version
            LatestVersion = get_latest_available_platform_version(client, PlatformName, OSVersion)

    platform_cache.append({
                           'PlatformArn': PlatformArn,
                           'OperatingSystemVersion': OSVersion,
                           'PlatformName': PlatformName,
                           'PlatformVersion': PlatformVersion,
                           'LatestVersion': LatestVersion
                          })

    return OSVersion, PlatformName, PlatformVersion, LatestVersion


def get_current_versions(client):
    """
    Get the current list of beanstalks and their versions
    """
    current_versions = []

    try:
        response = client.describe_environments()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'Environments' in response and len(response['Environments']) > 0:
            for result in response['Environments']:
                os_version, platform_name, platform_version, latest_version = get_platform_information(client, result['PlatformArn'])

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
                         'Application',
                         'Environment',
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

    table.sortby = 'Application'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
