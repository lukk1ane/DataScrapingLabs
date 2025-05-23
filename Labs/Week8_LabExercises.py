import requests
from bs4 import BeautifulSoup
import pickle


# ---------- Task 1 ----------
def task1_simple_login():
    session = requests.Session()
    login_url = "https://www.scrapingcourse.com/login"
    products_url = "https://www.scrapingcourse.com/products"

    credentials = {
        "username": "demo",
        "password": "demo"
    }

    response = session.post(login_url, data=credentials)

    if "Welcome" in response.text:
        products_page = session.get(products_url)
        soup = BeautifulSoup(products_page.text, "html.parser")
        for product in soup.select("div.card"):
            title = product.select_one("h4").text.strip()
            price = product.select_one("p").text.strip()
            print(f"{title} - {price}")
    else:
        print("Login failed.")


# ---------- Task 2 ----------
def task2_csrf_login():
    session = requests.Session()
    login_url = "https://www.scrapingcourse.com/login/csrf"
    products_url = "https://www.scrapingcourse.com/products"

    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    payload = {
        "username": "demo",
        "password": "demo",
        "csrf_token": csrf_token
    }

    response = session.post(login_url, data=payload)

    if "Welcome" in response.text:
        products_page = session.get(products_url)
        soup = BeautifulSoup(products_page.text, "html.parser")
        for product in soup.select("div.card"):
            title = product.select_one("h4").text.strip()
            price = product.select_one("p").text.strip()
            print(f"{title} - {price}")
    else:
        print("Login failed.")


# ---------- Task 3 ----------
def task3_cookie_handling():
    session = requests.Session()
    login_url = "https://www.scrapingcourse.com/login/csrf"
    products_url = "https://www.scrapingcourse.com/products"

    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    payload = {
        "username": "demo",
        "password": "demo",
        "csrf_token": csrf_token
    }

    session.post(login_url, data=payload)

    for cookie in session.cookies:
        print(f"{cookie.name} = {cookie.value}")

    session.cookies.set("session", "invalidsession123")

    response = session.get(products_url)
    if "Products" in response.text:
        print("Still logged in with modified cookie.")
    else:
        print("Access denied after modifying cookie.")

    with open("cookies.pkl", "wb") as f:
        pickle.dump(session.cookies, f)

    new_session = requests.Session()
    with open("cookies.pkl", "rb") as f:
        new_session.cookies.update(pickle.load(f))

    restored_page = new_session.get(products_url)
    if "Products" in restored_page.text:
        print("Accessed products with restored cookies.")
    else:
        print("Could not access products with restored cookies.")

if __name__ == "__main__":
    task1_simple_login()
    task2_csrf_login()
    task3_cookie_handling()
