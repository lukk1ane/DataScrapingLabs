import requests
from bs4 import BeautifulSoup
import ssl
from requests.exceptions import SSLError



def task1():
    response = requests.get(url)
    print("Status Code:", response.status_code)

    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

def task2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    path_to_book_titles = "body div div div div section div ol li article h3 a"
    book_titles = [book.get_text(strip=True) for book in soup.select(path_to_book_titles)]

    for idx, title in enumerate(book_titles, 1):
        print(f"{idx}. {title}")

    return book_titles

def task3():
    # Iterating over all 50 pages
    all_books = {}
    for i in range(1, 51):
        url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        all_books[i] = task2(url)

    return all_books

def task4():
    BASE_URL = "https://httpbin.org"  # Using public url for testing purposes

    def get_request():
        response = requests.get(f"{BASE_URL}/get", params={"example": "test"})
        print("\n GET Request:")
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    def post_request():
        payload = {"username": "test_user", "password": "secure123"}
        response = requests.post(f"{BASE_URL}/post", json=payload)
        print("\n POST Request:")
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    def head_request():
        response = requests.head(f"{BASE_URL}/get")
        print("\n HEAD Request:")
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)

    get_request()
    post_request()
    head_request()

def task5():
    def verify_ssl_certificate(url):
        try:
            response = requests.get(url, verify=True)  # SSL verification enabled (default)
            print(f"\nSSL Verification Successful: {url} is secure!")
            print("Status Code:", response.status_code)
        except SSLError as e:
            print(f"\nSSL Verification Failed: {url} is not secure!")
            print("Error:", e)

    def disable_ssl_verification(url):
        try:
            response = requests.get(url, verify=False)  # Disabling SSL verification
            print(f"\nSSL Verification Disabled: {url} - Response Status Code:", response.status_code)
            print("Warning: SSL certificate is not verified!")
        except requests.exceptions.RequestException as e:
            print(f"Request Failed: {e}")

    def get_ssl_certificate_info(url):
        hostname = url.replace("https://", "").replace("http://", "").split('/')[0]
        port = 443  # Default SSL port

        try:
            cert = ssl.get_server_certificate((hostname, port))
            print("\nSSL Certificate Info:")
            print(cert)
        except Exception as e:
            print(f"Error retrieving SSL certificate info: {e}")

    url = "https://www.google.com"  # Using some url

    verify_ssl_certificate(url)
    disable_ssl_verification(url)
    get_ssl_certificate_info(url)



if __name__ == '__main__':
    url = "http://books.toscrape.com/"

    # task1()
    # task2(url)
    # task3()
    # task4()
    task5()
