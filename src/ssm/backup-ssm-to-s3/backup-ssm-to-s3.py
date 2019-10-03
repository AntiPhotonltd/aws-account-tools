#!/usr/bin/env python

# -------------------------------------------------------------------------------- #
# Description                                                                      #
# -------------------------------------------------------------------------------- #
# Take a dump of everything from 'Parameter Store', write it all to a temporary    #
# csv file before uploading to an S3 bucket for safe keeping.                      #
# -------------------------------------------------------------------------------- #


from __future__ import print_function

import argparse
import boto3
import collections
import csv
import dicttoxml
import json
import os
import requests
import sys
import time

from botocore.exceptions import ClientError, EndpointConnectionError
from termcolor import colored, cprint

SSMValue = collections.namedtuple('SSMValue', 'name, value, type')


# -------------------------------------------------------------------------------- #
# Main()                                                                           #
# -------------------------------------------------------------------------------- #
# This is the actual 'script' and the functions/sub routines are called in order.  #
# -------------------------------------------------------------------------------- #

def main(cmdline=None):
    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.default_region:
        if os.environ.get('AWS_DEFAULT_REGION') is not None:
            args.region = os.environ['AWS_DEFAULT_REGION']
            show_message('Using default region: %s' % args.region)
        else:
            show_warning('No default region found - Ignoring -d option')

    if args.region:
        client = boto3.client('ssm', region_name=args.region)
    else:
        client = boto3.client('ssm')

    if args.csv and args.xml:
        abort_script('You cannot specificy csv AND xml')

    show_message('Backuping up Parameter store to s3 bucket %s' % args.bucket)

    if args.unencrypted:
        show_warning('You are going to store the backup file UNENCRYPTED')

    if verify_s3_bucket(args) is None:
        abort_script('Backup bucket does not exist and we cannot create it')

    parameters = get_all_parameters(client, args)
    upload_parameters(parameters, args)

    return 0


# -------------------------------------------------------------------------------- #
# Make Parser                                                                      #
# -------------------------------------------------------------------------------- #
# Setup the command line parser.                                                   #
# -------------------------------------------------------------------------------- #

def make_parser():
    parser = argparse.ArgumentParser(description='Backup Parameter Store')

    parser.add_argument('-b', '--bucket', type=str, help='The bucket to write to', required=True)
    parser.add_argument('-c', '--csv', help='Write the backup as a csv file [default: json]', action='store_true')
    parser.add_argument('-d', '--default-region', help='Use the AWS_DEFAULT_REGION', action='store_true')
    parser.add_argument('-f', '--force', help='Force the creation of the bucket if it does not exist', action='store_true')
    parser.add_argument('-p', '--prefix', type=str, help='The prefix for the backup file [default: backup]', default='backup')
    parser.add_argument('-r', '--region', type=str, help='The AWS region')
    parser.add_argument('-u', '--unencrypted', help='Unencrypted backup?', action='store_true')
    parser.add_argument('-x', '--xml', help='Write the backup as a xml file [default: json]', action='store_true')
    return parser


# -------------------------------------------------------------------------------- #
# Get Value                                                                        #
# -------------------------------------------------------------------------------- #
# Get a specific value from the parameter store and return it as a tuple.          #
# -------------------------------------------------------------------------------- #

def get_value(client, args, name, encrypted=True):
    try:
        result = client.get_parameter(Name=name, WithDecryption=encrypted)
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyId':
            return SSMValue(name, 'Pending Delete', None)
        show_error('Client Error: %s' % e.response['Error']['Code'])
        return None
    except Exception as e:
        show_error('Unknown Error: %s' % e.response['Error']['Code'])
        return None

    type = result['Parameter']['Type']
    value = result['Parameter']['Value']
    if type == 'StringList':
        value = value.split(',')

    return SSMValue(name, value, type)


# -------------------------------------------------------------------------------- #
# Verify S3 Bucket                                                                 #
# -------------------------------------------------------------------------------- #
# Check to see if the backup bucket exists, and if not optional crete it.          #
# -------------------------------------------------------------------------------- #

def verify_s3_bucket(args):
    bucket = None

    s3 = boto3.resource('s3')
    try:
        bucket = s3.meta.client.head_bucket(Bucket=args.bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            show_error('Bucket Not Found')
        else:
            show_error('Client Error: %s' % e.response['Error']['Code'])

        if args.force:
            if args.region:
                show_message('Region is set to %s - attempt to create the backup bucket %s' % (args.region, args.bucket))
                try:
                    bucket = s3.create_bucket(Bucket=args.bucket, CreateBucketConfiguration={'LocationConstraint': args.region})
                    bucket.Acl().put(ACL='private')
                except Exception as e:
                    show_error('Filed to create the new bucket because: %s' % e.response['Error']['Code'])
                    return None
                return bucket
            else:
                show_error('Region is not set - cannot create backup bucket')
                bucket = None
    except Exception as e:
        show_error('Unknown Error: %s' % e.response['Error']['Code'])
        bucket = None

    return bucket


# -------------------------------------------------------------------------------- #
# Get all Parameters                                                               #
# -------------------------------------------------------------------------------- #
# Retreive a complete list of all parameters from the parameter store.             #
# -------------------------------------------------------------------------------- #

def get_all_parameters(client, args, next_token=None):
    results = []

    try:
        if next_token:
            query_result = client.describe_parameters(NextToken=next_token)
        else:
            query_result = client.describe_parameters()
    except EndpointConnectionError as e:
        show_error('%s (Probably an invalid region!)' % e)
    except Exception as e:
        show_error("Unknown error: " + str(e))
    else:
        if 'ResponseMetadata' in query_result:
            if 'HTTPStatusCode' in query_result['ResponseMetadata']:
                if query_result['ResponseMetadata']['HTTPStatusCode'] == 200:
                    if 'NextToken' in query_result:
                        results.extend(query_result['Parameters'])
                        results.extend(get_all_parameters(client, args, next_token=query_result['NextToken']))
                    else:
                        results.extend(query_result['Parameters'])

    for parts in results:
        value = None
        value_results = get_value(client, args, parts['Name']) if parts['Type'] == 'SecureString' else get_value(client, args, parts['Name'], False)
        if value_results is not None:
            value = value_results.value
        parts['Value'] = value
        if 'KeyId' not in parts:
            parts['KeyId'] = 'Unset'
        if 'Description' not in parts:
            parts['Description'] = 'Unset'

    return results


# -------------------------------------------------------------------------------- #
# Main()                                                                           #
# -------------------------------------------------------------------------------- #
# This is the actual 'script' and the functions/sub routines are called in order.  #
# -------------------------------------------------------------------------------- #

def upload_parameters(parameters, args):
    if args.csv:
        ext = 'csv'
    elif args.xml:
        ext = 'xml'
    else:
        ext = 'json'

    filename = "%s-%s.%s" % (args.prefix, time.strftime('%Y%m%d%H%M%S', time.gmtime()), ext)

    show_message("Backing up to s3://%s/%s" % (args.bucket, filename))

    if args.csv:
        keys = parameters[0].keys()
        with open(filename, 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(parameters)
    elif args.xml:
        xml_str = dicttoxml.dicttoxml(parameters)
        with open(filename, "wb") as output_file:
            output_file.write(xml_str)
    else:
        json_str = json.dumps(parameters, indent=4, sort_keys=True, default=str)
        with open(filename, "wb") as output_file:
            output_file.write(json_str)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(args.bucket)

    with open(filename, 'rb') as data:
        if args.unencrypted:
            bucket.put_object(Key=filename, Body=data)
        else:
            bucket.put_object(Key=filename, Body=data, ServerSideEncryption='aws:kms')
    os.remove(filename)

    show_message('Backup Complete')


# -------------------------------------------------------------------------------- #
# Utility Functions                                                                #
# -------------------------------------------------------------------------------- #
# A small set of utility functions for making life a little easier.                #
# -------------------------------------------------------------------------------- #

def abort_script(message, code=1):
    show_error(message)
    sys.exit(code)


def show_error(message):
    cprint('[Error] %s' % message, 'red', attrs=['bold'])


def show_warning(message):
    cprint('[Warning] %s' % message, 'yellow', attrs=['bold'])


def show_success(message):
    cprint(message, 'green', attrs=['bold'])


def show_message(message):
    cprint(message, attrs=['bold'])


# -------------------------------------------------------------------------------- #
# Main() really this time                                                          #
# -------------------------------------------------------------------------------- #
# This runs when the application is run from the command it grabs sys.argv[1:]     #
# which is everything after the program name and passes it to main the return      #
# value from main is then used as the argument to sys.exit, which you can test for #
# in the shell. program exit codes are usually 0 for ok, and non-zero for          #
# something going wrong.                                                           #
# -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -------------------------------------------------------------------------------- #
# End of Script                                                                    #
# -------------------------------------------------------------------------------- #
# This is the end - nothing more to see here.                                      #
# -------------------------------------------------------------------------------- #
