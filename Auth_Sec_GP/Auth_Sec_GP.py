"""
This script:
1. Logs in (basic and CSRF) to https://www.scrapingcourse.com
2. Scrapes the protected dashboard for product names & prices
3. Inspects, tampers, saves & reloads cookies

Usage:
    python3 Auth_Sec_GP.py
"""

import requests
from bs4 import BeautifulSoup
import pickle
import os
import sys

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------

BASE_URL      = "https://www.scrapingcourse.com"
LOGIN_URL     = BASE_URL + "/login"
CSRF_LOGIN    = BASE_URL + "/login/csrf"
DEMO_EMAIL    = "admin@example.com"
DEMO_PASSWORD = "password"
COOKIE_JAR    = "cookies.pkl"

# ------------------------------------------------------------------------------
# SELECTORS —  from DevTools inspection
# ------------------------------------------------------------------------------

PRODUCT_CONTAINER_SEL = "div.product-item"
TITLE_SEL             = "span.product-name"
PRICE_SEL             = "span.product-price.text-slate-600"


# ------------------------------------------------------------------------------
# UTILITIES
# ------------------------------------------------------------------------------

def dump_html(filename, html):
    """Write full HTML to a file for offline inspection (optional)."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {filename} for inspection.")


def scrape_and_print(soup):
    """Scrape using the configured selectors and print results."""
    products = soup.select(PRODUCT_CONTAINER_SEL)
    if not products:
        print(f"⚠️  No products found with selector '{PRODUCT_CONTAINER_SEL}'.", file=sys.stderr)
        return
    for card in products:
        title_el = card.select_one(TITLE_SEL)
        price_el = card.select_one(PRICE_SEL)
        title = title_el.get_text(strip=True) if title_el else "<no title>"
        price = price_el.get_text(strip=True) if price_el else "<no price>"
        print(f"{title:30s} — {price}")


# ------------------------------------------------------------------------------
# TASK 1: Basic Login & Scrape
# ------------------------------------------------------------------------------

def task1_basic_login_and_scrape():
    print("\n>>> Task 1: Basic Login & Scrape")
    with requests.Session() as s:
        # 1) POST credentials
        r = s.post(LOGIN_URL, data={"email": DEMO_EMAIL, "password": DEMO_PASSWORD}, allow_redirects=True)
        r.raise_for_status()

        # 2) GET the protected dashboard (follow redirect)
        protected = r if r.url != LOGIN_URL else s.get(LOGIN_URL)
        protected.raise_for_status()

        # (Optional) dump_html("success.html", protected.text)

        # 3) Scrape & print
        soup = BeautifulSoup(protected.text, "html.parser")
        scrape_and_print(soup)


# ------------------------------------------------------------------------------
# TASK 2: CSRF-protected Login & Scrape
# ------------------------------------------------------------------------------

def task2_csrf_login_and_scrape():
    print("\n>>> Task 2: CSRF Login & Scrape")
    with requests.Session() as s:
        # 1) GET form to retrieve CSRF token
        r = s.get(CSRF_LOGIN)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # 2) auto-detect hidden CSRF input
        hidden = next(
            (inp for inp in soup.find_all("input", type="hidden")
             if "csrf" in inp.get("name", "").lower() or "token" in inp.get("name", "").lower()),
            None
        )
        if not hidden:
            print("⚠️  CSRF token input not found.", file=sys.stderr)
            return

        token_name, token_val = hidden["name"], hidden["value"]

        # 3) POST credentials + token
        payload = {"email": DEMO_EMAIL, "password": DEMO_PASSWORD, token_name: token_val}
        post = s.post(CSRF_LOGIN, data=payload, allow_redirects=True)
        post.raise_for_status()

        # 4) GET the protected dashboard
        protected = post if post.url != CSRF_LOGIN else s.get(CSRF_LOGIN)
        protected.raise_for_status()

        # 5) Scrape & print
        soup2 = BeautifulSoup(protected.text, "html.parser")
        scrape_and_print(soup2)


# ------------------------------------------------------------------------------
# TASK 3: Cookie Inspection & Persistence
# ------------------------------------------------------------------------------

def task3_cookie_inspection_and_persistence():
    print("\n>>> Task 3: Cookie Inspection & Persistence")
    s = requests.Session()
    s.post(LOGIN_URL, data={"email": DEMO_EMAIL, "password": DEMO_PASSWORD})

    print("\n--- Cookies after login ---")
    for c in s.cookies:
        print(f"{c.name} = {c.value}")

    # Simulate expiry by tampering one cookie
    if "session" in s.cookies:
        s.cookies.set("session", "EXPIRED")
    resp = s.get(LOGIN_URL)
    print("\nAfter tampering 'session' cookie – GET /login status:", resp.status_code)

    # Save cookies to disk
    with open(COOKIE_JAR, "wb") as f:
        pickle.dump(s.cookies, f)
    s.close()

    # Load cookies into a fresh session
    new_s = requests.Session()
    if os.path.exists(COOKIE_JAR):
        new_s.cookies.update(pickle.load(open(COOKIE_JAR, "rb")))

    resp2 = new_s.get(LOGIN_URL)
    print("\nLoaded cookies – GET /login status:", resp2.status_code)
    soup = BeautifulSoup(resp2.text, "html.parser")
    if resp2.ok and soup.select(PRODUCT_CONTAINER_SEL):
        print("✅ Still authenticated via saved cookies.")
    else:
        print("⚠️  Saved cookies no longer valid.")


# ------------------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    task1_basic_login_and_scrape()
    task2_csrf_login_and_scrape()
    task3_cookie_inspection_and_persistence()
