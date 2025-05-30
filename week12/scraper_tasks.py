import requests
from bs4 import BeautifulSoup
import pickle
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://www.scrapingcourse.com/'
}

BASE_URL = 'https://www.scrapingcourse.com'
LOGIN_URL_1 = f'{BASE_URL}/login'
LOGIN_URL_2_3 = f'{BASE_URL}/login/csrf'
PRODUCTS_URL = f'{BASE_URL}/products'
COOKIE_FILE = 'cookies_homework.pkl'

USERNAME_FIELD_NAME = 'username'
PASSWORD_FIELD_NAME = 'password'
CSRF_TOKEN_FIELD_NAME = 'csrf_token'

CREDENTIALS = {
    USERNAME_FIELD_NAME: 'admin',
    PASSWORD_FIELD_NAME: 'admin'
}

def print_products_or_preview(page_text, task_label):
    soup = BeautifulSoup(page_text, 'html.parser')
    cards = soup.select(".card")
    print(f"\n[{task_label}: Products Attempt]")
    if not cards or "<title>Not Found</title>" in page_text or "<title>Login</title>" in page_text:
        print("No products found or login likely failed. Page preview:")
        print(page_text[:1000])
        return False
    
    for product in cards:
        title_element = product.select_one(".card-title")
        price_element = product.select_one(".card-text")
        title = title_element.text.strip() if title_element else "N/A"
        price = "N/A"
        if price_element:
            price_text = price_element.text.strip()
            if "Price:" in price_text:
                price = price_text.split("Price:")[1].strip()
            else:
                price = price_text
        if title != "N/A":
            print(f"{title}: {price}")
    return True

def task_1():
    print("\n--- Task 1 ---")
    session = requests.Session()
    try:
        session.get(LOGIN_URL_1, headers=HEADERS, timeout=10)
        login_post_response = session.post(LOGIN_URL_1, data=CREDENTIALS, headers=HEADERS, timeout=10)
        print(f"[Task 1] Login POST URL: {login_post_response.url}, Status: {login_post_response.status_code}")
        products_response = session.get(PRODUCTS_URL, headers=HEADERS, timeout=10)
        print_products_or_preview(products_response.text, "Task 1")
    except requests.exceptions.RequestException as e:
        print(f"[Task 1] Request Exception: {e}")

def task_2():
    print("\n--- Task 2 ---")
    session = requests.Session()
    try:
        response = session.get(LOGIN_URL_2_3, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': CSRF_TOKEN_FIELD_NAME})

        if not csrf_input or not csrf_input.get('value'):
            print(f"[Task 2] CSRF token '{CSRF_TOKEN_FIELD_NAME}' not found. Page preview:")
            print(response.text[:1000])
            return

        csrf_token = csrf_input['value']
        payload = CREDENTIALS.copy()
        payload[CSRF_TOKEN_FIELD_NAME] = csrf_token
        
        login_post_response = session.post(LOGIN_URL_2_3, data=payload, headers=HEADERS, timeout=10)
        print(f"[Task 2] Login POST URL: {login_post_response.url}, Status: {login_post_response.status_code}")
        products_response = session.get(PRODUCTS_URL, headers=HEADERS, timeout=10)
        print_products_or_preview(products_response.text, "Task 2")
    except requests.exceptions.RequestException as e:
        print(f"[Task 2] Request Exception: {e}")


def task_3():
    print("\n--- Task 3 ---")
    session = requests.Session()
    login_successful_for_cookie_test = False
    try:
        response = session.get(LOGIN_URL_2_3, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': CSRF_TOKEN_FIELD_NAME})

        if not csrf_input or not csrf_input.get('value'):
            print(f"[Task 3] CSRF token '{CSRF_TOKEN_FIELD_NAME}' for initial login not found. Page preview:")
            print(response.text[:1000])
        else:
            csrf_token = csrf_input['value']
            payload = CREDENTIALS.copy()
            payload[CSRF_TOKEN_FIELD_NAME] = csrf_token
            login_post_response = session.post(LOGIN_URL_2_3, data=payload, headers=HEADERS, timeout=10)
            print(f"[Task 3] Initial Login POST URL: {login_post_response.url}, Status: {login_post_response.status_code}")
            if not ("/login" in login_post_response.url.lower() and login_post_response.url != LOGIN_URL_2_3):
                temp_products_response = session.get(PRODUCTS_URL, headers=HEADERS, timeout=10)
                if not ("<title>Not Found</title>" in temp_products_response.text or "<title>Login</title>" in temp_products_response.text):
                    login_successful_for_cookie_test = True
                    print("[Task 3] Initial login seems plausible for cookie test.")
                else:
                    print("[Task 3] Initial login failed to grant access to products.")
            else:
                print("[Task 3] Initial login redirected back to login.")

        print("\n[Task 3: Cookies After Login Attempt]")
        if not session.cookies:
            print("No cookies in session.")
        for cookie in session.cookies:
            print(f"{cookie.name}: {cookie.value[:50]}...")

        if login_successful_for_cookie_test:
            print("\n[Task 3] Proceeding with cookie manipulation as login seemed plausible.")
            tampered_session = requests.Session()
            tampered_session.headers.update(HEADERS)
            for cookie in session.cookies:
                tampered_session.cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
            
            session_cookie_name_to_tamper = None
            for ck_name in ['scrapingcoursecom_session', 'session']:
                if ck_name in tampered_session.cookies:
                    session_cookie_name_to_tamper = ck_name
                    break
            
            if session_cookie_name_to_tamper:
                print(f"Tampering cookie: {session_cookie_name_to_tamper}")
                tampered_session.cookies.set(session_cookie_name_to_tamper, 'tampered_value_123')
                products_response_tampered = tampered_session.get(PRODUCTS_URL, headers=HEADERS, timeout=10)
                print_products_or_preview(products_response_tampered.text, "Task 3 - With Tampered Cookie")
            else:
                print("[Task 3] Could not identify a primary session cookie to tamper.")

            with open(COOKIE_FILE, 'wb') as f:
                pickle.dump(session.cookies, f)
            print(f"\n[Task 3] Cookies saved to {COOKIE_FILE}")

            new_session_loaded = requests.Session()
            new_session_loaded.headers.update(HEADERS)
            with open(COOKIE_FILE, 'rb') as f:
                cookies_loaded = pickle.load(f)
                new_session_loaded.cookies.update(cookies_loaded)
            print("[Task 3] Cookies loaded into new session.")
            products_response_loaded = new_session_loaded.get(PRODUCTS_URL, headers=HEADERS, timeout=10)
            print_products_or_preview(products_response_loaded.text, "Task 3 - With Loaded Cookies")


    except requests.exceptions.RequestException as e:
        print(f"[Task 3] Request Exception: {e}")
    finally:
        if os.path.exists(COOKIE_FILE):
            os.remove(COOKIE_FILE)
            print(f"[Task 3] Cleaned up {COOKIE_FILE}")

if __name__ == '__main__':
    task_1()
    task_2()
    task_3()
    print("\nScript finished.")
