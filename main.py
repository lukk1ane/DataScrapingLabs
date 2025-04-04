import requests
from bs4 import BeautifulSoup


def task_1():
    # URL of the main page
    url = "https://books.toscrape.com/"

    # Send an HTTP GET request
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all book titles and prices
    books = soup.find_all("h3")

    for book in books:
        title = book.a.attrs["title"]
        parent = book.parent  # This is the <article> tag
        price = parent.find("p", class_="price_color").text.replace("Â£", '')  # Find the price

        print(f"Title: {title}, Price: {price}")


task_1()

import requests
from bs4 import BeautifulSoup


def scrape_books_to_scrape():
    url = "https://books.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    book_list = []

    for book in books:
        title_tag = book.find("h3").find("a")
        title = title_tag["title"] if title_tag else "N/A"

        price_tag = book.find("p", class_="price_color")
        price = price_tag.text.strip().replace("Â£", '') if price_tag else "N/A"

        availability_tag = price_tag.find_next_sibling("p", class_="instock availability")
        availability = availability_tag.text.strip() if availability_tag else "N/A"

        book_url = title_tag["href"] if title_tag else "#"
        full_url = f"https://books.toscrape.com/catalogue/{book_url.lstrip('../')}"

        book_list.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "URL": full_url
        })

    return book_list


books = scrape_books_to_scrape()
for item in books[:5]:
    print(f" Title: {item['Title']}")
    print(f" Price: {item['Price']}")
    print(f" Availability: {item['Availability']}")
    print(f" URL: {item['URL']}")
    print("-" * 50)
