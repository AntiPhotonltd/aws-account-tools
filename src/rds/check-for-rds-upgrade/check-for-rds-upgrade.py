#!/usr/bin/env python

"""
This is a simple script for checking if there are upgrades available for your RDS.

Example Usage:

    ./check-for-rds-upgrade.py

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
        client = boto3.client('rds', region_name=args.region)
    else:
        client = boto3.client('rds')

    current_versions = get_current_versions(client)
    possible_upgrades, real_upgrades = get_possible_upgrades(client, current_versions, args.all_databases)

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

    parser = argparse.ArgumentParser(description='Check for RDS Upgrades')

    parser.add_argument('-a', '--all-databases', help='List all databases (even if not upgradable)', action='store_true')
    parser.add_argument('-e', '--exit-code', help='Set exit code to number of available upgrades', action='store_true')
    parser.add_argument('-r', '--region', type=str, help='The aws region')
    parser.add_argument('-s', '--silent', help='Surpress all output', action='store_true')

    return parser


def get_current_versions(client):
    """
    Query a list of current RDS instances and their version numbers
    """

    current_versions = []

    response = client.describe_db_instances()

    for instance in response['DBInstances']:
        current_versions.append({
                                 'InstanceName': instance['DBInstanceIdentifier'],
                                 'Engine': instance['Engine'],
                                 'EngineVersion': instance['EngineVersion'],
                                })

    return current_versions


def get_possible_upgrades(client, current_versions, all_databases):
    """
    Check each RDS instance to see if there is an upgrade available
    """

    possible_upgrades = []
    real_upgrades = 0

    for instance in current_versions:
        latest_in_place_response = client.describe_db_engine_versions(Engine=instance['Engine'], EngineVersion=instance['EngineVersion'])

        latest_in_place_list = latest_in_place_response['DBEngineVersions'][0]['ValidUpgradeTarget']

        if latest_in_place_list:
            latest_in_place_upgrade = latest_in_place_list[-1]['EngineVersion']
            in_place_upgrade_available = True
        else:
            latest_in_place_upgrade = instance['EngineVersion']
            in_place_upgrade_available = False

        latest_response = client.describe_db_engine_versions(Engine=instance['Engine'])

        latest_upgrade = latest_response['DBEngineVersions'][-1]['EngineVersion']

        if cmp_version(latest_upgrade, instance['EngineVersion']) > 0:
            upgrade_available = True
        else:
            upgrade_available = False

        if in_place_upgrade_available or upgrade_available:
            is_upgrade_available = 1
        else:
            is_upgrade_available = 0

        if is_upgrade_available == 1:
            real_upgrades += 1

        if all_databases or is_upgrade_available == 1:
            possible_upgrades.append({
                                       'InstanceName': instance['InstanceName'],
                                       'Engine': instance['Engine'],
                                       'EngineVersion': instance['EngineVersion'],
                                       'LatestInPlaceUpgrade': latest_in_place_upgrade,
                                       'LatestUpgrade': latest_upgrade,
                                       'UpgradeAvailable': is_upgrade_available
                                     })
    return possible_upgrades, real_upgrades



def display_upgrades(current_upgrades):
    """
    Display the databases which can be upgraded (or all if flat is set)
    """

    x = PrettyTable()

    x.field_names = [
                     'Instance Name',
                     'Engine',
                     'Engine Version',
                     'Latest In Place Upgrade',
                     'Latest Upgrade',
                     'Upgrade Available'
                    ]

    for upgrade in current_upgrades:
        x.add_row([
                   upgrade['InstanceName'],
                   upgrade['Engine'],
                   upgrade['EngineVersion'],
                   upgrade['LatestInPlaceUpgrade'],
                   upgrade['LatestUpgrade'],
                   upgrade['UpgradeAvailable']
                  ])

    x.sortby = 'Instance Name'
    print(x)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
