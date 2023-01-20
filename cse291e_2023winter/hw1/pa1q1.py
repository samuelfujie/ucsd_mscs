import requests

### Parameters ###
url = 'https://api.spoofer.caida.org/sessions'

timestamp_before = '2023-01-03'
timestamp_after = '2023-01-01'

country = 'usa'

### API Call ###
query = {'timestamp[before]':timestamp_before, 'timestamp[after]':timestamp_after, 'country':country}
response = requests.get(url, params=query)
print(response.json())