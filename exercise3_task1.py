import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes_data = []
for quote_div in soup.find_all("div", class_="quote"):
    quote_text = quote_div.find("span", class_="text").get_text()
    author = quote_div.find("small", class_="author").get_text()
    quotes_data.append({"quote": quote_text, "author": author})

next_page = soup.find("li", class_="next")
next_page_link = url + next_page.a["href"] if next_page else None

tags = [tag.get_text() for tag in soup.select(".tag-item > a")]

print("\nAll Quotes and Their Authors:")
for item in quotes_data:
    print(f'➤ "{item["quote"]}" — {item["author"]}')

print("\nNext Page Link:", next_page_link if next_page_link else "No Next Page")

print("\nTags Associated with Quotes:", ", ".join(tags))



## examle with regex

print("example of regex code")

import re
import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract quotes that contain the word "life"
quotes_life = []
for quote_div in soup.find_all("div", class_="quote"):
    quote_text = quote_div.find("span", class_="text").get_text()
    if re.search(r'\blife\b', quote_text, re.IGNORECASE):  # Word boundary for exact match
        author = quote_div.find("small", class_="author").get_text()
        quotes_life.append({"quote": quote_text, "author": author})

# Print Quotes Containing "life"
for item in quotes_life:
    print(f'➤ "{item["quote"]}" — {item["author"]}')
