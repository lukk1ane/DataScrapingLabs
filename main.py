import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Task 1

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

h3_tags = soup.find_all('h3')

for h3 in h3_tags:
    title = h3.a['title']

    parent = h3.parent
    price_tag = parent.find('p', class_='price_color')

    if price_tag:
        price = price_tag.text
        print(f"title: {title} | price: {price}")

# Task 2

books_container = soup.find_all('article', class_='product_pod')

books_data = []

for book in books_container:
    title = book.h3.a['title'].strip()

    price = book.find('p', class_='price_color').text.strip()

    relative_url = book.h3.a['href']
    full_url = urljoin(url, relative_url)

    product_resp = requests.get(full_url)
    product_soup = BeautifulSoup(product_resp.text, 'html.parser')

    desc_header = product_soup.find('div', id='product_description')
    if desc_header:
        desc_p = desc_header.find_next_sibling('p')
        description = desc_p.text.strip() if desc_p else "No description"
    else:
        description = "No description"

    availability_tag = product_soup.find('th', string='Availability')
    if availability_tag:
        availability = availability_tag.find_next_sibling('td').text.strip()
    else:
        availability = "Not available"

    rating_tag = book.find('p', class_='star-rating')
    if rating_tag and 'class' in rating_tag.attrs:
        classes = rating_tag['class']
        rating = [c for c in classes if c != 'star-rating'][0]
    else:
        rating = "No rating"

    books_data.append({
        'Title': title,
        'Price': price,
        'URL': full_url,
        'Description': description,
        'Availability': availability,
        'Rating': rating
    })


csv_filename = 'books_data.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=books_data[0].keys())
    writer.writeheader()
    writer.writerows(books_data)

for book in books_data:
    print("\n--- Book ---")
    for key, value in book.items():
        print(f"{key}: {value}")

