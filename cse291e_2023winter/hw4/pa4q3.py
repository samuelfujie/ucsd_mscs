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


isp_csv_file_name = 'manrs_isp_20230221.csv'
cdn_csv_file_name = 'manrs_cdn_20230221.csv'

rel_bz2_file_name = '20230201.as-rel.txt.bz2'

MANRS_ases = set()
MANRS_core = set()

t1_providers = set()

p2c = defaultdict(list)


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


for byte_line in bz2.BZ2File(rel_bz2_file_name, 'rb'):
    # convert byte string into regular string line
    string_line = byte_line.decode("utf-8").strip()

    cells = string_line.split('|')

    # provider-customer link
    if cells[-1] == '-1':
        p2c[cells[0]].append(cells[1])

        # if cells[1] == '268218':
        #     print("======== Provider: {} | Customer: {}".format(cells[0], cells[1]))


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

while queue:
    curr_as = queue.popleft()
    # BFS
    for customer in p2c[curr_as]:
        if customer in MANRS_ases and customer not in MANRS_core:
            queue.append(customer)
            MANRS_core.add(customer)

# if '268218' in MANRS_core:
#     print("----------> 268218 FOUND IN CORE!!!!!!")
'''
Step 6: Find all direct customers of the MANRS Core, 
        i.e, of ASes in the MANRS core.
'''

direct_customers = set()

for asn in MANRS_core:
    for customer in p2c[asn]:
        # if asn == '52892':
        #     print(p2c[asn])
        direct_customers.add(customer)


'''
Step 7: Print the AS numbers, each separated by a newline, into output.txt.
'''

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(list(direct_customers)))
print(len(direct_customers))
