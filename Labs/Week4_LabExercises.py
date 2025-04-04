import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ------------- Task 1 -------------

def scrape_books_main_page():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    book_headers = soup.find_all("h3")
    books = []

    for h3 in book_headers:
        parent = h3.parent

        while parent and parent.name != "article":
            parent = parent.parent

        price_tag = parent.find("p", class_="price_color") if parent else None
        price = price_tag.text.strip() if price_tag else "N/A"
        title = h3.a["title"]

        books.append((title, price))
        print(f"{title} - {price}")

    return books


# ------------- Task 2 ---------
BASE_URL = "https://books.toscrape.com/"

def scrape_books_structure():
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    books_data = []
    product_cards = soup.find_all("article", class_="product_pod")

    for card in product_cards[:10]:
        h3_tag = card.find("h3")
        title = h3_tag.a['title'] if h3_tag and h3_tag.a else "No title"

        price_tag = card.find("p", attrs={"class": "price_color"})
        price = price_tag.text.strip() if price_tag else "No price"

        availability_tag = price_tag.find_next_sibling("p") if price_tag else None
        availability = availability_tag.text.strip() if availability_tag else "No availability"

        link_tag = h3_tag.a if h3_tag and h3_tag.a else None
        link = urljoin(BASE_URL, link_tag["href"]) if link_tag else "No link"

        books_data.append({
            "title": title,
            "price": price,
            "availability": availability,
            "url": link
        })

        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print(f"URL: {link}")
        print("-" * 50)

    return books_data

