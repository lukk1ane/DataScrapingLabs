import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

url = 'http://quotes.toscrape.com'

try:
    response = requests.get(url)
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

# Task 1
quotes = soup.find_all('div', class_='quote')

print("Quotes and Authors:")
for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    print(f"- Quote: {text}\n  Author: {author}\n")

# Task 2
next_page_link = soup.find('li', class_='next')
if next_page_link:
    next_page_url = url + next_page_link.find('a')['href']
    print(f"Next Page URL: {next_page_url}")
else:
    print("No Next Page Link Found")

# Task 3
tags = soup.find_all('a', class_='tag')

print("\nTags:")
for tag in tags:
    print(f"- {tag.text}")
