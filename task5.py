import ssl
import socket
import requests

url = "https://books.toscrape.com/"

try:
    response = requests.get(url, verify=True)
    print("SSL Verification: SUCCESS")
except requests.exceptions.SSLError:
    print("SSL Verification: FAILED")

try:
    response = requests.get(url, verify=False)
    print("SSL Verification Disabled: Request Successful")
except requests.exceptions.SSLError:
    print("SSL Verification Disabled: Request Failed")

hostname = "books.toscrape.com"
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert = ssock.getpeercert()
        print("SSL Certificate Information:")
        print(f"Subject: {cert['subject']}")
        print(f"Issuer: {cert['issuer']}")
        print(f"Valid From: {cert['notBefore']}")
        print(f"Valid Until: {cert['notAfter']}")