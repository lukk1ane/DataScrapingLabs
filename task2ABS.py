import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def scrape_books_to_scrape():
    base_url = 'https://books.toscrape.com/'
    
    response = requests.get(base_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    main_container = soup.find('div', class_='container-fluid')
    
    book_articles = main_container.select('article.product_pod')
    
    all_books = []
    
    for book in book_articles:
        book_data = {}
        
        title_element = book.h3.a
        book_data['title'] = title_element.get('title')
        
        relative_url = title_element.get('href')
        book_data['url'] = urljoin(base_url, relative_url)
        
        price_element = book.select_one('div.product_price p.price_color')
        book_data['price'] = price_element.text if price_element else 'Not available'
        
        availability_element = price_element.find_next_sibling('p', class_='instock availability')
        book_data['availability'] = availability_element.text.strip() if availability_element else 'Unknown'
        
        rating_element = book.select_one('p.star-rating')
        if rating_element:
            rating_classes = rating_element.get('class')
            rating = [cls for cls in rating_classes if cls != 'star-rating'][0]
            book_data['rating'] = rating
        else:
            book_data['rating'] = 'No rating'
        
        all_books.append(book_data)
    
    return all_books

def scrape_book_details(book_url):
    """Scrape detailed information about a specific book."""
    response = requests.get(book_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the book page. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    book_details = {}
    
    product_description = soup.select_one('#product_description ~ p')
    book_details['description'] = product_description.text if product_description else 'No description available'
    
    product_info_table = soup.select_one('table.table-striped')
    
    if product_info_table:
        rows = product_info_table.select('tr')
        for row in rows:
            header = row.select_one('th')
            data = row.select_one('td')
            if header and data:
                key = header.text.strip()
                value = data.text.strip()
                book_details[key] = value
    
    return book_details

def save_to_csv(books_data, filename="books_data.csv"):
    """Save the extracted data to a CSV file."""
    if not books_data:
        print("No data to save.")
        return
    
    fieldnames = set()
    for book in books_data:
        fieldnames.update(book.keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books_data)
    
    print(f"Data saved to {filename}")

def main():
    books_list = scrape_books_to_scrape()
    
    if not books_list:
        print("Failed to scrape books list.")
        return
    
    print(f"Found {len(books_list)} books on the main page.")
    
    print("\nExample of scraped books:")
    for i, book in enumerate(books_list[:5], 1):
        print(f"\nBook {i}:")
        for key, value in book.items():
            print(f"{key}: {value}")
    
    print("\nScraping detailed information for 2 books:")
    
    enhanced_books = []
    for i, book in enumerate(books_list[:2]):
        print(f"\nScraping details for: {book['title']}")
        
        time.sleep(1)
        
        details = scrape_book_details(book['url'])
        if details:
            combined_data = {**book, **details}
            enhanced_books.append(combined_data)
            
            print(f"Enhanced data for {book['title']}:")
            for key, value in combined_data.items():
                if key == 'description':
                    print(f"description: {value[:100]}...")
                else:
                    print(f"{key}: {value}")
    
    save_to_csv(books_list, "all_books.csv")
    
    if enhanced_books:
        save_to_csv(enhanced_books, "enhanced_books.csv")

if __name__ == "__main__":
    main()