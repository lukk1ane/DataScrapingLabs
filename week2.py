import requests
from bs4 import BeautifulSoup
import ssl
import socket

BASE_URL = "https://books.toscrape.com"


# Task 1: Send a GET request and print status and headers
def task_1():
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")


# Task 2: Extract all book titles from homepage
def task_2():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all("h3")
    print("\nBook Titles on Homepage:")
    for book in books:
        print(book.a.attrs['title'])


# Task 3: Navigate through pages and extract book titles
def task_3():
    url = BASE_URL + "/catalogue/page-1.html"
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all("h3")
        print("\nBook Titles on Current Page:")
        for book in books:
            print(book.a.attrs['title'])
        next_page = soup.find("li", class_="next")
        if next_page:
            url = BASE_URL + "/catalogue/" + next_page.a.attrs["href"]
        else:
            break


# Task 4: Demonstrate different HTTP methods
def task_4():
    print("\nGET request:")
    get_response = requests.get(BASE_URL)
    print(f"GET Status Code: {get_response.status_code}")

    print("\nHEAD request:")
    head_response = requests.head(BASE_URL)
    print(f"HEAD Status Code: {head_response.status_code}")

    print("\nPOST request (Not supported but for demonstration):")
    post_response = requests.post(BASE_URL, data={"key": "value"})
    print(f"POST Status Code: {post_response.status_code}")


# Task 5: SSL Verification
def task_5():
    hostname = "books.toscrape.com"
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("\nSSL Certificate is valid!")
                print(f"Issuer: {cert['issuer']}")
                print(f"Valid from: {cert['notBefore']}")
                print(f"Valid until: {cert['notAfter']}")
    except ssl.SSLError as e:
        print("\nSSL Verification Failed:", e)


# Run all tasks
if __name__ == "__main__":
    task_1()
    task_2()
    task_3()
    task_4()
    task_5()
