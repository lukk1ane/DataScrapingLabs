import requests
from bs4 import BeautifulSoup

# Define endpoints and login credentials
BASE_URL = "https://www.scrapingcourse.com"
LOGIN_ENDPOINT = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
user_credentials = {
    "email": "admin@example.com",
    "password": "password"
}

# Create a session to persist cookies and headers
with requests.Session() as session:
    # Authenticate the user
    login_response = session.post(LOGIN_ENDPOINT, data=user_credentials)

    if "Logout" not in login_response.text:
        print("Login failed. Please check credentials or endpoint.")
    else:
        print("Login successful. Fetching product data...")

        # Fetch the protected products page
        dashboard_response = session.get(DASHBOARD_URL)
        html = BeautifulSoup(dashboard_response.text, "html.parser")

        # Parse and display product details
        product_cards = html.select(".product-item")
        for item in product_cards:
            name = item.select_one(".product-name")
            price = item.select_one(".product-price")
            if name and price:
                print(f"{name.text.strip()}: {price.text.strip()}")
