import bs4
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'

# 1
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# 2
h3s = soup.find_all('h3')

# 3
def get_book_info(title_elem: bs4.element.Tag):
    parent = title_elem.parent
    price_elem = parent.find('p', attrs={'class': 'price_color'})
    return {
        'title': title_elem.find('a').get('title'),
        'price': price_elem.get_text()
    }

books = list(map(
    lambda x: get_book_info(x),
    h3s
))

for book in books:
    print(book)
    print()
