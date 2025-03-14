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

    def extract_book_titles(self):
        """Task 2: Extract all book titles from the homepage."""
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        book_titles = [book.get_text(strip=True) for book in soup.select("h3 a")]

        print("Book Titles on Homepage:")
        for title in book_titles:
            print(title)


if __name__ == '__main__':
    scraper = BookScraper()

    print("\n--- Task 1: GET Status & Headers ---")
    scraper.get_status_and_headers()

    print("\n--- Task 2: Extract Book Titles ---")
    scraper.extract_book_titles()

