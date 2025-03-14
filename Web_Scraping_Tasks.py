import requests
from bs4 import BeautifulSoup
import ssl
import socket

# Task 1: Send a GET request and print status code & headers
def task_1():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    print("Task 1 - GET Request:")
    print("Status Code:", response.status_code)
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\n" + "="*50 + "\n")

# Task 2: Extract all book titles from the homepage
def task_2():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [book.get_text().strip() for book in soup.select("h3 a")]

    print("Task 2 - Book Titles on Homepage:")
    for title in titles:
        print(title)
    print("\n" + "="*50 + "\n")

# Task 3: Navigate through pages and extract data
def task_3():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    page = 1
    all_books = []

    while True:
        url = base_url.format(page)
        response = requests.get(url)

        if response.status_code != 200:
            break  # Stop if page doesn't exist

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("h3 a")

        for book in books:
            all_books.append(book.get_text().strip())

        page += 1

    print("Task 3 - Extracted Book Titles from All Pages:")
    for title in all_books:
        print(title)
    print("\n" + "="*50 + "\n")

# Task 4: Demonstrating different HTTP methods
def task_4():
    url = "http://books.toscrape.com/"

    # GET Request
    response_get = requests.get(url)
    print("Task 4 - GET Response Code:", response_get.status_code)

    # HEAD Request
    response_head = requests.head(url)
    print("HEAD Response Code:", response_head.status_code)
    print("HEAD Response Headers:", response_head.headers)

    # POST Request (Usually requires a form submission, so it might not work on this site)
    response_post = requests.post(url, data={"key": "value"})
    print("POST Response Code:", response_post.status_code)
    print("\n" + "="*50 + "\n")

# Task 5: SSL Certificate Verification
def task_5():
    ssl_url = "https://www.google.com"

    # Verify SSL certificate
    try:
        response = requests.get(ssl_url, verify=True)
        print("Task 5 - SSL Verification: SUCCESS")
    except requests.exceptions.SSLError:
        print("SSL Verification: FAILED")

    # Disable SSL Verification
    try:
        response = requests.get(ssl_url, verify=False)
        print("SSL Verification Disabled: Request Successful")
    except requests.exceptions.SSLError:
        print("SSL Verification Disabled: FAILED")

    # Retrieve SSL certificate information
    def get_ssl_info(hostname):
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return cert

    ssl_info = get_ssl_info("www.google.com")
    print("SSL Certificate Information:")
    for key, value in ssl_info.items():
        print(f"{key}: {value}")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    task_1()
    task_2()
    task_3()
    task_4()
    task_5()
