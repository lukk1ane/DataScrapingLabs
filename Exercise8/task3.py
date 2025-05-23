import requests
from bs4 import BeautifulSoup

# Define the URLs for the login page and dashboard
BASE_URL = "https://www.scrapingcourse.com"
LOGIN_PATH = f"{BASE_URL}/login/csrf"
DASHBOARD_PATH = f"{BASE_URL}/dashboard"

# Initialize session for persistent cookies and headers
with requests.Session() as session:
    # Fetch the login page to retrieve the CSRF token
    login_response = session.get(LOGIN_PATH)
    page_content = BeautifulSoup(login_response.text, "html.parser")

    # Attempt to extract the CSRF token from the page
    token_input = page_content.find("input", attrs={"name": "_token"})
    if not token_input:
        raise ValueError("Unable to locate CSRF token on login page.")

    # Construct the login payload with credentials and CSRF token
    login_payload = {
        "email": "admin@example.com",
        "password": "password",
        "_token": token_input["value"]
    }

    # Submit the login form
    auth_response = session.post(LOGIN_PATH, data=login_payload)

    # After logging in, access the dashboard page
    dashboard_response = session.get(DASHBOARD_PATH)
    dashboard_soup = BeautifulSoup(dashboard_response.text, "html.parser")

    # Parse product data from the page
    for item in dashboard_soup.select(".product-item"):
        name_element = item.select_one(".product-name")
        price_element = item.select_one(".product-price")
        if name_element and price_element:
            product_name = name_element.get_text(strip=True)
            product_price = price_element.get_text(strip=True)
            print(f"{product_name}: {product_price}")
