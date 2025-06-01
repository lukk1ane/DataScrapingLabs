import requests
from bs4 import BeautifulSoup
import csv
import re
import os

def get_page_content(url):
    """Fetch webpage content and return BeautifulSoup object"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def clean_price(price_text):
    """Clean price data by removing currency symbols and converting to float"""
    try:
        # Remove currency symbol and convert to float using regular expressions
        # This regex will remove any non-digit characters except for the decimal point
        clean_price = re.sub(r'[^\d\.]', '', price_text)
        return float(clean_price)
    except (ValueError, TypeError) as e:
        print(f"Error cleaning price {price_text}: {e}")
        return None

def clean_text(text):
    """Clean text by removing excess whitespace and unwanted characters"""
    if text:
        # Replace multiple spaces and newlines with a single space using regular expressions
        # This regex will replace multiple whitespace characters with a single space
        clean = re.sub(r'\s+', ' ', text)
        return clean.strip()
    return ""

def extract_product_info(product_url):
    """Extract detailed product information from a product page"""
    soup = get_page_content(product_url)
    if not soup:
        return None
    
    # variable to store product information (titles, prices, availability, etc.)
    product_info = {}
    
    try:
        # Extract product title
        product_info['title'] = clean_text(soup.select_one('.product_main h1').text)
    except (AttributeError, TypeError) as e:
        print(f"Error extracting title: {e}")
        product_info['title'] = "N/A"
    
    try:
        # Extract price
        price_text = soup.select_one('.price_color').text
        product_info['price'] = clean_price(price_text)
    except (AttributeError, TypeError) as e:
        print(f"Error extracting price: {e}")
        product_info['price'] = None
    
    try:
        # Extract availability
        availability = soup.select_one('.availability')
        product_info['availability'] = clean_text(availability.text) if availability else "N/A"
    except (AttributeError, TypeError) as e:
        print(f"Error extracting availability: {e}")
        product_info['availability'] = "N/A"
    
    try:
        # Extract product description
        product_description = soup.select_one('#product_description + p')
        product_info['description'] = clean_text(product_description.text) if product_description else "No description available"
    except (AttributeError, TypeError) as e:
        print(f"Error extracting description: {e}")
        product_info['description'] = "N/A"
    
    try:
        # Extract product information from table
        table_rows = soup.select('table.table-striped tr')
        for row in table_rows:
            header = clean_text(row.select_one('th').text)
            value = clean_text(row.select_one('td').text)
            product_info[header] = value
    except (AttributeError, TypeError) as e:
        print(f"Error extracting table data: {e}")
    
    try:
        # Extract category using parent-child relationships
        breadcrumb = soup.select('.breadcrumb li')
        if len(breadcrumb) >= 3:
            product_info['category'] = clean_text(breadcrumb[2].text)
        else:
            product_info['category'] = "N/A"
    except (AttributeError, IndexError, TypeError) as e:
        print(f"Error extracting category: {e}")
        product_info['category'] = "N/A"
    
    try:
        # Extract rating
        rating_class = soup.select_one('p.star-rating')['class']
        rating_text = [cls for cls in rating_class if cls != 'star-rating'][0]
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        product_info['rating'] = ratings.get(rating_text, 0)
    except (AttributeError, IndexError, TypeError, KeyError) as e:
        print(f"Error extracting rating: {e}")
        product_info['rating'] = 0
    
    return product_info

def scrape_books(base_url, num_books=5):
    """Scrape books from the website"""
    books = []
    page_url = base_url
    base_domain = "http://books.toscrape.com"
    
    while len(books) < num_books:
        print(f"Scraping page: {page_url}")
        soup = get_page_content(page_url)
        if not soup:
            break
        
        book_containers = soup.select('.product_pod')
        
        for book in book_containers:
            if len(books) >= num_books:
                break
                
            try:
                # Get book details URL
                book_url_element = book.select_one('h3 a')
                if not book_url_element or 'href' not in book_url_element.attrs:
                    continue
                    
                relative_url = book_url_element['href']
                
                # Convert relative URL to absolute URL
                if relative_url.startswith('../'):
                    # Remove the '../' prefix and join with base domain
                    book_url = f"{base_domain}/catalogue/{relative_url.replace('../', '')}"
                else:
                    # If it's already a full path or starts with '/'
                    if relative_url.startswith('/'):
                        book_url = f"{base_domain}{relative_url}"
                    else:
                        # If it's a relative path from current directory
                        current_dir = '/'.join(page_url.split('/')[:-1])
                        book_url = f"{current_dir}/{relative_url}"
                
                # Fetch and process book details
                book_info = extract_product_info(book_url)
                if book_info:
                    books.append(book_info)
                    print(f"Scraped book: {book_info.get('title', 'Unknown')}")
            except Exception as e:
                print(f"Error processing a book: {e}")
        
        # Check if there's a next page needed to scrape
        # Find the next button in pagination
        next_button = soup.select_one('li.next a')
        if next_button and len(books) < num_books:
            next_url = next_button['href']
            
            # Handle relative URLs for pagination
            if '../' in next_url:
                # Go up one directory level
                current_dir = '/'.join(page_url.split('/')[:-1])
                current_dir = '/'.join(current_dir.split('/')[:-1])  # Go up another level for '../'
                page_url = f"{current_dir}/{next_url.replace('../', '')}"
            else:
                # Stay in same directory
                current_dir = '/'.join(page_url.split('/')[:-1])
                page_url = f"{current_dir}/{next_url}"
        else:
            break
    
    return books

def save_to_csv(books, filename='books_data.csv'):
    """Save scraped book data to CSV file"""
    if not books:
        print("No data to save.")
        return
    
    # Get all unique keys from all books
    fieldnames = set()
    for book in books:
        fieldnames.update(book.keys())
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(books)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    base_url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    
    books = scrape_books(base_url, num_books=10)
    
    if books:
        print(f"Successfully scraped {len(books)} books")
        save_to_csv(books)
    else:
        print("Failed to scrape any books.")

if __name__ == "__main__":
    main()