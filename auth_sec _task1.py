import requests
from bs4 import BeautifulSoup

def task1_login_no_csrf():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    })

    login_url = "https://www.scrapingcourse.com/login"
    dashboard_url = "https://www.scrapingcourse.com/dashboard"

    payload = {
        "email": "admin@example.com",
        "password": "password"
    }

    # Login
    login_response = session.post(login_url, data=payload)
    print(f"Login status code: {login_response.status_code}")
    print("Redirected to:", login_response.url)

    # dashboard
    response = session.get(dashboard_url)
    print(f"Dashboard status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div.product-item")
    print(f"Found {len(products)} product cards.")

    for product in products:
        info = product.select_one(".product-info")
        if info:
            lines = [line.strip() for line in info.stripped_strings]
            if len(lines) >= 2:
                title = lines[0]
                price = lines[1]
                print(f"{title} - {price}")
            else:
                print("Could not extract title and price.")
        else:
            print("Product info block missing.")


task1_login_no_csrf()
