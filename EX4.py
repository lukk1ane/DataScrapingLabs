import requests
from bs4 import BeautifulSoup

def scrape_books_main_page():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("h3")
    print("BooksToScrape.com - Book Titles and Prices:")
    for book in books:
        title = book.find("a")["title"]
        price = book.parent.find("p", class_="price_color").text
        print(f"Title: {title}, Price: {price}")

def scrape_swoop_ge():
    url = "https://www.swoop.ge/category/eleqtro-teqnika/televizorebi"  # Category URL with static listings
    headers = {"User-Agent": "Mozilla/5.0"}  # Spoof user-agent to avoid blocks
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    print("\nSwoop.ge - Product Titles and Prices (if available):")
    products = soup.find_all("div", class_="catalog-product-card")  # Updated class based on real category page
    extracted_data = []
    for product in products[:2]:  # Grab at least 2 for the task
        title_tag = product.find("a", class_="title")
        price_tag = product.find("div", class_="price-box")
        title = title_tag.text.strip() if title_tag else "No title"
        price = price_tag.text.strip() if price_tag else "No price"
        extracted_data.append({"title": title, "price": price})
        print(f"Title: {title}, Price: {price}")

if __name__ == "__main__":
    scrape_books_main_page()
    scrape_swoop_ge()
