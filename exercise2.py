import requests
from bs4 import BeautifulSoup
import ssl
import socket
from urllib.parse import urljoin

def task_1():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers)

def task_2():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [book.get_text().strip() for book in soup.find_all('h3')]
    print("Book Titles:", titles)

def task_3():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    page = 1
    while True:
        url = base_url.format(page)
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [book.get_text().strip() for book in soup.find_all('h3')]
        print(f"Page {page} Titles:", titles)
        page += 1

def task_4():
    url = "http://books.toscrape.com/"
    response_get = requests.get(url)
    response_head = requests.head(url)
    response_post = requests.post(url, data={"key": "value"})
    
    print("GET Response Code:", response_get.status_code)
    print("HEAD Response Code:", response_head.status_code)
    print("POST Response Code:", response_post.status_code)

def task_5():
    hostname = "books.toscrape.com"
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("SSL Certificate is valid")
                print("SSL Certificate Info:", cert)
    except ssl.SSLError as e:
        print("SSL Verification Failed:", e)
    
    # Disabling SSL Verification
    try:
        response = requests.get("https://books.toscrape.com", verify=False)
        print("Response with SSL verification disabled:", response.status_code)
    except requests.exceptions.SSLError as e:
        print("Error with SSL verification disabled:", e)

if __name__ == "__main__":
    print("Executing Task 1:")
    task_1()
    print("\nExecuting Task 2:")
    task_2()
    print("\nExecuting Task 3:")
    task_3()
    print("\nExecuting Task 4:")
    task_4()
    print("\nExecuting Task 5:")
    task_5()
