import requests
from bs4 import BeautifulSoup

def fetch_books_to_scrape():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

def extract_book_titles():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    titles = [book.get_text(strip=True) for book in soup.select("h3 a")]
    print("Book Titles:")
    for title in titles:
        print(title)

if __name__ == "__main__":
    fetch_books_to_scrape()
    extract_book_titles()
