import requests
from bs4 import BeautifulSoup
import ssl
import socket


# task 01
print("Task 01: \n")
# Make a GET request to the URL
url = "http://books.toscrape.com/"
response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)

# task 02
print("\nTask 02: \n")
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

book_titles = soup.find_all('h3')

for title in book_titles:
    print(title.text)

# Task 03
print("\nTask 03: \n")
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# Loop through the pages
for page_number in range(1, 3):  # Limiting to 2 pages for demonstration
    url = base_url.format(page_number)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        book_titles = soup.find_all('h3')
        
        print(f"Page {page_number} Book Titles:")
        for title in book_titles:
            print(title.text)
    else:
        print(f"Failed to retrieve page {page_number}")


# Task 04
print("\nTask 04: \n")

# GET request
try:
    get_response = requests.get("https://httpbin.org/get")
    print("GET Response Status Code:", get_response.status_code)
    if get_response.status_code == 200:
        print("GET Response Content:", get_response.json())
    else:
        print(f"GET request failed with status code: {get_response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"GET request failed: {str(e)}")

# POST request
try:
    post_data = {'key1': 'value1', 'key2': 'value2'}
    post_response = requests.post("https://httpbin.org/post", data=post_data)
    print("POST Response Status Code:", post_response.status_code)
    if post_response.status_code == 200:
        print("POST Response Content:", post_response.json())
    else:
        print(f"POST request failed with status code: {post_response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"POST request failed: {str(e)}")

# HEAD request
try:
    head_response = requests.head("https://httpbin.org/get")
    print("HEAD Response Status Code:", head_response.status_code)
    print("HEAD Response Headers:", dict(head_response.headers))
except requests.exceptions.RequestException as e:
    print(f"HEAD request failed: {str(e)}")


# Task 05
print("\nTask 05: \n")
try:
    # Test SSL verification
    ssl_response = requests.get("https://httpbin.org/", verify=True)
    print("SSL Verification Status Code:", ssl_response.status_code)
    print("SSL Verification: Success")
except requests.exceptions.SSLError as e:
    print("SSL Verification: Failed", str(e))

try:
    # Disable SSL verification
    ssl_response = requests.get("https://httpbin.org/", verify=False)
    print("SSL Verification Disabled Status Code:", ssl_response.status_code)
    print("SSL Verification Disabled: Success")
except requests.exceptions.SSLError:
    print("SSL Verification Disabled: Failed")

# get ssl info
def get_ssl_cert_info(hostname, port=443):
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Create socket and wrap it with SSL
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("Certificate Details:")
                print(f"Subject: {dict(x[0] for x in cert['subject'])}")
                print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
                print(f"Version: {cert['version']}")
                print(f"Serial Number: {cert['serialNumber']}")
                print(f"Valid From: {cert['notBefore']}")
                print(f"Valid Until: {cert['notAfter']}")
                return cert
    except Exception as e:
        print(f"Error getting certificate info: {str(e)}")
        return None

if __name__ == "__main__":
    hostname = "httpbin.org"
    cert_info = get_ssl_cert_info(hostname)
