import requests
from bs4 import BeautifulSoup
import ssl
import socket

# Task 1: Send a GET request and print status code and response headers
# --------------------------------------------
url = "http://books.toscrape.com/"
response = requests.get(url)
print("Task 1: Status Code:", response.status_code)
print("Response Headers:", response.headers)

# Task 2: Extract all book titles from the homepage
# --------------------------------------------
soup = BeautifulSoup(response.text, 'html.parser')
titles = [book.get_text(strip=True) for book in soup.select("h3 a")]
print("\nTask 2: Book Titles on Homepage:")
print(titles)

# Task 3: Navigate through pages and extract book data
# --------------------------------------------
print("\nTask 3: Extracting book data from multiple pages")
page = 1
while True:
    page_url = f"{url}catalogue/page-{page}.html"
    page_response = requests.get(page_url)
    if page_response.status_code != 200:
        break
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    books = [book.get_text(strip=True) for book in page_soup.select("h3 a")]
    print(f"Page {page} Books:", books)
    page += 1

# Task 4: Demonstrate different HTTP methods
# --------------------------------------------
print("\nTask 4: HTTP Methods Demonstration")
print("GET Request Status:", requests.get(url).status_code)
print("HEAD Request Headers:", requests.head(url).headers)
try:
    post_response = requests.post(url, data={'test': 'data'})
    print("POST Request Status:", post_response.status_code)
except requests.exceptions.RequestException as e:
    print("POST Request Failed:", e)

# Task 5: SSL Certificate Verification
# --------------------------------------------


def check_ssl_cert(hostname):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert()
            print("\nTask 5: SSL Certificate Information:")
            print("SSL Valid: Success")
            print(cert)
    except Exception as e:
        print("\nTask 5: SSL Verification Failed:", e)

# Checking SSL for a website


ssl_url = "books.toscrape.com"
check_ssl_cert(ssl_url)

# Demonstrate what happens when SSL verification is disabled
# --------------------------------------------
try:
    response = requests.get("https://www.google.com", verify=False)
    print("\nSSL Verification Disabled: Request Succeeded")
except requests.exceptions.SSLError as e:
    print("\nSSL Verification Disabled: Request Failed", e)
