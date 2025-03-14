import requests
from bs4 import BeautifulSoup
import ssl
import socket

def get_status_and_headers(url):
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

def extract_book_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [book.get_text().strip() for book in soup.select("h3 a")]
    print("Book Titles:")
    for title in titles:
        print(title)

def scrape_all_pages(base_url):
    page = 1
    books = []
    while True:
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code != 200:
            break  # Stop if we reach a non-existing page
        soup = BeautifulSoup(response.text, "html.parser")
        book_elements = soup.select(".product_pod")
        for book in book_elements:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").get_text()
            books.append((title, price))
        page += 1
    print("Extracted Books:")
    for title, price in books:
        print(f"{title} - {price}")

def demonstrate_http_methods():
    url = "http://httpbin.org"
    print("GET Request:")
    print(requests.get(url + "/get").json())
    print("POST Request:")
    print(requests.post(url + "/post", data={"key": "value"}).json())
    print("HEAD Request Headers:")
    response_head = requests.head(url)
    for key, value in response_head.headers.items():
        print(f"{key}: {value}")

def check_ssl_certificate(host):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.create_connection((host, 443)), server_hostname=host) as s:
            cert = s.getpeercert()
        print("SSL Certificate Verified Successfully!")
        print("Issuer:", dict(cert["issuer"]))
        print("Valid From:", cert["notBefore"])
        print("Valid Until:", cert["notAfter"])
    except Exception as e:
        print(f"SSL Verification Failed: {e}")

def demonstrate_ssl_verification():
    check_ssl_certificate("books.toscrape.com")
    print("\nDemonstrating SSL Verification Disabled:")
    try:
        response = requests.get("https://expired.badssl.com/", verify=False)
        print("Response (SSL Disabled):", response.status_code)
    except requests.exceptions.SSLError as e:
        print("SSL Verification Failed:", e)

if __name__ == "__main__":
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    homepage_url = "http://books.toscrape.com/"
    
    print("\nTask 1: Status and Headers")
    get_status_and_headers(homepage_url)
    
    print("\nTask 2: Extract Book Titles")
    extract_book_titles(homepage_url)
    
    print("\nTask 3: Scrape All Pages")
    scrape_all_pages(base_url)
    
    print("\nTask 4: Demonstrate HTTP Methods")
    demonstrate_http_methods()
    
    print("\nTask 5: SSL Verification")
    demonstrate_ssl_verification()
