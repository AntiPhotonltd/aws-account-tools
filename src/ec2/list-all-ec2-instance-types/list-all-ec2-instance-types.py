#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------- #
# Description                                                                      #
# -------------------------------------------------------------------------------- #
# Take a dump of everything from 'Parameter Store', write it all to a temporary    #
# csv file before uploading to an S3 bucket for safe keeping.                      #
# -------------------------------------------------------------------------------- #
# Example Usage:                                                                   #
#                                                                                  #
#    ./list-all-ec2-instance-types.py                                              #
# -------------------------------------------------------------------------------- #


from __future__ import print_function

import argparse
import json
import progressbar
import requests
import sys

import os.path

from operator import itemgetter
from prettytable import PrettyTable

default_url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
default_filename = "index.json"
default_chunk_size = 4096

cache_file = "cached.json"

empty_string = ''
unknown_string = 'Unknown'
unknown_version = '0.0.0'
unknown_int = 0


# -------------------------------------------------------------------------------- #
# Main()                                                                           #
# -------------------------------------------------------------------------------- #
# This is the actual 'script' and the functions/sub routines are called in order.  #
# -------------------------------------------------------------------------------- #

def main(cmdline=None):
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')

    parser = make_parser()

    args = parser.parse_args(cmdline)

    if args.force_cache or args.force_all:
        if os.path.exists(cache_file):
            os.remove(cache_file)
    if args.force_pricing or args.force_all:
        if os.path.exists(default_filename):
            os.remove(default_filename)

    file_contents = load_file(cache_file, default_chunk_size)
    if file_contents is not None:
        results = convert_to_json(file_contents)
        display_results(results)
        return

    file_contents = load_file(default_filename, default_chunk_size)
    if file_contents is None:
        file_contents = download_file(default_url, default_filename, default_chunk_size)
        if file_contents is None:
            print("Failed to download the pricing file")
            return

    results = convert_to_json(file_contents)
    results = process_file_contents(results)
    display_results(results)
    save_cache_file(results)


# -------------------------------------------------------------------------------- #
# Make Parser                                                                      #
# -------------------------------------------------------------------------------- #
# Setup the command line parser.                                                   #
# -------------------------------------------------------------------------------- #

def make_parser():

    """
    This function builds up the command line parser that is used by the script.
    """

    parser = argparse.ArgumentParser(description='List EC2 Instance Types')
    parser.add_argument('-a', '--force-all', help='--force-cache & --force-pricing', action='store_true')
    parser.add_argument('-c', '--force-cache', help='Force re-calculation of the cache file', action='store_true')
    parser.add_argument('-p', '--force-pricing', help='Force downlaod of pricing file', action='store_true')
    return parser


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def convert_to_json(data):
    """
    """
    print("Converting to json")
    json_data = json.loads(data)
    return json_data


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def load_file(filename, chunk_size):
    """
    """
    data = ''

    if not os.path.isfile(filename):
        return None

    print("Loading Data...")

    file_size = os.path.getsize(filename)
    num_bars = file_size / chunk_size
    bar = progressbar.ProgressBar(maxval=num_bars, term_width=100).start()
    i = 0

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            data += chunk
            bar.update(i)
            i += 1
    bar.finish()

    return data


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def save_cache_file(results):
    json_str = json.dumps(results, indent=4, sort_keys=True, default=str)
    with open(cache_file, "wb") as output_file:
        output_file.write(json_str)


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def download_file(url, filename, chunk_size):
    file_content = ''

    print("Downloading %s" % filename)
    r = requests.get(url, stream=True)
    f = open(filename, 'wb')
    file_size = int(r.headers['Content-Length'])
    num_bars = file_size / chunk_size
    bar = progressbar.ProgressBar(maxval=num_bars, term_width=100).start()
    i = 0

    for chunk in r.iter_content(chunk_size=chunk_size):
        f.write(chunk)
        file_content += chunk
        bar.update(i)
        i += 1
    f.close()
    bar.finish()
    return file_content


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def get_child_value(child_name):
    child_value = None

    child_lookup_table = [
                          'metal',
                          'nano',
                          'micro',
                          'small',
                          'medium',
                          'large',
                          'xlarge',
                          '2xlarge',
                          '3xlarge',
                          '4xlarge',
                          '6xlarge',
                          '8xlarge',
                          '9xlarge',
                          '10xlarge',
                          '12xlarge',
                          '16xlarge',
                          '18xlarge',
                          '24xlarge',
                          '32xlarge',
                         ]

    try:
        child_value = child_lookup_table.index(child_name)
    except ValueError:
        print("Child NOT found: %s" % child_name)

    return child_value


def get_region_from_name(search_name):
    search_name = search_name.replace('(', '')
    search_name = search_name.replace(')', '')
    search_name = search_name.replace('.', '')
    search_name = search_name.replace(' ', '-')

    region_list = {
                   'us-east-2': 'US-East-Ohio',
                   'us-east-1': 'US-East-N-Virginia',
                   'us-west-1': 'US-West-N-California',
                   'us-west-2': 'US-West-Oregon',
                   'ap-south-1': 'Asia-Pacific-Mumbai',
                   'ap-northeast-3': 'Asia-Pacific-Osaka-Local',
                   'ap-northeast-2': 'Asia-Pacific-Seoul',
                   'ap-southeast-1': 'Asia-Pacific-Singapore',
                   'ap-southeast-2': 'Asia-Pacific-Sydney',
                   'ap-northeast-1': 'Asia-Pacific-Tokyo',
                   'ca-central-1': 'Canada-Central',
                   'cn-north-1': 'China-Beijing',
                   'cn-northwest-1': 'China-Ningxia',
                   'eu-central-1': 'EU-Frankfurt',
                   'eu-west-1': 'EU-Ireland',
                   'eu-west-2': 'EU-London',
                   'eu-west-3': 'EU-Paris',
                   'eu-north-1': 'EU-Stockholm',
                   'sa-east-1': 'South-America-Sao-Paulo',
                   'us-gov-east-1': 'AWS-GovCloud-US-East',
                   'us-gov-west-1': 'AWS-GovCloud-US',
                  }

    for code, name in region_list.items():
        if name == search_name:
            return(code)

    print("%s is NOT found in the list" % search_name)
    return None


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def process_file_contents(data):
    results = []

    count = len(data['products'])
    print("Processing %d entries" % (count))
    bar = progressbar.ProgressBar(maxval=count, term_width=100).start()
    i = 0

    for name, value in data['products'].items():
        bar.update(i)
        i += 1

        if 'attributes' in value:
            parts = value['attributes']

            if 'instanceType' in parts:
                if not any(r['InstanceType'] == parts['instanceType'] for r in results):
                    locations = []
                    regions = []
                    if 'location' in parts:
                        locations.append(parts['location'])
                        region = get_region_from_name(parts['location'])
                        if region is not None:
                            regions.append(region)

                    bits = parts['instanceType'].split('.', 1)

                    parent = bits[0]
                    child = get_child_value(bits[1]) if len(bits) > 1 else 0

                    results.append({
                                    'ParentType': parent,
                                    'ChildType': child,
                                    'InstanceType': parts['instanceType'] if 'instanceType' in parts else unknown_string,
                                    'VPCU': parts['vcpu'] if 'vcpu' in parts else unknown_string,
                                    'Memory': parts['memory'] if 'memory' in parts else unknown_string,
                                    'Storage': parts['storage'] if 'storage' in parts else unknown_string,
                                    'Location': locations,
                                    'Regions': regions,
                                   })
                else:
                    my_item = next((item for item in results if item['InstanceType'] == parts['instanceType']), None)
                    if my_item is not None:
                        if parts['location'] not in my_item['Location']:
                            my_item['Location'].append(parts['location'])

                        region = get_region_from_name(parts['location'])
                        if region is not None and region not in my_item['Regions']:
                            my_item['Regions'].append(region)

    bar.finish()
    return results


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def multikeysort(items, columns):
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]

    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)


# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------- #

def display_results(results):
    table = PrettyTable()

    table.field_names = [
                         'Parent Type',
                         'Instance Type',
                         'VPCUs',
                         'Memory',
                         'Storage',
                         'Location',
                         'Regions',
                        ]

    sorted_results = multikeysort(results, ['ParentType', 'ChildType'])

    for parts in sorted_results:
        sorted_list = sorted(parts['Location'])
        locations = '\n'.join(map(str, sorted_list))

        sorted_regions = sorted(parts['Regions'])
        regions = '\n'.join(map(str, sorted_regions))
        table.add_row([
                       parts['ParentType'],
                       parts['InstanceType'],
                       parts['VPCU'],
                       parts['Memory'],
                       parts['Storage'],
                       locations,
                       regions,
                      ])

    print(table)


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
