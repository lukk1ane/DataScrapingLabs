import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree


def scrape_books():
    url = "https://books.toscrape.com/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for h3_tag in soup.find_all('h3'):
        title = h3_tag.a.attrs['title']
        parent = h3_tag.find_parent('article')
        price = parent.find('p', class_='price_color').text if parent else 'N/A'
        books.append({'Title': title, 'Price': price})

    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price'])
        writer.writeheader()
        writer.writerows(books)

    print("Books data saved to books.csv")


def scrape_other_website(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})  # Avoid bot blocking

    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    dom = etree.HTML(response.content)  # Use response.content for lxml

    products = []

    # Flexible container detection (adjust class based on target site)
    main_container = soup.find('div', class_=lambda x: x and ('products' in x or 'list' in x or 'items' in x))
    if not main_container:
        print("Could not find main container. Trying alternative search...")
        main_container = soup.find(['section', 'ul', 'div'], class_=True)  # Fallback

    if not main_container:
        print("No suitable container found.")
        return

    for product in main_container.find_all(['div', 'li'], class_=lambda x: x and ('item' in x or 'product' in x)):
        # Extract title (prioritize <h2>, <h3>, or <a> tags)
        title_elem = product.find(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x or 'name' in x))
        title = title_elem.text.strip() if title_elem else 'N/A'

        # Extract price (look for common price classes)
        price_elem = product.find(class_=lambda x: x and ('price' in x or 'cost' in x))
        price = price_elem.text.strip() if price_elem else 'N/A'

        # Use sibling to find description (if exists)
        description = 'N/A'
        if title_elem:
            description_elem = title_elem.find_next_sibling('p')
            description = description_elem.text.strip() if description_elem else 'N/A'

        # Use XPath to extract URL (more robust than hardcoded classes)
        product_url = dom.xpath(".//a[contains(@href, 'product') or contains(@href, 'item')]/@href")
        product_url = product_url[0] if product_url else 'N/A'

        products.append({
            'Title': title,
            'Price': price,
            'Description': description,
            'URL': product_url
        })

    if not products:
        print("No products found. Check selectors.")
        return

    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Description', 'URL'])
        writer.writeheader()
        writer.writerows(products)

    print(f"Data saved to products.csv (found {len(products)} items)")


# Run the functions
scrape_books()
scrape_other_website("https://www.swoop.ge/category/23/notebooki")  # Example URL