import requests
from bs4 import BeautifulSoup
import json

URL = "http://nike.com/w/style-your-air-149wq"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def scrape_data(url, headers):
    scraped_data = []

    try:
        print(f"Requesting page: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print("Page requested successfully.")

        soup = BeautifulSoup(response.content, 'lxml')
        print("HTML parsed successfully.")

        product_cards = soup.find_all('div', class_='product-card')
        print(f"Found {len(product_cards)} potential product cards.")

        if not product_cards:
            print("No product cards found with the specified class. Website structure might have changed.")
            return []

        count = 0
        for card in product_cards:
            product_info = {}

            try:
                link_element = card.find('a', class_='product-card__link-overlay')
                if link_element and link_element.has_attr('href'):
                    product_info['url'] = link_element['href']
                else:
                    product_info['url'] = None

                title_element = card.find('div', class_='product-card__title')
                product_info['title'] = title_element.get_text(strip=True) if title_element else None

                subtitle_element = card.find('div', class_='product-card__subtitle')
                product_info['subtitle'] = subtitle_element.get_text(strip=True) if subtitle_element else None

                price_element = card.select_one(
                    '[data-testid="product-price"], .product-price')
                if price_element:
                    product_info['price'] = price_element.get_text(strip=True)
                else:
                    price_container = card.find(class_='product-price')
                    product_info['price'] = price_container.get_text(strip=True) if price_container else None

                if product_info.get('title') and product_info.get('url'):
                    scraped_data.append(product_info)
                    count += 1
                    print(f"Successfully extracted data for: {product_info.get('title')}")
                else:
                    print("Skipping card - missing essential data (title or URL).")


            except Exception as e:
                print(f"Error processing a product card: {e}")

        print(f"\nFinished scraping. Extracted data for {len(scraped_data)} products.")
        return scraped_data

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []


if __name__ == "__main__":
    extracted_products = scrape_data(URL, HEADERS)

    if extracted_products:
        print("\n--- Extracted Product Data ---")
        print(json.dumps(extracted_products, indent=4))
    else:
        print("\nNo product data was extracted.")
