import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

h3_tags = soup.find_all('h3')

print("Book Titles and Prices:")


for h3 in h3_tags:
    title = h3.a['title']
    
    parent = h3.parent
    
    price_tag = parent.find('p', class_='price_color')
    price = price_tag.get_text()
    
    print(f"Title: {title}")
    print(f"Price: {price}")
    print("---")