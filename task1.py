import requests
from bs4 import BeautifulSoup


url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

books = soup.find_all('h3')
for book in books:
 
    title = book.a['title']
    
    parent = book.parent
    price = parent.find('p', class_='price_color').text
    
    print(f"Title: {title} | Price: {price}")