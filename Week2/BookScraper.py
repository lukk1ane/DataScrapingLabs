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

    def extract_all_books(self):
        """Task 3: Navigate through pages of the book catalog and extract book titles."""
        base_catalog_url = self.base_url + "catalogue/page-{}.html"
        page = 1
        all_books = []

        while True:
            url = base_catalog_url.format(page)
            response = requests.get(url)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            books = [book.get_text(strip=True) for book in soup.select("h3 a")]
            all_books.extend(books)

            print(f"Scraped Page {page} with {len(books)} books")
            page += 1

        print("\nTotal Books Scraped:", len(all_books))

    def demonstrate_http_methods(self):
        """Task 4: Demonstrate different HTTP methods."""
        # GET request
        response_get = requests.get(self.base_url)
        print("GET Response:", response_get.status_code)

        # HEAD request (only headers)
        response_head = requests.head(self.base_url)
        print("HEAD Response Headers:", response_head.headers)

        # POST request (just a simulation)
        response_post = requests.post(self.base_url, data={"key": "value"})
        print("POST Response:", response_post.status_code)


if __name__ == '__main__':
    scraper = BookScraper()

    print("\n--- Task 1: GET Status & Headers ---")
    scraper.get_status_and_headers()

    print("\n--- Task 2: Extract Book Titles ---")
    scraper.extract_book_titles()

    print("\n--- Task 3: Extract All Books ---")
    scraper.extract_all_books()

    print("\n--- Task 4: Demonstrate HTTP Methods ---")
    scraper.demonstrate_http_methods()
