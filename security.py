import requests
from bs4 import BeautifulSoup
import json

"""Task 1: Simple Login"""
LOGIN_URL = "https://www.scrapingcourse.com/login"
PRODUCTS_URL = "https://www.scrapingcourse.com/products"
USERNAME = "demo"
PASSWORD = "demo"

print("--- Task 1: Simple Login ---")

# Initialize a session
session = requests.Session()

# 1. Submit the login form
login_payload = {
    "email": USERNAME,  # Corrected field name (might be 'email' instead of 'username')
    "password": PASSWORD,
}

print(f"Attempting to log in to {LOGIN_URL}...")
response = session.post(LOGIN_URL, data=login_payload)

# Check if login succeeded
if response.status_code == 200 and "products" in response.text.lower():
    print("Login successful!")

    # 2. Access the protected products page
    products_response = session.get(PRODUCTS_URL)
    soup = BeautifulSoup(products_response.text, 'html.parser')

    # 3. Extract and print product titles and prices
    print("\n--- Products ---")
    product_cards = soup.find_all('div', class_='card')
    for card in product_cards:
        title = card.find('h4', class_='card-title').get_text(strip=True) if card.find('h4', class_='card-title') else "N/A"
        price = card.find('h5').get_text(strip=True) if card.find('h5') else "N/A"
        print(f"Title: {title}, Price: {price}")
else:
    print("Login failed. Check form fields or credentials.")
    print("Response URL:", response.url)
    print("Response Status Code:", response.status_code)

"""Task 2: CSRF Token Login"""
CSRF_LOGIN_URL = "https://www.scrapingcourse.com/login/csrf"

print("\n--- Task 2: CSRF Token Login ---")

# Initialize a new session
csrf_session = requests.Session()

# 1. Get the CSRF token
csrf_response = csrf_session.get(CSRF_LOGIN_URL)
soup = BeautifulSoup(csrf_response.text, 'html.parser')
csrf_token = soup.find('input', {'name': '_token'})['value'] if soup.find('input', {'name': '_token'}) else None

if not csrf_token:
    print("Error: CSRF token not found.")
else:
    print(f"CSRF Token: {csrf_token}")

    # 2. Submit login with CSRF token
    csrf_payload = {
        "email": USERNAME,  # Corrected field name (might be 'email' instead of 'username')
        "password": PASSWORD,
        "_token": csrf_token,
    }

    login_response = csrf_session.post(CSRF_LOGIN_URL, data=csrf_payload)

    # Check if login succeeded
    if login_response.status_code == 200 and "products" in login_response.text.lower():
        print("CSRF Login successful!")

        # 3. Extract and print products
        products_response = csrf_session.get(PRODUCTS_URL)
        soup = BeautifulSoup(products_response.text, 'html.parser')

        print("\n--- Products (CSRF Login) ---")
        product_cards = soup.find_all('div', class_='card')
        for card in product_cards:
            title = card.find('h4', class_='card-title').get_text(strip=True) if card.find('h4', class_='card-title') else "N/A"
            price = card.find('h5').get_text(strip=True) if card.find('h5') else "N/A"
            print(f"Title: {title}, Price: {price}")
    else:
        print("CSRF Login failed. Check token or credentials.")
        print("Response URL:", login_response.url)

"""Task 3: Cookie Management"""
print("\n--- Task 3: Cookie Management and Manipulation ---")

# Use the session from Task 2 (csrf_session)
if 'csrf_session' in globals():
    # 1. Print all cookies
    print("\n--- Cookies in the current session (after CSRF login) ---")
    for cookie in csrf_session.cookies:
        print(f"Name: {cookie.name}, Value: {cookie.value}, Domain: {cookie.domain}")

    # 2. Modify a cookie and test access
    session_cookie_name = None
    for cookie in csrf_session.cookies:
        if "session" in cookie.name.lower():
            session_cookie_name = cookie.name
            break

    if session_cookie_name:
        modified_session = requests.Session()
        # Copy all cookies
        for cookie in csrf_session.cookies:
            modified_session.cookies.set(cookie.name, cookie.value, domain=cookie.domain)
        # Modify the session cookie
        modified_session.cookies.set(session_cookie_name, "invalid_value", domain=".scrapingcourse.com")

        print(f"\nAttempting to access {PRODUCTS_URL} with modified cookie...")
        response_modified = modified_session.get(PRODUCTS_URL)
        if "products" in response_modified.text.lower():
            print("Result: Still logged in (cookie modification did not work).")
        else:
            print("Result: Session invalidated (cookie modification worked).")

    # 3. Save and load cookies
    COOKIE_FILE = "cookies.json"
    cookies_to_save = [{"name": c.name, "value": c.value, "domain": c.domain} for c in csrf_session.cookies]

    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies_to_save, f)
    print(f"\nCookies saved to {COOKIE_FILE}.")

    # Load cookies into a new session
    new_session = requests.Session()
    with open(COOKIE_FILE, 'r') as f:
        cookies_loaded = json.load(f)
        for cookie in cookies_loaded:
            new_session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    print(f"Attempting to access {PRODUCTS_URL} with loaded cookies...")
    response_loaded = new_session.get(PRODUCTS_URL)
    if "products" in response_loaded.text.lower():
        print("Result: Successfully accessed products page with loaded cookies.")
    else:
        print("Result: Failed to access products page (cookies may have expired).")
else:
    print("Error: CSRF session not found. Run Task 2 first.")