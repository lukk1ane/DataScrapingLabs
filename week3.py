import requests
from bs4 import BeautifulSoup
def fetch_books_page():
    url = "http://books.toscrape.com/"
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    fetch_books_page()

# task 2
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

titles = [book.get_text().strip() for book in soup.find_all("h3")]

print("Book Titles from Homepage:")
for title in titles:
    print(title)

# task 3

# base_url = "http://books.toscrape.com/catalogue/page-{}.html"
# page = 1
# all_titles = []
#
# while True:
#     response = requests.get(base_url.format(page))
#     if response.status_code != 200:
#         break  # Stop when there are no more pages
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#     titles = [book.get_text().strip() for book in soup.find_all("h3")]
#     all_titles.extend(titles)
#
#     print(f"Scraped page {page}")
#     page += 1
#
# print("\nAll Book Titles:")
# for title in all_titles:
#     print(title)

# task 4

import requests

url = "https://httpbin.org"

#GET
get_response = requests.get(url + "/get")
print("GET Response:", get_response.json())

#POST
post_response = requests.post(url + "/post", data={"key": "value"})
print("POST Response:", post_response.json())

#HEAD
head_response = requests.head(url)
print("HEAD Response Headers:", head_response.headers)


# task 5
import requests

website = "https://google.com/"

try:
    response = requests.get(website, verify=True)
    print(f"{website} has a valid SSL certificate.")
except requests.exceptions.SSLError:
    print(f"{website} does NOT have a valid SSL certificate.")


response_no_ssl = requests.get(website)
print("\nResponse with SSL Verification Disabled:")
print(response_no_ssl.status_code)
