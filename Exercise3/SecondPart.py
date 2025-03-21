import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all quotes and authors
quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    text = quote.find('span', class_='text').string
    author = quote.find('small', class_='author').string
    print(f"Quote: {text} - Author: {author}")

# Extract the link to the "Next" page
next_page = soup.find('li', class_='next')
if next_page:
    next_page_url = next_page.find('a')['href']
    print("Next Page URL:", url + next_page_url)
else:
    print("No next page found.")

# Extract all tags associated with the quotes
tags = soup.find_all('a', class_='tag')
for tag in tags:
    print("Tag:", tag.string)