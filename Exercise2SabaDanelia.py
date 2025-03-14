import json
import socket
import ssl

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
# task 1
page = 1
urlI = f"https://books.toscrape.com/catalogue/page-{page}.html"
urlMain = "https://books.toscrape.com/index.html"
response = requests.get(urlMain)
print(response.status_code)
print(response.headers)
print("_________________________________________________________")
# task 2
response = requests.get(urlMain)
soup = BeautifulSoup(response.content, 'html.parser')
titles = [book.get_text(strip = True) for book in soup.select("h3 a")]

print("books:")
for i in range(len(titles)):
    print(f"book{i}: {titles[i]}")
print("_________________________________________________________")
# task 3
everyTitle = []
maxPage = 5
while True:
        # url = urlI
        if(page > maxPage):
            break
        response = requests.get(urlI)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = [book.get_text(strip=True) for book in soup.select("h3 a")]
        everyTitle += titles
        page += 1
print(everyTitle)
print("_________________________________________________________")
# task 4
url1 = "https://books.toscrape.com"
get = requests.get(url1)
print(get.status_code)
url2 = "https://books.toscrape.com"
data = {"username": "saba", "password": "saba1234"}
post = requests.post(url2, data)
print(post.status_code)
head = requests.head(urlMain)
print(head.status_code)
print("_________________________________________________________")
# task 5
# Verify if a website has a valid SSL certificate.
# Display the success or failure of SSL verification.
try:
    response = requests.get(urlMain,verify=True)
    print("SSL SUCCESS")
except requests.exceptions.SSLError:
        print("SSL FAILURE")
#Show what happens when SSL verification is disabled.
disabledSSL = requests.get(urlMain, verify=False)
print(f"SSL Disabled status: {disabledSSL.status_code}")
#Retrieve and display basic SSL certificate information.
context = ssl.create_default_context()
conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="books.toscrape.com")
conn.connect(("books.toscrape.com", 443))
cert = conn.getpeercert()

print("SSL info:")
for key, value in cert.items():
    print(f"{key}: {value}")