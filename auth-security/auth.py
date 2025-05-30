import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://www.scrapingcourse.com/login"
PRODUCTS_URL = "https://www.scrapingcourse.com/products"
USERNAME = "demo"
PASSWORD = "demo"

session = requests.Session()

session.get(LOGIN_URL)

payload = {
    "username": USERNAME,
    "password": PASSWORD,
}
response = session.post(LOGIN_URL, data=payload)

products_resp = session.get(PRODUCTS_URL)
soup = BeautifulSoup(products_resp.text, "html.parser")

for product in soup.select('.product'):
    title = product.select_one('.title').get_text(strip=True)
    price = product.select_one('.price').get_text(strip=True)
    print(f"{title}: {price}")


CSRF_LOGIN_URL = "https://www.scrapingcourse.com/login/csrf"
CSRF_PRODUCTS_URL = "https://www.scrapingcourse.com/products/csrf"

session = requests.Session()

# 2
login_page = session.get(CSRF_LOGIN_URL)
soup = BeautifulSoup(login_page.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf_token"})["value"]


payload = {
    "username": USERNAME,
    "password": PASSWORD,
    "csrf_token": csrf_token
}
response = session.post(CSRF_LOGIN_URL, data=payload)

products_resp = session.get(CSRF_PRODUCTS_URL)
soup = BeautifulSoup(products_resp.text, "html.parser")

for product in soup.select('.product'):
    title = product.select_one('.title').get_text(strip=True)
    price = product.select_one('.price').get_text(strip=True)
    print(f"{title}: {price}")

# 3

import pickle

print("Cookies after login:")
for cookie in session.cookies:
    print(cookie.name, cookie.value)

for cookie in session.cookies:
    if cookie.name == 'session':
        session.cookies.set(cookie.name, 'invalid_value')

response = session.get(CSRF_PRODUCTS_URL)
print("Access with modified cookie:", "logged in" if "Logout" in response.text else "not logged in")

with open("cookies.pkl", "wb") as f:
    pickle.dump(session.cookies, f)

new_session = requests.Session()
with open("cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    new_session.cookies.update(cookies)

response = new_session.get(CSRF_PRODUCTS_URL)
print("Access with loaded cookies:", "logged in" if "Logout" in response.text else "not logged in")


