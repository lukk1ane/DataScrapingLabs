from itertools import product

import bs4.element
from bs4 import BeautifulSoup
import lxml
import requests

url = 'https://zoommer.ge/mobiluri-telefonebi-google-c968s'

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

container = soup.select_one('#__next > div > div.sc-4a7e9996-0.kAhAWY > div > div > div.sc-1e9b893c-0.bsbbwz > div.sc-1e9b893c-12.dQsAMy')
def parse_elements(elem: bs4.element.Tag):
    url = 'https://zoommer.ge/'+ elem.select_one('div > a').get('href')
    price = elem.select_one('h4').get_text()
    name = elem.find('div',attrs={'class':'kVfima'}).select_one('a').get_text()
    return {
        'url': url,
        'price': price,
        'name': name
    }
products = list(map(
    lambda x: parse_elements(x),
    container.children
))

for p in products:
    print(p)