import requests
from bs4 import BeautifulSoup
import pickle

URL = "https://www.scrapingcourse.com/login"
URL_CSRF = "https://www.scrapingcourse.com/login/csrf"
URL_PROD = "https://www.scrapingcourse.com/dashboard"
EMAIL = "admin@example.com"
PASS = "password"
PRODUCTS_CONTAINER_ID = "product-grid"


def save_cookies(session, filename):
    jar = session.cookies
    with open(filename, "wb") as f:
        pickle.dump(jar, f)


def load_cookies(session, filename):
    with open(filename, "rb") as f:
        cookies = pickle.load(f)
        session.cookies.update(cookies)


def extract_product_data(node):
    products_container = node.find("div", attrs={"id": PRODUCTS_CONTAINER_ID})
    products = products_container.find_all("div", class_="product-item")
    _data = []

    for product in products:
        info = product.find("div", class_="product-info").find_all("span")
        title = info[0].text
        price = info[1].text
        _data.append({"title": title, "price": price})
    return _data


# task 1

payload = {
    "email": EMAIL,
    "password": PASS
}

res = requests.post(URL, data=payload)
doc = BeautifulSoup(res.text, "html.parser")

data = extract_product_data(doc)
for item in data:
    print(item)

# task 2
session = requests.session()
res = session.get(URL_CSRF)
doc = BeautifulSoup(res.text, "html.parser")
token_input = doc.find("input", attrs={"name": "_token"})
token = token_input.get("value")

payload = {
    "_token": token,
    "email": EMAIL,
    "password": PASS,
}

res = session.post(URL_CSRF, data=payload)
doc = BeautifulSoup(res.text, "html.parser")
data = extract_product_data(doc)
for item in data:
    print(item)

# task 3
with requests.session() as session:
    res = session.get(URL_CSRF)
    doc = BeautifulSoup(res.text, "html.parser")
    token_input = doc.find("input", attrs={"name": "_token"})
    token = token_input.get("value")

    payload = {
        "_token": token,
        "email": EMAIL,
        "password": PASS,
    }

    res = session.post(URL_CSRF, data=payload)
    doc = BeautifulSoup(res.text, "html.parser")
    data = extract_product_data(doc)
    save_cookies(session, "cookies")
    session.cookies.clear_session_cookies()
    res = session.get(URL_PROD)
    print(doc)

with requests.session() as session:
    load_cookies(session, "cookies")
    res = session.get(URL_PROD)
    doc = BeautifulSoup(res.text, "html.parser")
    data = extract_product_data(doc)
    for item in data:
        print(item)
