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

import bz2

bz2_file_name = '20221001.as-rel.txt.bz2'

p2c = defaultdict(list)

for byte_line in bz2.BZ2File(bz2_file_name, 'rb'):
    # convert byte string into regular string line
    string_line = byte_line.decode("utf-8").strip()

    cells = string_line.split('|')

    # provider-customer link
    if cells[-1] == '-1':
        p2c[cells[0]].append(cells[1])

# Load AS number
with open('input.txt') as file:
    asnum = file.read()

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(p2c[asnum]))
