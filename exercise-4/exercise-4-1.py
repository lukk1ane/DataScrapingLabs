import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    for book in soup.find_all('h3'):
        parent = book.parent.parent

        title = book.a['title']

        price = parent.find('p', class_='price_color').text

        print(f'Title: {title}, Price: {price}')
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
