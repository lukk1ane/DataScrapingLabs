import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree


def fetch_books_from_url(books_url):
    response = requests.get(books_url)

    if response.status_code != 200:
        print("Error: Unable to access books page.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    book_list = []

    for book in soup.find_all('h3'):
        title = book.a.get('title')
        article_tag = book.find_parent('article')
        price_tag = article_tag.find('p', class_='price_color') if article_tag else None
        price = price_tag.text.strip() if price_tag else 'N/A'

        book_list.append({'Title': title, 'Price': price})

    with open('books.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['Title', 'Price'])
        writer.writeheader()
        writer.writerows(book_list)

    print(f"{len(book_list)} books saved to books.csv")


def fetch_products_from_url(product_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(product_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to access {product_url} (Status Code: {response.status_code})")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    html_tree = etree.HTML(response.content)
    product_data = []

    container = soup.find('div', class_=lambda c: c and any(x in c for x in ['products', 'list', 'items']))
    if not container:
        print("Primary product container not found. Trying fallback...")
        container = soup.find(['section', 'ul', 'div'], class_=True)

    if not container:
        print("No product container located.")
        return

    for element in container.find_all(['div', 'li'], class_=lambda c: c and any(x in c for x in ['item', 'product'])):
        title_tag = element.find(['h2', 'h3', 'a'], class_=lambda c: c and any(x in c for x in ['title', 'name']))
        title = title_tag.text.strip() if title_tag else 'N/A'

        price_tag = element.find(class_=lambda c: c and any(x in c for x in ['price', 'cost']))
        price = price_tag.text.strip() if price_tag else 'N/A'

        description = 'N/A'
        if title_tag:
            desc_tag = title_tag.find_next_sibling('p')
            description = desc_tag.text.strip() if desc_tag else 'N/A'

        links = html_tree.xpath(".//a[contains(@href, 'product') or contains(@href, 'item')]/@href")
        link = links[0] if links else 'N/A'

        product_data.append({
            'Title': title,
            'Price': price,
            'Description': description,
            'URL': link
        })

    if not product_data:
        print("No products were extracted. Check structure or selectors.")
        return

    with open('products.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Description', 'URL'])
        writer.writeheader()
        writer.writerows(product_data)

    print(f"{len(product_data)} products saved to products.csv")

fetch_books_from_url("https://books.toscrape.com/")
fetch_products_from_url("https://www.swoop.ge/category/23/notebooki")
