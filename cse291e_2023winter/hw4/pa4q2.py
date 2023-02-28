#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Sun Feb 26 16:28:16 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

from collections import defaultdict, deque

import bz2
import csv
import gzip


isp_csv_file_name = 'manrs_isp_20230221.csv'
cdn_csv_file_name = 'manrs_cdn_20230221.csv'

rel_bz2_file_name = '20230201.as-rel.txt.bz2'

MANRS_ases = set()
MANRS_core = set()

t1_providers = set()

p2c = defaultdict(set)


'''
Step 1: Parse the participants lists in the MANRS ISP program 
        and MANRS CDN program and keep a list of ASes participating 
        in those programs. We refer to those ASes as MANRS ASes.
'''

# Process CSV files
with open(isp_csv_file_name, newline='') as csvfile:
    data = csv.DictReader(csvfile)

    for row in data:
        asn_list = row['ASNs'].split(';')
        for asn in asn_list:
            MANRS_ases.add(asn)

with open(cdn_csv_file_name, newline='') as csvfile:
    data = csv.DictReader(csvfile)

    for row in data:
        asn_list = row['ASNs'].split(';')
        for asn in asn_list:
            MANRS_ases.add(asn)


'''
Step 2: Parse the AS relationship file. Maintain a list of Tier 1 
        providers (§2.3.2) and a mapping of each AS to its customer ASes.
'''

for byte_line in bz2.BZ2File(rel_bz2_file_name, 'rb'):
    # convert byte string into regular string line
    string_line = byte_line.decode("utf-8").strip()

    # Find tier 1 ASNs
    if string_line[0] == '#':
        cells = string_line.split(' ')

        if cells[1] == 'input':
            for cell in cells:
                if cell.isdigit():
                    t1_providers.add(cell)


    # Provider-Customer link
    else:
        cells = string_line.split('|')
        if cells[-1] == '-1':
            p2c[cells[0]].add(cells[1])


'''
Step 3: Find the list of ASes that are Tier 1 providers and MANRS 
        ASes. Add them to the MANRS Core.
'''

for provider in t1_providers:
    if provider in MANRS_ases:
        MANRS_core.add(provider)


'''
Step 4: For each AS in the MANRS Core, find its customer ASes and 
        add them to the MANRS Core if they are also MANRS ASes.
Step 5: Repeat step (4) until the size of MANRS Core stops increasing.
'''

queue = deque(list(MANRS_core))
visited = set()

while queue:
    curr_as = queue.popleft()
    visited.add(curr_as)

    for customer in p2c[curr_as]:
        if customer in MANRS_ases and customer not in visited:
            queue.append(customer)
            MANRS_core.add(customer)


'''
Step 6: Map the MANRS Core ASes to Organizations
'''

# Upzip the gzip file
gzip_file_name = '20230101.as-org2info.txt.gz'
data_file_name = '20230101.as-org2info.txt'

with gzip.open(gzip_file_name, 'rb') as file:
    with open(data_file_name, 'wb') as output_file:
        output_file.write(file.read())

# removing the new line characters
with open(data_file_name) as f:
    lines = [line.rstrip() for line in f]

id_to_name = {}
asn_to_id = {}

for line in lines:
    cells = line.split('|')

    # organization entry: org_id -> org_name
    if len(cells) == 5:
        org_id = cells[0]
        org_name = cells[2]

        id_to_name[org_id] = org_name
    
    # AS number entry: org_id -> AS numbers
    if len(cells) == 6:
        as_num = cells[0]
        org_id = cells[3]

        asn_to_id[as_num] = org_id

MANRS_orgs = set()

for asn in MANRS_core:
    org_id = asn_to_id[asn]
    org_name = id_to_name[org_id]
    MANRS_orgs.add(org_name)


'''
Step 7: Print the organization names, each separated by a newline, into output.txt
'''

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(list(MANRS_orgs)))
