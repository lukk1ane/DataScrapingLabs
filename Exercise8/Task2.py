import requests
from bs4 import BeautifulSoup

login_url = 'https://www.scrapingcourse.com/login/csrf'
products_url = 'https://www.scrapingcourse.com/dashboard'
credentials = {'email': 'admin@example.com', 'password': 'password'}

session = requests.Session()

login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')

# Extract CSRF token from the hidden input
csrf_token = soup.find('input', {'name': '_token'})
if not csrf_token:
    raise Exception("CSRF token not found")
token_value = csrf_token['value']

# Prepare login data with the correct CSRF field name
credentials = {
    'email': 'admin@example.com',
    'password': 'password',
    '_token': token_value
}

# Submit login form with CSRF token
response = session.post(login_url, data=credentials)

# Then access the protected page
products_page = session.get('https://www.scrapingcourse.com/dashboard')
soup = BeautifulSoup(products_page.text, 'html.parser')

# Extract product info
products = soup.select('.product-item')
for product in products:
    title = product.select_one('.product-name').get_text(strip=True)
    price = product.select_one('.product-price').get_text(strip=True)
    print(f'{title}: {price}')
