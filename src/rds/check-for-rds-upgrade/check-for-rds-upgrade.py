#!/usr/bin/env python

"""
Example Usage:

    ./check-for-rds-upgrade.py
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
    parser.add_argument('-r', '--region', help='The aws region')
    parser.add_argument('-s', '--silent', help='Surpress all output', action='store_true')

    return parser


def get_current_versions(client):
    """
    Query a list of current RDS instances and their version numbers
    """

    current_versions = []

    try:
        response = client.describe_db_instances()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'DBInstances' in response:
            for instance in response['DBInstances']:
                current_versions.append({
                                         'InstanceName': instance['DBInstanceIdentifier'] if 'DBInstanceIdentifier' in instance else unknown_string,
                                         'Engine': instance['Engine'] if 'Engine' in instance else unknown_string,
                                         'EngineVersion': instance['EngineVersion'] if 'EngineVersion' in instance else unknown_string,
                                        })
    return current_versions


def get_latest_in_place_version(client, instance):
    """
    Get the latest in place upgrade version
    """

    latest_in_place_list = []

    try:
        latest_in_place_response = client.describe_db_engine_versions(Engine=instance['Engine'], EngineVersion=instance['EngineVersion'])
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        latest_in_place_list = latest_in_place_response['DBEngineVersions'][0]['ValidUpgradeTarget']

    if latest_in_place_list:
        latest_in_place_upgrade = latest_in_place_list[-1]['EngineVersion']
        in_place_upgrade_available = True
    else:
        latest_in_place_upgrade = instance['EngineVersion']
        in_place_upgrade_available = False

    return latest_in_place_upgrade, in_place_upgrade_available


def get_latest_upgrade(client, instance):
    """
    Get the latest full upgrade version
    """
    latest_upgrade = unknown_version

    try:
        latest_response = client.describe_db_engine_versions(Engine=instance['Engine'])
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        latest_upgrade = latest_response['DBEngineVersions'][-1]['EngineVersion']

    return latest_upgrade

def get_possible_upgrades(client, current_versions, all_databases):
    """
    Check each RDS instance to see if there is an upgrade available
    """

    possible_upgrades = []
    real_upgrades = 0

    for instance in current_versions:
        latest_in_place_upgrade, in_place_upgrade_available = get_latest_in_place_version(client, instance)
        latest_upgrade = get_latest_upgrade(client, instance)

        upgrade_available = True if cmp_version(latest_upgrade, instance['EngineVersion']) > 0 else False
        is_upgrade_available = True if in_place_upgrade_available or upgrade_available else False

        if is_upgrade_available:
          real_upgrades += 1

        if all_databases or is_upgrade_available:
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

    table = PrettyTable()

    table.field_names = [
                         'Instance Name',
                         'Engine',
                         'Engine Version',
                         'Latest In Place Upgrade',
                         'Latest Upgrade',
                         'Upgrade Available'
                        ]

    for upgrade in current_upgrades:
        table.add_row([
                       upgrade['InstanceName'],
                       upgrade['Engine'],
                       upgrade['EngineVersion'],
                       upgrade['LatestInPlaceUpgrade'],
                       upgrade['LatestUpgrade'],
                       upgrade['UpgradeAvailable']
                      ])

    table.sortby = 'Instance Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
