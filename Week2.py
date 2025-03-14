import requests
from bs4 import BeautifulSoup
import ssl
import socket

"""Task 1"""
def task_1():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Headers:", response.headers, "\n")


"""Task 2"""
def task_2():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [book.get_text() for book in soup.find_all("h3")]
    print("Book Titles on Homepage:")
    for title in titles:
        print(title)
    print()


"""Task 3"""

def task_3():
    url = "http://books.toscrape.com/catalogue/page-{}.html"
    page = 1
    while True:
        response = requests.get(url.format(page))
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [book.get_text() for book in soup.find_all("h3")]
        print(f"Page {page} Titles:")
        for title in titles:
            print(title)
        page += 1
    print()


"""Task 4"""
def task_4():
    url = "http://httpbin.org"
    print("GET Response:", requests.get(url + "/get").text[:200])
    print("POST Response:", requests.post(url + "/post", data={"key": "value"}).text[:200])
    print("HEAD Response Headers:", requests.head(url).headers, "\n")


"""Task 5"""
def task_5():
    domain = "books.toscrape.com"
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print("SSL Certificate is Valid.")
                print("Certificate Info:", cert)
    except ssl.SSLError as e:
        print("SSL Certificate is Invalid:", e)

    print("\nDisabling SSL Verification:")
    try:
        requests.get("https://" + domain, verify=False)
        print("Success with SSL verification disabled.")
    except requests.exceptions.SSLError as e:
        print("Failed without SSL verification:", e)


if __name__ == "__main__":
    task_1()
    task_2()
    task_3()
    task_4()
    task_5()
