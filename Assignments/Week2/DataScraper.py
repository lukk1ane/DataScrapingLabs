import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import json
import os
import logging
from time import sleep

class ECommerceScraper:
    def __init__(self, base_url, output_dir="output"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.products = []
        self.setup_logging()
        self.create_output_directory()

    def setup_logging(self):
        """Set up logging to track progress and errors."""
        logging.basicConfig(
            filename="scraper.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Scraper initialized.")

    def create_output_directory(self):
        """Create the output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"Created output directory: {self.output_dir}")

    def fetch_page(self, url):
        """Fetch the HTML content of a page."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_products(self, html):
        """Parse product data from the HTML content."""
        soup = BeautifulSoup(html, "html.parser")
        products = []

        for item in soup.select(".item-cell"):  # adjusted selector for the target website
            try:
                name = item.select_one(".item-title").get_text(strip=True)
                price = item.select_one(".price-current").get_text(strip=True)
                img_element = item.select_one("img")
                img_url = urljoin(self.base_url, img_element["src"]) if img_element else "No image"
                product = {"name": name, "price": price, "img_url": img_url}
                products.append(product)
            except Exception as e:
                logging.error(f"Error parsing product: {e}")
                continue

        return products

    def download_image(self, img_url, product_name):
        """Download and save an image."""
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            img_name = f"{product_name.replace('/', '_')}.jpg"
            img_path = os.path.join(self.output_dir, img_name)
            with open(img_path, "wb") as img_file:
                img_file.write(response.content)
            logging.info(f"Downloaded image: {img_name}")
        except Exception as e:
            logging.error(f"Failed to download image {img_url}: {e}")

    def save_to_json(self, data, filename="products.json"):
        """Save data to a JSON file."""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"Data saved to JSON: {file_path}")

    def save_to_csv(self, data, filename="products.csv"):
        """Save data to a CSV file."""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["name", "price", "img_url"])
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Data saved to CSV: {file_path}")

    def handle_pagination(self, base_url, query_param="page", max_pages=5):
        """Handle pagination by iterating through multiple pages."""
        for page in range(1, max_pages + 1):
            url = f"{base_url}&{query_param}={page}"
            logging.info(f"Fetching page {page}: {url}")
            html = self.fetch_page(url)
            if not html:
                break

            products = self.parse_products(html)
            self.products.extend(products)

            # download images for products on this page
            for product in products:
                if product["img_url"] != "No image":
                    self.download_image(product["img_url"], product["name"])

            sleep(2)  # add a delay to avoid overloading the server

    def run(self, search_query="laptop"):
        """Run the scraper."""
        search_url = f"{self.base_url}/p/pl?d={search_query}"
        self.handle_pagination(search_url)

        # save data to JSON and CSV
        self.save_to_json(self.products)
        self.save_to_csv(self.products)

        logging.info("Scraping completed.")


# Example Usage
if __name__ == "__main__":
    base_url = "https://www.newegg.com"
    scraper = ECommerceScraper(base_url)
    scraper.run(search_query="laptop")