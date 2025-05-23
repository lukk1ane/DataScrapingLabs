import requests
from bs4 import BeautifulSoup

# Target URLs
BASE = "https://www.scrapingcourse.com"
LOGIN_PAGE = f"{BASE}/login/csrf"
DASHBOARD = f"{BASE}/dashboard"

# User credentials
auth_data = {
    "email": "admin@example.com",
    "password": "password"
}

# Start session
with requests.Session() as client:
    # Load login page to retrieve CSRF token
    login_resp = client.get(LOGIN_PAGE)
    parser = BeautifulSoup(login_resp.text, "html.parser")

    # Locate the CSRF token input field
    token_input = parser.find("input", attrs={"name": "_token"})
    if not token_input:
        raise RuntimeError("CSRF token input field is missing from the login page.")

    # Add token to login payload
    auth_data["_token"] = token_input["value"]

    # Send login request with CSRF token
    login_result = client.post(LOGIN_PAGE, data=auth_data)

    # Request the protected resource
    dashboard_resp = client.get(DASHBOARD)
    parsed_html = BeautifulSoup(dashboard_resp.text, "html.parser")

    # Find and display product details
    for item in parsed_html.select(".product-item"):
        name_tag = item.select_one(".product-name")
        price_tag = item.select_one(".product-price")
        if name_tag and price_tag:
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            print(f"{name}: {price}")
