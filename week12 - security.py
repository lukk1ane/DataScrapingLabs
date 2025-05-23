import requests
from bs4 import BeautifulSoup
import pickle

# task 1 and 2

def get_products(url): 
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if url.endswith("csrf"): 
        csrf_token = soup.find("input", {"name": "_token"})["value"]

        payload = {
            "_token": csrf_token,
            "email": "admin@example.com",
            "password": "password"
        }
    else: 
        payload = {
            "email": "admin@example.com",
            "password": "password"
        }

    

    # 1. Submit the login form using a POST request.
    login_response = session.post(url, data=payload)


    # access products page after login
    soup = BeautifulSoup(login_response.text, "html.parser")
    product_items = soup.find_all("div", class_="product-item")
    products = []

    # exctract titles and prices
    for item in product_items:
        prod = {
        "title": item.find(class_="product-name").text,
        "price": item.find(class_="product-price").text
        }
        products.append (prod)

    return products


login_url = "https://www.scrapingcourse.com/login"
csrf_url = "https://www.scrapingcourse.com/login/csrf"

# task 1
products_without_csrf = get_products(login_url)
print("products on url without csrf")
for prod in products_without_csrf: 
    print(prod)


# task 2 (same as task 1 but with different url, idenitfy if it login with csrf using url)
products_with_csrf = get_products(csrf_url)

print("\nproducts on url with csrf")
for prod in products_with_csrf: 
    print(prod)




# task 3

login_url = "https://www.scrapingcourse.com/login/csrf"
dashboard_url = "https://www.scrapingcourse.com/dashboard"

session = requests.Session()
login_page = session.get(login_url)

soup = BeautifulSoup(login_page.text, "html.parser")
csrf_token = soup.find("input", {"name": "_token"})["value"]

payload = {
    "_token": csrf_token,
    "email": "admin@example.com",
    "password": "password"
}


login_response = session.post(login_url, data=payload)

# Print all cookies stored in session
print("cookies stored in the session after login:")
for cookie in session.cookies:
    print(f"{cookie.name}: {cookie.value}")




# modify scrapingcoursecom_session cookie value 
cookie_name = "scrapingcoursecom_session"
if cookie_name in session.cookies:
    original_value = session.cookies.get(cookie_name)
    session.cookies.set(cookie_name, "modified")
else:
    print(f"no '{cookie_name}' cookie found")


# check if still logged in
response = session.get(dashboard_url)

# not logged in anymore
if "/login" in response.url:
    print("not logged in anymore after cookie change")
else:
    print("still logged in")


# save cookies
with open("cookies.pkl", "wb") as f:
    pickle.dump(session.cookies, f)

# load them in a new session to access the products without logging in again

new_session = requests.Session()
with open("cookies.pkl", "rb") as f:
    loaded_cookies = pickle.load(f)
    new_session.cookies.update(loaded_cookies)

response = new_session.get(dashboard_url)
print(response.url)
if "/login" in response.url:
    print("not logged in")
else:
    print("logged in after loading cookies from previous session")

