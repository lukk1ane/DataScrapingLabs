import requests
from bs4 import BeautifulSoup
import ssl
import socket

BASE_URL = "https://books.toscrape.com"


# Task 1: GET request to Books to Scrape
def get_request():
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"\n[Task 1] GET Request to {BASE_URL}")
        print(f"Status Code: {response.status_code}\n")
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Task 2: Extract book titles from homepage
def extract_titles():
    try:
        response = requests.get(BASE_URL, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all("h3")

        print("\n[Task 2] Book Titles from Homepage:")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book.a.attrs['title']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Task 3: Scrape all book titles from paginated pages
def scrape_all_pages():
    url = BASE_URL + "/catalogue/page-1.html"
    page_num = 1

    print("\n[Task 3] Extracting Books from All Pages...\n")
    while url:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all("h3")

            print(f"Page {page_num} Titles:")
            for book in books:
                print(f"- {book.a.attrs['title']}")

            next_page = soup.find("li", class_="next")
            if next_page:
                url = BASE_URL + "/catalogue/" + next_page.a.attrs["href"]
                page_num += 1
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break


# Task 4: Demonstrate HTTP methods (GET, POST, HEAD)
def test_http_methods():
    print("\n[Task 4] Testing HTTP Methods\n")

    try:
        get_resp = requests.get(BASE_URL)
        print(f"GET Response Code: {get_resp.status_code}")

        head_resp = requests.head(BASE_URL)
        print(f"HEAD Response Code: {head_resp.status_code}")

        post_resp = requests.post(BASE_URL, data={"sample": "data"})
        print(f"POST Response Code: {post_resp.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Task 5: Check SSL certificate
def check_ssl():
    hostname = "books.toscrape.com"
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("\n[Task 5] SSL Certificate Information\n")
                print(f"Issuer: {cert.get('issuer', 'N/A')}")
                print(f"Valid From: {cert.get('notBefore', 'N/A')}")
                print(f"Valid Until: {cert.get('notAfter', 'N/A')}")
                print("SSL Certificate is Valid ✅")
    except ssl.SSLError as e:
        print("SSL Verification Failed ❌", e)
    except socket.error as e:
        print("Socket Error:", e)


# Run all tasks
if __name__ == "__main__":
    get_request()
    extract_titles()
    scrape_all_pages()
    test_http_methods()
    check_ssl()
