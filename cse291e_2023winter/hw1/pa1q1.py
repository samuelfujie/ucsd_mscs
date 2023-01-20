#!/usr/bin/env python3

'''
=============================================================================
Created By  : Samuel Fu
Created Date: Fri Jan 20 11:31:54 PST 2023
Class: CSE 291E
Professor: KC Claffy
=============================================================================
'''

import json
import requests

# Parameters
url = 'https://api.spoofer.caida.org/sessions'

timestamp_before = '2023-01-03'
timestamp_after = '2023-01-01'

country = 'usa'
page = 1

# API Call
current_item_count = 0
current_item_list = []

while True:
    # Make API call
    query = {
        'timestamp[before]': timestamp_before,
        'timestamp[after]': timestamp_after,
        'country': country,
        'page': page
    }
    response = requests.get(url, params=query)
    json_response = response.json()

    total_item_count = json_response['hydra:totalItems']

    # Check if all items are collected
    if total_item_count > current_item_count:
        # Append items on current page to item list
        current_item_list += json_response['hydra:member']
        current_item_count = len(current_item_list)

        # Update page number to be next page
        page += 1
    else:
        break

# Dump list into a JSON file
out_file = open("output.json", "w")
json.dump(current_item_list, out_file)
out_file.close()
