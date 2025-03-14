import requests
from bs4 import BeautifulSoup
import ssl
import socket



# Exercise 1
def fetch_response_info(url):
    try:
        response = requests.get(url)
        print(f"\nStatus Code: {response.status_code}")
        print("\nResponse Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
    except requests.RequestException as e:
        print(f"Error: {e}")



# Exercise 2
def extract_book_titles(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        book_titles = [book.get_text(strip=True) for book in soup.select("article.product_pod h3 a")]

        print("\nBook Titles on Homepage:")
        for title in book_titles:
            print("-", title)

    except requests.RequestException as e:
        print(f"Error: {e}")



# Exercise 3
def scrape_all_books(base_url):
    page = 1
    all_books = []

    while True:
        url = f"{base_url}/catalogue/page-{page}.html"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        books = [book.get_text(strip=True) for book in soup.select("article.product_pod h3 a")]
        all_books.extend(books)
        print(f"\nPage {page} Books:", books)

        page += 1

    print(f"\nTotal books scraped: {len(all_books)}")



# Exercise 4
def demonstrate_http_methods(url):
    try:
        get_response = requests.get(url)
        print(f"\nGET Request Status: {get_response.status_code}")

        head_response = requests.head(url)
        print(f"\nHEAD Request Headers:\n{head_response.headers}")

        try:
            post_response = requests.post(url, data={"sample": "test"})
            print(f"\nPOST Request Response: {post_response.status_code} (Expected failure)")
        except requests.RequestException as e:
            print(f"\nPOST Request Error: {e}")

    except requests.RequestException as e:
        print(f"Error: {e}")



# Exercise 5
def check_ssl_certificate(domain, verify=True):
    try:
        context = ssl.create_default_context() if verify else ssl._create_unverified_context()

        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cert = secure_sock.getpeercert()

                print(f"\nSSL Check for {domain} (Verification: {'Enabled' if verify else 'Disabled'})")
                print(f"Issuer: {cert.get('issuer', 'Unknown')}")
                print(f"Subject: {cert.get('subject', 'Unknown')}")
                print(f"Valid From: {cert.get('notBefore', 'Unknown')}")
                print(f"Valid Until: {cert.get('notAfter', 'Unknown')}")

    except ssl.SSLError:
        print(f"\nSSL verification failed for {domain} (Verification: {'Enabled' if verify else 'Disabled'})")
    except socket.gaierror:
        print(f"\nCould not connect to {domain}")



URL = "http://books.toscrape.com"
