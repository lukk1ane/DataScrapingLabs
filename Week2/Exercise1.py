'''
Create a script that sends a GET request to the Books to Scrape website and prints the status
code and response headers.
'''

import requests

ulr = requests.get('https://books.toscrape.com/')
response = requests.get(ulr.url)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)