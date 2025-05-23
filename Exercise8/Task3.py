import requests
import pickle
import os
from bs4 import BeautifulSoup

login_url = 'https://www.scrapingcourse.com/login/csrf'
products_url = 'https://www.scrapingcourse.com/dashboard'
credentials = {'email': 'admin@example.com', 'password': 'password'}

session = requests.Session()

# Get CSRF token
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')

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

# Perform login
login_response = session.post(login_url, data=credentials)
if 'login' in login_response.url.lower():
    raise Exception("Login failed")

# Print all cookies
print("\nCookies after login:")
for cookie in session.cookies:
    print(f"{cookie.name} (Domain: {cookie.domain}): {cookie.value[:50]}...")

# Modify the session cookie specifically
target_cookie = 'scrapingcoursecom_session'
if target_cookie in session.cookies:
    original_value = session.cookies[target_cookie]
    session.cookies.set(target_cookie, 'tampered_value', domain='www.scrapingcourse.com', path='/')
    print(f"\nModified {target_cookie} from {original_value[:50]}... to 'tampered_value'")
else:
    print(f"\n{target_cookie} not found in cookies")

# Try to access protected page after modification
response = session.get(products_url)
if 'login' in response.url.lower():
    print("\nAccess denied after cookie tampering (expected)")
else:
    print("\nStill logged in after cookie tampering (unexpected)")

# Save cookies to file
cookie_file = 'scraping_course_cookies.pkl'
try:
    with open(cookie_file, 'wb') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)
    print(f"\nCookies saved to {os.path.abspath(cookie_file)}")
except Exception as e:
    print(f"\nError saving cookies: {e}")

# Create new session and load cookies
new_session = requests.Session()
try:
    with open(cookie_file, 'rb') as f:
        cookies = pickle.load(f)
        new_session.cookies.update(requests.utils.cookiejar_from_dict(cookies))
    print("\nCookies loaded successfully")

    # Verify loaded cookies
    print("\nLoaded cookies:")
    for cookie in new_session.cookies:
        print(f"{cookie.name}: {cookie.value[:50]}...")

    # Test access with loaded cookies
    response = new_session.get(products_url)
    if 'login' in response.url.lower():
        print("\nAccess denied with loaded cookies")
    else:
        print("\nAccess granted with loaded cookies")
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select('.product-item') or soup.select('.product')
        if products:
            print("\nProducts:")
            for product in products[:3]:  # Print first 3
                title = product.select_one('.product-name, .title, .name')
                price = product.select_one('.product-price, .price')
                if title and price:
                    print(f"{title.get_text(strip=True)}: {price.get_text(strip=True)}")
        else:
            print("\nNo products found - check selectors")
except Exception as e:
    print(f"\nError loading cookies: {e}")