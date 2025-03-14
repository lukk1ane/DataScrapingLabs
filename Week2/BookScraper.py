import requests
from bs4 import BeautifulSoup
import ssl
import socket


class BookScraper:
    def __init__(self, base_url="https://books.toscrape.com/"):
        self.base_url = base_url

    def get_status_and_headers(self):
        """Task 1: Send a GET request and print the status code and response headers."""
        response = requests.get(self.base_url)
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)


if __name__ == '__main__':
    # Instantiate the class and call methods
    scraper = BookScraper()

    print("\n--- Task 1: GET Status & Headers ---")
    scraper.get_status_and_headers()
