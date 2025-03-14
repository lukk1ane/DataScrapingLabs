import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import time
import ssl
import socket

# URL of the Books to Scrape website
url = "http://books.toscrape.com/"

# Task 1: Send a GET request and print the status code and response headers
response = requests.get(url)
print("Status Code:", response.status_code)
print("\nResponse Headers:")
for key, value in response.headers.items():
    print(f"{key}: {value}")

# Task 2: Extract and print all book titles from the homepage
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "lxml")
    book_titles = soup.find_all("h3")
    print("\nBook Titles:")
    for title in book_titles:
        print(title.a["title"])
else:
    print(f"\nFailed to retrieve the webpage. Status code: {response.status_code}")

# Task 3: Navigate through pages of the book catalog and extract data from each page
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
page_number = 1

while True:
    page_url = base_url.format(page_number)
    response = requests.get(page_url)
    
    if response.status_code != 200:
        print(f"\nReached the end of the catalog at page {page_number - 1}.")
        break
    
    soup = BeautifulSoup(response.content, "lxml")
    book_titles = soup.find_all("h3")
    
    print(f"\nBook Titles from Page {page_number}:")
    for title in book_titles:
        print(title.a["title"])
    
    page_number += 1

# Task 4: Implement HTTP Methods (GET, POST, HEAD)
def test_http_methods(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    # GET request
    start_time = time.time()
    get_response = requests.get(url, headers=headers)
    get_time = time.time() - start_time

    print(f"\nGET Request to {url}")
    print(f"Status Code: {get_response.status_code}")
    print(f"Response Time: {get_time:.4f} seconds")
    print(f"Content Length: {len(get_response.content)} bytes")
    print(f"Headers: {dict(get_response.headers)}")
    print()

    # HEAD request
    start_time = time.time()
    head_response = requests.head(url, headers=headers)
    head_time = time.time() - start_time

    print(f"HEAD Request to {url}")
    print(f"Status Code: {head_response.status_code}")
    print(f"Response Time: {head_time:.4f} seconds")
    print(f"Headers: {dict(head_response.headers)}")
    print()

    # POST request
    try:
        start_time = time.time()
        post_response = requests.post(url, headers=headers, data={})
        post_time = time.time() - start_time

        print(f"POST Request to {url}")
        print(f"Status Code: {post_response.status_code}")
        print(f"Response Time: {post_time:.4f} seconds")
        print(f"Content Length: {len(post_response.content)} bytes")
        print(f"Headers: {dict(post_response.headers)}")
    except requests.exceptions.RequestException as e:
        print(f"Error with POST request: {e}")

    # Compare request times
    print("\nMethod Comparison:")
    print(f"GET time: {get_time:.4f} seconds")
    print(f"HEAD time: {head_time:.4f} seconds")
    print(f"HEAD was {get_time / head_time:.2f}x faster than GET")

# Test HTTP methods on the Books to Scrape homepage
print("\nTask 4: Testing HTTP Methods")
test_http_methods(url)

# Task 5: Verify SSL certificate and retrieve basic SSL information
def verify_ssl_certificate(domain):
    try:
        # Create a default SSL context
        context = ssl.create_default_context()

        # Wrap the socket with SSL
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                print(f"\nSSL Certificate for {domain} is valid.")
                cert = ssock.getpeercert()
                print("\nBasic SSL Certificate Information:")
                print(f"Issuer: {cert['issuer']}")
                print(f"Valid From: {cert['notBefore']}")
                print(f"Valid Until: {cert['notAfter']}")
                print(f"Subject: {cert['subject']}")
                print(f"Version: {cert['version']}")
    except ssl.SSLError as e:
        print(f"\nSSL Certificate for {domain} is invalid: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def test_ssl_verification(domain):
    # Test with SSL verification enabled
    print("\nTesting SSL verification with verification enabled:")
    try:
        response = requests.get(f"https://{domain}", verify=True)
        print(f"SSL verification succeeded. Status Code: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"SSL verification failed: {e}")

    # Test with SSL verification disabled
    print("\nTesting SSL verification with verification disabled:")
    try:
        response = requests.get(f"https://{domain}", verify=False)
        print(f"SSL verification bypassed. Status Code: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"SSL verification failed: {e}")

# Test SSL verification and retrieve certificate information
print("\nTask 5: Verifying SSL Certificate")
domain = "http://books.toscrape.com/" 
verify_ssl_certificate(domain)
test_ssl_verification(domain)