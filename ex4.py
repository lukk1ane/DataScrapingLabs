import requests
from bs4 import BeautifulSoup


# task1

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


for h3_tag in soup.find_all("h3"):
    article_tag = h3_tag.find_parent("article", class_="product_pod")
    if article_tag:
        price_tag = article_tag.find("p", class_="price_color")
        if price_tag:
            book_title = h3_tag.a["title"]
            book_price = price_tag.text.strip()
            # print(f"title: {book_title}, price: {book_price}")

