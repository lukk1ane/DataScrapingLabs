import requests
from bs4 import BeautifulSoup
from lxml import html
import csv
import time
import random
import re


def scrape_zoommer():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # example 1: scrape phones
    phones_url = 'https://zoommer.ge/mobiluri-telefonebi-c855'
    phone_data = scrape_with_relationships(phones_url, headers)

    # example 2 scrape laptops
    laptops_url = 'https://zoommer.ge/leptopis-brendebi-c717'
    laptop_data = scrape_with_xpath(laptops_url, headers)

    # print samples
    print("\n--- PHONES (Parent-Child + Siblings) ---")
    for product in phone_data[:3]:
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"Discount: {product.get('discount', 'N/A')}")
        print("-" * 50)

    print("\n--- LAPTOPS (XPath) ---")
    for product in laptop_data[:3]:
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"URL: {product['url']}")
        print("-" * 50)

    # save to csv
    save_to_csv(phone_data, 'zoommer_phones.csv')
    save_to_csv(laptop_data, 'zoommer_laptops.csv')

    return phone_data, laptop_data


# scrape using parent-child and sibling relationships
def scrape_with_relationships(url, headers):

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    # find all product containers
    product_containers = soup.find_all('div', id=lambda x: x and x.startswith('product-'))

    for container in product_containers:
        product = {}

        # parent-child: container -> title link
        title_link = container.find('a', title=True)
        if title_link:
            product['title'] = title_link.get('title', '').strip()
            product['url'] = 'https://zoommer.ge' + title_link.get('href', '')

        # parent-child -> sibling -> Price and discount
        price_div = container.find('div', class_=lambda x: x and 'sc-7543ba48-7' in x)  # Price container
        if price_div:
            # child: Price in h4
            price_h4 = price_div.find('h4')
            if price_h4:
                product['price'] = clean_price(price_h4.text)

            # sibling -> discount
            discount_span = price_h4.find_next_sibling('span')
            if discount_span:
                product['discount'] = discount_span.text.strip()

        products.append(product)
        time.sleep(random.uniform(0.1, 0.5))

    return products


# scrape using XPath selectors
def scrape_with_xpath(url, headers):

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    tree = html.fromstring(response.content)
    products = []

    # XPath to get all product containers
    product_nodes = tree.xpath('//div[contains(@id, "product-")]')

    for node in product_nodes:
        product = {}

        # XPath for title and URL
        title_node = node.xpath('.//a[@title][1]')
        if title_node:
            product['title'] = title_node[0].get('title', '').strip()
            product['url'] = 'https://zoommer.ge' + title_node[0].get('href', '')

        # XPath for price
        price_node = node.xpath('.//h4[contains(@class, "sc-7543ba48-8")]/text()')
        if price_node:
            product['price'] = clean_price(price_node[0])

        products.append(product)
        time.sleep(random.uniform(0.1, 0.5))

    return products


# remove unwanted characters
def clean_price(price_str):
    return re.sub(r'[^\d.]', '', price_str).strip()


def save_to_csv(data, filename):
    if not data:
        print(f"No data to save to {filename}")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} items to {filename}")


if __name__ == "__main__":
    phone_data, laptop_data = scrape_zoommer()
    print(f"\nScraped {len(phone_data)} phones and {len(laptop_data)} laptops")