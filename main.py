
from bs4 import BeautifulSoup
import requests
import ssl
import socket

url = "http://books.toscrape.com/"

def task_1():
    response = requests.get(url)
    print(f"status code: {response.status_code}")
    for key, value in response.headers.items():
        print(f'{key} : {value}')

task_1()


def task_2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all('h3')

    for book in books:
        title = book.a["title"]
        print(title)
        print('---')



task_2(url)


def task_3():
    page = 1
    base_url = f"https://books.toscrape.com/catalogue/page-{1}.html"
    while True:
        response = requests.get(base_url)
        if response.status_code != 200:
            break
        print(f"from page:{page}")
        print("---")
        task_2(base_url)
        page += 1


task_3()

def task_4():
    url = "http://httpbin.org"
    response_get = requests.get(url)
    print("GET Response Status Code:", response_get.status_code)

    data = {"name": "John Doe", "age": 30}
    response_post = requests.post(url + "/post", json=data)
    print("POST Response Status Code:", response_post.status_code)
    print("POST Response Data:", response_post.json())

    response_head = requests.head(url)
    print("\nHEAD Response Headers:")
    for key, value in response_head.headers.items():
        print(f"{key}: {value}")


task_4()


def task_5():
    url = "https://books.toscrape.com/"

    try:
        response = requests.get(url, verify=True)
        print("SSL Verification:  Success")
    except requests.exceptions.SSLError:
        print("SSL Verification:  Failed")

    response_no_ssl = requests.get(url, verify=True)
    print("\nSSL Verification Disabled - Response Status Code:", response_no_ssl.status_code)

    hostname = "books.toscrape.com"
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            print("\nSSL Certificate Information:")
            print(f"Issuer: {cert['issuer']}")
            print(f"Subject: {cert['subject']}")
            print(f"Valid From: {cert['notBefore']}")
            print(f"Valid Until: {cert['notAfter']}")
task_5()