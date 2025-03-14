import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"

def scrape_books():
    a = 1
    page_url = BASE_URL

    while page_url:
        print(f'Page : {a}')
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        titles = [book.get_text(strip=True) for book in soup.select("h3 a")]

        print(f"\nScraping: {page_url}")
        print("Book Titles:")
        for title in titles:
            print(f"- {title}")

        next_page = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_page["href"]) if next_page else None
        a += 1

if __name__ == "__main__":
    scrape_books()
