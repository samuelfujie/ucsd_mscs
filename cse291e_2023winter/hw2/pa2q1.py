#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Thu Jan 26 15:36:08 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

from collections import defaultdict

import gzip

# Upzip the gzip file
gzip_file_name = '20221001.as-org2info.txt.gz'
data_file_name = '2r0221001.as-org2info.txt'

with gzip.open(gzip_file_name, 'rb') as file:
    with open(data_file_name, 'wb') as output_file:
        output_file.write(file.read())

# removing the new line characters
with open(data_file_name) as f:
    lines = [line.rstrip() for line in f]

orgname_to_ids = defaultdict(set)
orgid_to_asnums = defaultdict(set)

for line in lines:
    cells = line.split('|')

    # organization entry: org_id -> organization name
    if len(cells) == 5:
        org_id = cells[0]
        org_name = cells[2]

        orgname_to_ids[org_name].add(org_id)
    
    # AS number entry: AS number -> org_id
    if len(cells) == 6:
        as_num = cells[0]
        org_id = cells[3]

        orgid_to_asnums[org_id].add(as_num)

# Load organization name
with open('input.txt') as file:
    input_org_name = file.read()

input_org_ids = orgname_to_ids[input_org_name]
input_org_asnums = []

for input_org_id in input_org_ids:
    input_org_asnums.extend(orgid_to_asnums[input_org_id])

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(input_org_asnums))
