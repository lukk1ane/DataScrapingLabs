import requests
from bs4 import BeautifulSoup
from lxml import html as lxml_html
import csv
import time
import random
import re


def zoommer_scraper():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/113.0.0.0 Safari/537.36'
    }

    phone_url = 'https://zoommer.ge/mobiluri-telefonebi-c855'
    laptop_url = 'https://zoommer.ge/leptopis-brendebi-c717'

    phone_items = scrape_using_dom(phone_url, headers)
    laptop_items = scrape_with_xpath_logic(laptop_url, headers)

    print("\n[Phones] - Using DOM Tree")
    for item in phone_items[:3]:
        print(f"Name: {item['name']}")
        print(f"Price: {item['price']}")
        print(f"Sale: {item.get('sale', 'None')}")
        print("=" * 40)

    print("\n[Laptops] - Using XPath")
    for item in laptop_items[:3]:
        print(f"Name: {item['name']}")
        print(f"Price: {item['price']}")
        print(f"Link: {item['link']}")
        print("=" * 40)

    export_to_csv(phone_items, 'phones_data.csv')
    export_to_csv(laptop_items, 'laptops_data.csv')

    return phone_items, laptop_items


def scrape_using_dom(link, headers):
    result = requests.get(link, headers=headers)
    if result.status_code != 200:
        print(f"Error fetching: {link}")
        return []

    dom = BeautifulSoup(result.text, 'html.parser')
    items = []

    product_blocks = dom.find_all('div', id=lambda val: val and val.startswith('product-'))

    for block in product_blocks:
        data = {}

        title_tag = block.find('a', title=True)
        if title_tag:
            data['name'] = title_tag['title'].strip()
            data['link'] = 'https://zoommer.ge' + title_tag.get('href', '')

        price_box = block.find('div', class_=lambda c: c and 'sc-7543ba48-7' in c)
        if price_box:
            price_element = price_box.find('h4')
            if price_element:
                data['price'] = sanitize_price(price_element.text)

            sale_info = price_element.find_next_sibling('span')
            if sale_info:
                data['sale'] = sale_info.get_text(strip=True)

        items.append(data)
        time.sleep(random.uniform(0.1, 0.4))

    return items


def scrape_with_xpath_logic(url, headers):
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        print(f"Unable to access: {url}")
        return []

    tree = lxml_html.fromstring(page.content)
    results = []

    product_nodes = tree.xpath('//div[starts-with(@id, "product-")]')

    for node in product_nodes:
        product_info = {}

        title = node.xpath('.//a[@title][1]')
        if title:
            product_info['name'] = title[0].get('title', '').strip()
            product_info['link'] = 'https://zoommer.ge' + title[0].get('href', '')

        price_raw = node.xpath('.//h4[contains(@class, "sc-7543ba48-8")]/text()')
        if price_raw:
            product_info['price'] = sanitize_price(price_raw[0])

        results.append(product_info)
        time.sleep(random.uniform(0.1, 0.4))

    return results


def sanitize_price(text):
    return re.sub(r'[^\d.]', '', text).strip()


def export_to_csv(items, filepath):
    if not items:
        print(f"No data to export for {filepath}")
        return

    with open(filepath, mode='w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)
    print(f"Saved {len(items)} records to {filepath}")


if __name__ == "__main__":
    phones, laptops = zoommer_scraper()
    print(f"\n✔ Scraped {len(phones)} phones and {len(laptops)} laptops")
