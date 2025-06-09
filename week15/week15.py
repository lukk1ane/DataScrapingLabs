import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import random
import csv
import logging
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
CSV_FILE = "advanced_books_scraper_results.csv"
BOOKS_TO_SCRAPE = 20
MINIMUM_CATEGORIES = 3
MINIMUM_STAR_RATING = 4

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1'
]

STAR_RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


def setup_session():
    """
    Sets up a requests.Session with robust anti-detection features.
    3. Session Management: A single session object handles cookies across requests.
    5. Error Handling: A retry mechanism with exponential backoff for robustness.
    6. Request Headers: Realistic default headers are set.
    """
    session = requests.Session()
    
    retries = Retry(
        total=5,
        backoff_factor=1,  # e.g., sleeps for 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[500, 502, 503, 504] # Retry on server errors
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',

        
        'Connection': 'keep-alive',
    })
    
    return session

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def navigation_delay():
    delay = random.uniform(1, 3)
    time.sleep(delay)

def reading_delay():
    delay = random.uniform(3, 6)
    time.sleep(delay)

def get_page_content(session, url, referer=None):

    headers = session.headers.copy()
    headers['User-Agent'] = get_random_user_agent()
    if referer:
        headers['Referer'] = referer
    
    try:
        response = session.get(url, headers=headers, timeout=20)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        return BeautifulSoup(response.text, 'html.parser')


    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def get_category_urls(session, base_url):

    logging.info("Fetching category URLs from the homepage...")
    soup = get_page_content(session, base_url)
    if not soup:
        return []

    try:
        with open("debug_homepage.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        logging.info("Saved the received HTML to debug_homepage.html for inspection.")
    except Exception as e:
        logging.error(f"Could not write debug file: {e}")

    
    if not category_links:
        logging.warning("The CSS selector did not find any category links in the received HTML.")
        logging.warning("Please inspect 'debug_homepage.html' to see what your script received.")

    urls = [urljoin(base_url, link['href']) for link in category_links]
    random.shuffle(urls)  # Randomize to avoid predictable patterns
    logging.info(f"Found {len(urls)} category URLs. Shuffling for variety.")
    return urls

def parse_book_page(soup, category_name):
    try:
        title = soup.find('h1').text.strip()
        price = soup.select_one('p.price_color').text.strip()
        availability = soup.select_one('p.instock.availability').text.strip()
        
        rating_tag = soup.select_one('p.star-rating')
        rating_class = rating_tag['class'][-1]
        star_rating = STAR_RATING_MAP.get(rating_class, 0)

        description_tag = soup.select_one('#product_description ~ p')
        description = description_tag.text.strip() if description_tag else "No description available."
        
        return {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Star Rating': star_rating,
            'Description': description,
            'Category': category_name
        }
    except (AttributeError, IndexError) as e:
        logging.error(f"Error parsing a book page element: {e}. Skipping book.")
        return None

def scrape():
    session = setup_session()
    all_books_data = []
    scraped_categories = set()

    category_urls = get_category_urls(session, BASE_URL)
    if not category_urls:
        logging.critical("Could not retrieve category URLs. Aborting.")
        return

    logging.info(f"Goal: {BOOKS_TO_SCRAPE} books with {MINIMUM_STAR_RATING}+ stars from at least {MINIMUM_CATEGORIES} categories.")
    
    for category_url in category_urls:
        if len(all_books_data) >= BOOKS_TO_SCRAPE and len(scraped_categories) >= MINIMUM_CATEGORIES:
            break
            
        current_page_url = category_url
        category_name = ""
        
        while current_page_url:
            if len(all_books_data) >= BOOKS_TO_SCRAPE and len(scraped_categories) >= MINIMUM_CATEGORIES:
                break
            
            logging.info(f"Navigating to category page: {current_page_url}")
            navigation_delay()
            soup = get_page_content(session, current_page_url, referer=BASE_URL)
            if not soup:
                break

            if not category_name:
                category_name = soup.find('h1').text.strip()

            books_on_page = soup.select('article.product_pod')

            for book_article in books_on_page:
                # Smart Filtering: Check rating on the category page to avoid unnecessary requests
                rating_class = book_article.select_one('p.star-rating')['class'][-1]
                rating_value = STAR_RATING_MAP.get(rating_class, 0)

                if rating_value >= MINIMUM_STAR_RATING:
                    book_relative_url = book_article.find('h3').find('a')['href']
                    book_url = urljoin(current_page_url, book_relative_url)
                    
                    logging.info(f"High rating ({rating_value} stars) found. Visiting book page: {book_url}")
                    reading_delay()
                    book_soup = get_page_content(session, book_url, referer=current_page_url)
                    
                    if book_soup:
                        book_data = parse_book_page(book_soup, category_name)
                        if book_data:
                            all_books_data.append(book_data)
                            scraped_categories.add(category_name)
                            logging.info(f"Scraped '{book_data['Title']}' [{len(all_books_data)}/{BOOKS_TO_SCRAPE}] from category '{category_name}'.")
                            
                            if len(all_books_data) >= BOOKS_TO_SCRAPE and len(scraped_categories) >= MINIMUM_CATEGORIES:
                                break
            
            next_page_tag = soup.select_one('li.next a')
            current_page_url = urljoin(current_page_url, next_page_tag['href']) if next_page_tag else None

    logging.info(f"Scraping finished. Total books: {len(all_books_data)}. Categories: {len(scraped_categories)}.")
    return all_books_data

def save_to_csv(data, filename):
    if not data:
        logging.warning("No data was collected to save.")
        return
    
    # Use the keys from the first dictionary as headers
    fieldnames = list(data[0].keys())
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                # Basic validation: ensure all expected keys are in the row
                validated_row = {key: row.get(key, 'N/A') for key in fieldnames}
                writer.writerow(validated_row)
        logging.info(f"Data successfully saved to {filename}")
    except IOError as e:
        logging.error(f"Error writing to file {filename}: {e}")

if __name__ == "__main__":
    scraped_data = scrape()
    if scraped_data:
        save_to_csv(scraped_data, CSV_FILE)
    else:
        logging.error("Scraping did not yield any data. The CSV file was not created.")
