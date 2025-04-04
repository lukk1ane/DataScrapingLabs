import requests
from bs4 import BeautifulSoup

# 1. send http request
url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 2. locating all books (h3 tags)
h3_tags = soup.find_all('h3')

print("Book Titles and Prices:")
print("----------------------")

# 3. navigate to parent to print name and price
for h3 in h3_tags:
    # get title
    title = h3.a['title']

    # navigate to parent
    parent = h3.parent

    # find price in paragraphs
    price_tag = parent.find('p', class_='price_color')
    price = price_tag.get_text()

    # print
    print(f"Title: {title}")
    print(f"Price: {price}")
    print("---")