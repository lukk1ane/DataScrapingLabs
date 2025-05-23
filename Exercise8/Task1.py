
import requests
from bs4 import BeautifulSoup

login_url = 'https://www.scrapingcourse.com/login'
products_url = 'https://www.scrapingcourse.com/dashboard'
credentials = {'email': 'admin@example.com', 'password': 'password'}

session = requests.Session()
response = session.post(login_url, data=credentials)

# Access protected page
products_page = session.get(products_url)
soup = BeautifulSoup(products_page.text, 'html.parser')

# Extract titles and prices based on updated HTML
products = soup.select('.product-item')
for product in products:
    title = product.select_one('.product-name').get_text(strip=True)
    price = product.select_one('.product-price').get_text(strip=True)
    print(f'{title}: {price}')
