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

large_org_names = []

for orgname, org_ids in orgname_to_ids.items():
    asnums = []
    for org_id in org_ids:
        asnums.extend(orgid_to_asnums[org_id])

    # check if the org is large enough
    if len(set(asnums)) >= 20:
        large_org_names.append(orgname)

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(large_org_names))
