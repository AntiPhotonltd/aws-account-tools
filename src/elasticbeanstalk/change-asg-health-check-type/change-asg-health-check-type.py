#!/usr/bin/env python

"""
Example Usage:

    ./change-asg-health-check-type.py
"""

from __future__ import print_function

import argparse
import boto3
import requests
import sys

from botocore.exceptions import ClientError, EndpointConnectionError
from dictsearch.search import iterate_dictionary
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
        client = boto3.client('elasticbeanstalk', region_name=args.region)
    else:
        client = boto3.client('elasticbeanstalk')

    asg_name = get_asg_name(client, args)
    if asg_name == None:
        print('Failed to find the asg_name - Aborting')
        exit(1)

    if args.region:
        client = boto3.client('autoscaling', region_name=args.region)
    else:
        client = boto3.client('autoscaling')

    change_health_check_type(client, asg_name, args.grace_period)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='Change ASG Health Check Type')

    parser.add_argument('-b', '--beanstalk', help='The beanstalk application name', required=True)
    parser.add_argument('-g', '--grace-period', type=int, help='Delay', default=300)
    parser.add_argument('-r', '--region', help='The aws region')

    return parser


def get_asg_name(client, args):
    """
    Query the API
    """

    asg_name = None

    try:
        response = client.describe_environment_resources(EnvironmentName=args.beanstalk)
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print(str(e))
        exit(1)
    else:
        if 'EnvironmentResources' in response and len(response['EnvironmentResources']) > 0:
            if iterate_dictionary(response,"EnvironmentResources/AutoScalingGroups/Name"):
                asg_name = iterate_dictionary(response,"EnvironmentResources/AutoScalingGroups/Name")[0]

    return asg_name


def change_health_check_type(client, asg_name, grace_period):
    """
    Display the results
    """

    try:
        response = client.update_auto_scaling_group(AutoScalingGroupName=asg_name, HealthCheckType='ELB', HealthCheckGracePeriod=grace_period)
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print(str(e))
        exit(1)
    else:
        print(response)
        if iterate_dictionary(response,"ResponseMetadata/HTTPStatusCode"):
            status_code = iterate_dictionary(response,"ResponseMetadata/HTTPStatusCode")[0]
            if status_code == 200:
                print('Update sucessful')
            else:
                print('Update failed')


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
