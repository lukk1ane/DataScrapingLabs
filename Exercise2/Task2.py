import requests
from bs4 import BeautifulSoup


def extract_book_titles():
    url = "http://books.toscrape.com/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('article', class_='product_pod')

        print(f"Found {len(books)} books on the homepage:\n")

        for i, book in enumerate(books, 1):
            title = book.h3.a['title']
            print(f"{i}. {title}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


if __name__ == "__main__":
    extract_book_titles()