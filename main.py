import requests
import ssl
import socket
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# Task 1
def fetch_books_to_scrape():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print("Response headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    return response


# Task 2
def extract_book_titles():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [book.get_text(strip=True) for book in soup.find_all("h3")]
    print("Book Titles:")
    for title in titles:
        print(title)
    return titles


# helper function for Task 3
def extract_book_titles_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [book.get_text(strip=True) for book in soup.find_all("h3")]


# Task 3
def scrape_all_pages():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    page = 1
    all_titles = []
    while True:
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code != 200:
            break
        print(f"Scraping page {page}...")
        all_titles.extend(extract_book_titles_from_page(url))
        page += 1
    print(f"Total pages scraped: {page - 1}")
    print(f"Total books found: {len(all_titles)}")
    print("First 5 Book Titles:")
    for title in all_titles[:5]:
        print(title)
    return all_titles


# Task 4
def demonstrate_http_methods():
    url = "http://books.toscrape.com/"
    # GET Request
    get_response = requests.get(url)
    print(f"GET Request Status: {get_response.status_code}")

    # HEAD Request
    head_response = requests.head(url)
    print(f"HEAD Request Status: {head_response.status_code}")
    print("HEAD Response Headers:")
    for key, value in head_response.headers.items():
        print(f"{key}: {value}")

    # POST Request (Demonstration only, as Books to Scrape does not support POST)
    post_response = requests.post(url, data={"test": "data"})
    print(f"POST Request Status: {post_response.status_code}")

    return {"get": get_response, "head": head_response, "post": post_response}


# Task 5
def verify_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print("SSL Certificate Information:")
                # Only print a few key certificate details
                print(f"Subject: {dict(cert['subject'][0])}")
                print(f"Issuer: {dict(cert['issuer'][0])}")
                print(f"Valid from: {cert['notBefore']}")
                print(f"Valid until: {cert['notAfter']}")
                print("SSL Verification: SUCCESS")
    except Exception as e:
        print(f"SSL Verification: FAILED - {e}")


def demonstrate_ssl_verification():
    domain = "books.toscrape.com"
    print("Verifying SSL certificate for:", domain)
    verify_ssl_certificate(domain)

    print("\nDisabling SSL verification...")
    try:
        response = requests.get(f"https://{domain}", verify=False)
        print(f"Request successful with SSL verification disabled. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Request failed with SSL verification disabled: {e}")


if __name__ == "__main__":
    print("=== Task 1: Fetch Books to Scrape ===")
    fetch_books_to_scrape()

    print("\n=== Task 2: Extract Book Titles ===")
    extract_book_titles()

    print("\n=== Task 3: Scrape All Pages ===")
    scrape_all_pages()

    print("\n=== Task 4: Demonstrate HTTP Methods ===")
    demonstrate_http_methods()

    print("\n=== Task 5: Verify SSL Certificate ===")
    demonstrate_ssl_verification()