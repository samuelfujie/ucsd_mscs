#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Fri Jan 20 11:31:54 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

import csv
import dateutil.parser
import json

# Initiaze set of ASes who claimed performing SAV
as_with_sav = set()

# Process CSV file
with open('manrs.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)

    for row in data:
        if row['Action 2: Anti-spoofing'] == 'Yes':
            # Update the AS set
            asns = row['ASNs'].split(";")
            as_with_sav.update(asns)


# Load from spoofer cache
cache_file = 'spoofer_cache.json'

with open(cache_file) as file:
    file_contents = file.read()

session_list = json.loads(file_contents)

# Load country code
with open('input.txt') as file:
    country = file.read()

# Process the cache
ipv4_to_timestamp = {}

for session in session_list:
    # Filter invalid countries
    if session['country'] != country:
        continue

    # Filter invalid results
    if session['routedspoof'] == 'unknown':
        continue

    # Filter ASes who did not make the claim
    if session['asn4'] not in as_with_sav:
        continue

    ipv4 = session['client4']
    # ISO-8601 date
    timestamp = session['timestamp']
    date = dateutil.parser.parse(timestamp)

    if ipv4 in ipv4_to_timestamp:
        prev_date = ipv4_to_timestamp[ipv4]

        # if the session is later than stored
        if (date - prev_date).total_seconds() > 0:
            # Update the timestamp if not filter spoof packet
            if session['routedspoof'] == 'received':
                ipv4_to_timestamp[ipv4] = date
            # Remove from dict if it fixed the filter
            else:
                del ipv4_to_timestamp[ipv4]
    else:
        # Store in dict if it does not filter spoof packet
        if session['routedspoof'] == 'received':
            ipv4_to_timestamp[ipv4] = date

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(ipv4_to_timestamp.keys()))
