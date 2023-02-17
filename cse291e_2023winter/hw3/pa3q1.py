#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Thu Feb 16 19:11:11 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

import gzip
import pytricia

from collections import defaultdict


# Upzip the gzip file
gzip_file_name = 'routeviews-rv2-20230201-1200.pfx2as.gz'
dataset_file_name = 'routeviews-rv2-20230201-1200.pfx2as'

with gzip.open(gzip_file_name, 'rb') as file:
    with open(dataset_file_name, 'wb') as output_file:
        output_file.write(file.read())

with open(dataset_file_name) as file:
    lines = [line.rstrip() for line in file]


# Parse the dataset and store the mapping
ip_prefix_to_as_set = defaultdict(set)

for line in lines:
    row = line.split()

    prefix = row[0]
    length = row[1]
    num = row[2]

    as_list = num.split('_')

    for as_num in as_list:
        # Ignore AS sets
        if ',' not in as_num:
            ip_prefix_to_as_set[prefix + '/' + length].add(as_num)


# Construct trie tree
pyt = pytricia.PyTricia()

for ip_prefix in ip_prefix_to_as_set.keys():
    pyt.insert(ip_prefix, "")


# Load IP address
with open('input.txt') as file:
    target_ip_address = file.read()

# Find the longest matching prefix
best_match_prefix = pyt.get_key(target_ip_address)

# Locate the ASes that owns the prefix
target_as_set = ip_prefix_to_as_set[best_match_prefix]

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(list(target_as_set)))
