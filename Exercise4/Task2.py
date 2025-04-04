import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tree = html.fromstring(response.content)

books_data = []

for article in soup.find_all('article', class_='product_pod'):
    title = article.h3.a['title']
    price = article.find('p', class_='price_color').text
    
    rating = article.p['class'][1] 
    
    book_xpath = tree.xpath(f'//article[.//a[@title="{title}"]]')[0]
    availability = book_xpath.xpath('.//p[@class="instock availability"]/text()')[0].strip()
    
    books_data.append({
        'Title': title,
        'Price': price,
        'Rating': rating,
        'Availability': availability
    })

df = pd.DataFrame(books_data)
print("Books Data:")
print(df.head())

df.to_csv('books_data.csv', index=False)
print("\nData saved to 'books_data.csv'")