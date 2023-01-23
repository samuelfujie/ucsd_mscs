#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Fri Jan 20 11:31:54 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

import dateutil.parser
import json

# Load from spoofer cache
cache_file = 'spoofer_cache.json'

with open(cache_file) as file:
    file_contents = file.read()

session_list = json.loads(file_contents)

# Load country code
with open('input.txt') as file:
    country = file.read()

# Process the cache
ipv6_to_timestamp = {}

for session in session_list:
    # Filter invalid countries
    if session['country'] != country:
        continue

    # Filter invalid results
    if session['routedspoof6'] == 'unknown':
        continue

    ipv6 = session['client6']
    # ISO-8601 date
    timestamp = session['timestamp']
    date = dateutil.parser.parse(timestamp)

    if ipv6 in ipv6_to_timestamp:
        prev_date = ipv6_to_timestamp[ipv6]

        # if the session is later than stored
        if (date - prev_date).total_seconds() > 0:
            # Update the timestamp if not filter spoof packet
            if session['routedspoof6'] == 'received':
                ipv6_to_timestamp[ipv6] = date
            # Remove from dict if it fixed the filter
            else:
                del ipv6_to_timestamp[ipv6]
    else:
        # Store in dict if it does not filter spoof packet
        if session['routedspoof6'] == 'received':
            ipv6_to_timestamp[ipv6] = date

# Dump to output.txt
with open('output.txt', mode='wt', encoding='utf-8') as file:
    file.write('\n'.join(ipv6_to_timestamp.keys()))
