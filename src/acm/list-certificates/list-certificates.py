#!/usr/bin/env python

"""
This is a simple script for listing all certificates from ACM

Example Usage:

    ./list-certificates.py
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

    client = boto3.client('acm')

    certificates = get_certificates(client)
    display_certificates(certificates)


def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List Certificates')

    return parser


def get_certificates(client):
    """
    Query a list of certificates
    """

    certificates = []

    try:
        response = client.list_certificates()
    except EndpointConnectionError as e:
        print("ERROR: %s (Probably an invalid region!)" % e)
    except Exception as e:
        print("Unknown error: " + str(e))
    else:
        if 'CertificateSummaryList' in response:
            for cert in response['CertificateSummaryList']:
                certificates.append({
                                     'CertificateArn': cert['CertificateArn'] if 'CertificateArn' in cert else unknown_string,
                                     'DomainName': cert['DomainName'] if 'DomainName' in cert else unknown_string
                                    })
    return certificates


def display_certificates(certificates):
    """
    Display all the certificates
    """

    table = PrettyTable()

    table.field_names = [
                         'Domain Name',
                         'Certificate Arn'
                        ]

    for cert in certificates:
        table.add_row([
                       cert['DomainName'],
                       cert['CertificateArn']
                      ])

    table.sortby = 'Domain Name'
    print(table)


if __name__ == "__main__":

    # This runs when the application is run from the command it grabs sys.argv[1:] which is everything after
    # the program name and passes it to main the return value from main is then used as the argument to
    # sys.exit, which you can test for in the shell. program exit codes are usually 0 for ok, and non-zero
    # for something going wrong.

    sys.exit(main(sys.argv[1:]))
