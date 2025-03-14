import socket
import ssl
import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://books.toscrape.com"
CATALOG_URL_TEMPLATE = f"{BASE_URL}/catalogue/page-{{page_num}}.html"
MAX_PAGES_TO_SCRAPE = 5


def fetch_page(url, method="get", data=None, verify_ssl=True):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        if method.lower() == "get":
            return requests.get(url, headers=headers, verify=verify_ssl)
        elif method.lower() == "post":
            return requests.post(url, data=data, headers=headers, verify=verify_ssl)
        elif method.lower() == "head":
            return requests.head(url, headers=headers, verify=verify_ssl)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    except Exception as e:
        print(f"Error fetching {url} with {method}: {e}")
        return None


def extract_book_titles(html_content):
    parser = BeautifulSoup(html_content, 'html.parser')
    book_elements = parser.select("h3 a")
    return [element.get_text(strip=True) for element in book_elements]


def inspect_main_page():
    print("===== TASK 1: BASIC REQUEST AND RESPONSE INSPECTION =====")
    response = fetch_page(BASE_URL)
    if response:
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    print("-" * 60)


def extract_main_page_books():
    print("===== TASK 2: EXTRACT BOOKS FROM MAIN PAGE =====")
    response = fetch_page(BASE_URL)
    if response and response.status_code == 200:
        book_list = extract_book_titles(response.content)
        print(f"Found {len(book_list)} books on main page:")
        for idx, title in enumerate(book_list, 1):
            print(f"  Book {idx}: {title}")
    print("-" * 60)


def scrape_multiple_pages():
    print("===== TASK 3: PAGINATED SCRAPING =====")
    collected_books = []

    for page_num in range(1, MAX_PAGES_TO_SCRAPE + 1):
        page_url = CATALOG_URL_TEMPLATE.format(page_num=page_num)
        print(f"Scraping page {page_num}...")

        response = fetch_page(page_url)
        if not response or response.status_code != 200:
            print(f"Failed to fetch page {page_num}, stopping pagination")
            break

        page_books = extract_book_titles(response.content)
        collected_books.extend(page_books)

        time.sleep(random.uniform(0.5, 1.0))

    print(f"Collected {len(collected_books)} books from {MAX_PAGES_TO_SCRAPE} pages")
    print("Sample of collected books:")
    for idx, title in enumerate(collected_books[:5], 1):
        print(f"  {idx}. {title}")
    print("-" * 60)


def test_http_methods():
    print("===== TASK 4: TESTING HTTP METHODS =====")

    get_response = fetch_page(BASE_URL, method="get")
    print(f"GET request status: {get_response.status_code if get_response else 'Failed'}")

    dummy_credentials = {"username": "bookuser", "password": "pass1234"}
    post_response = fetch_page(BASE_URL, method="post", data=dummy_credentials)
    print(f"POST request status: {post_response.status_code if post_response else 'Failed'}")

    head_response = fetch_page(BASE_URL, method="head")
    print(f"HEAD request status: {head_response.status_code if head_response else 'Failed'}")
    print("-" * 60)


def analyze_ssl_certificate():
    print("===== TASK 5: SSL CERTIFICATE VERIFICATION =====")

    try:
        verify_response = fetch_page(BASE_URL, verify_ssl=True)
        print("SSL Verification: SUCCESSFUL")
    except requests.exceptions.SSLError:
        print("SSL Verification: FAILED")

    try:
        no_verify_response = fetch_page(BASE_URL, verify_ssl=False)
        print(
            f"Request with SSL verification disabled: Status {no_verify_response.status_code if no_verify_response else 'Failed'}")
    except Exception as e:
        print(f"Error with SSL verification disabled: {e}")

    try:
        hostname = "books.toscrape.com"
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_socket:
                certificate = secure_socket.getpeercert()

                print("\nCertificate Information:")
                important_fields = ['subject', 'issuer', 'version', 'notBefore', 'notAfter']
                for field in important_fields:
                    if field in certificate:
                        print(f"  {field}: {certificate[field]}")
    except Exception as e:
        print(f"Error retrieving SSL certificate: {e}")
    print("-" * 60)


if __name__ == "__main__":
    inspect_main_page()
    extract_main_page_books()
    scrape_multiple_pages()
    test_http_methods()
    analyze_ssl_certificate()