import bs4
import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com'

html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


def extract_quote_author(quote_elem: bs4.element.Tag):
    return {
        'quote': quote_elem.find('span', attrs={'class': 'text'}).get_text(),
        'author': quote_elem.find('small', attrs={'class': 'author'}).get_text()
    }


quote_elements = soup.find_all('div', attrs={'class': 'quote'})
quotes = list(map(lambda x: extract_quote_author(x), quote_elements))

print(f'quotes: {quotes}')

next_page_link = url + soup.find('li', attrs={'class': 'next'}).find('a').get('href')
print(f'\n\nnext page link: {next_page_link}')


def get_tags(quote_elem: bs4.element.Tag):
    return list(map(lambda x: x.get_text(), quote_elem.find_all('a', attrs={'class': 'tag'})))

tags = list(map(get_tags, quote_elements))
tags = list(set(tag for sublist in tags for tag in sublist))

print(f'\n\ntags: {tags}')
