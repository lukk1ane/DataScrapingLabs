import requests
from bs4 import BeautifulSoup
import socket
from OpenSSL import SSL
from pprint import pprint
# EXERCISE 1 --------------------------------
url = 'http://books.toscrape.com/'

def get_request(url):
    res = requests.get(url)
    return res
res = get_request(url)
print(res.status_code)
for key, value in res.headers.items():
    print(f"{key}: {value}")
# EXERCISE 2 --------------------------------

def get_book_titles(url):
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('h3')
    titles = [book.a['title'] for book in books]
    
    return titles



book_titles = get_book_titles(url)
    
for idx, title in enumerate(book_titles, start=1):
    print(f"{idx}. {title}")


# EXERCISE 3 -------------------------------
def get_book_titles(url):
    titles = []
    
    while url:
        response = requests.get(url)
        
        if response.status_code != 200:
            print("Failed to retrieve page")
            return titles
        
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('h3')
        titles.extend([book.a['title'] for book in books])
        
       
        next_button = soup.find('li', class_='next')
        if next_button:
            next_url = next_button.find('a')['href']
            print(next_url)
            if "catalogue" not in url:
                url = f"http://books.toscrape.com/{next_url}"
            else:
                url = f"http://books.toscrape.com/{next_url}"
        else:
            url = None  
    
    return titles
 
book_titles = get_book_titles(url)
    
for idx, title in enumerate(book_titles, start=1):
    print(f"{idx}. {title}")



# EXERCISE 4

# GET 
def get_request():
    response = requests.get(url)
    print("GET Request Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()[:10]}") 

# POST 
def post_request():
    data = {
        'title': 'Book1',
        'body': 'book1',
    }
    response = requests.post(url, json=data)
    print("\nPOST Request Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

# HEAD
def head_request():
    response = requests.head(url)
    print("\nHEAD Request Response:")
    print(f"Status Code: {response.status_code}")
    print("Headers: ")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

get_request()    
post_request()   
head_request()   

# Exercise 5 ----------------------------

def verify_ssl_certificate(url):
    try:
        response = requests.get(url, verify=True)
        print("success!")
        print("{response.status_code}")
    except requests.exceptions.SSLError as e:
        print("Failed")

def verify_ssl_disabled(url):
    try:
        response = requests.get(url, verify=False)
        print("SSL Verification Disabled for !")
        print("HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Request Failed for {url}. Error: {e}")

def get_ssl_certificate_info(url):
    hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
    context = SSL.Context(SSL.TLSv1_2_METHOD)
    connection = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    connection.set_tlsext_host_name(hostname.encode())
    connection.connect((hostname, 443))
    cert = connection.get_peer_certificate()
    print(cert.get_subject().get_components()) 
    print(f"Certificate Issuer: {cert.get_issuer()}")
    print(f"Certificate Serial Number: {cert.get_serial_number()}")
    print(f"Certificate Version: {cert.get_version()}")
    connection.close()

get_ssl_certificate_info(url)
verify_ssl_certificate(url)
verify_ssl_disabled(url)