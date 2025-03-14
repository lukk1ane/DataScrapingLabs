import requests
from bs4 import BeautifulSoup
import csv
import time

def extract_book_data(book_element):
    """Extract detailed information about a book from its HTML element."""
    title_element = book_element.select_one("h3 a")
    title = title_element.get('title')
    
    
    relative_url = title_element.get('href')
    if relative_url.startswith('catalogue/'):
        url = f"http://books.toscrape.com/{relative_url}"
    else:
        url = f"http://books.toscrape.com/catalogue/{relative_url}"
    
    
    price = book_element.select_one(".price_color").text
    
   
    availability = book_element.select_one(".availability").text.strip()
   
    star_class = book_element.select_one(".star-rating").get('class')
    rating = star_class[1] if len(star_class) > 1 else "No rating"
    
    return {
        'title': title,
        'url': url,
        'price': price,
        'availability': availability,
        'rating': rating
    }

def scrape_page(url):
    """Scrape all books from a single page."""
    response = requests.get(url)
    books = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        book_elements = soup.select("article.product_pod")
        
        for book_element in book_elements:
            book_data = extract_book_data(book_element)
            books.append(book_data)
            
        # Check if there's a next page
        next_button = soup.select_one("li.next a")
        next_page_url = None
        
        if next_button:
            next_page_relative = next_button.get('href')
            # Construct the absolute URL for the next page
            if 'catalogue/' in url:
                base_url = url.split('catalogue/')[0] + 'catalogue/'
            else:
                base_url = url.rsplit('/', 1)[0] + '/'
            next_page_url = base_url + next_page_relative
            
    return books, next_page_url

def save_to_csv(books, filename="books_data.csv"):
    """Save book data to a CSV file."""
    if not books:
        return
        
    keys = books[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

def main():
    start_url = "http://books.toscrape.com/catalogue/page-1.html"
    current_url = start_url
    all_books = []
    page_num = 1
    
    while current_url:
        print(f"Scraping page {page_num}...")
        books, next_page_url = scrape_page(current_url)
        
        all_books.extend(books)
        print(f"Found {len(books)} books on page {page_num}")
        
        # Update for next iteration
        current_url = next_page_url
        page_num += 1
        
        # Be nice to the server with a small delay
        time.sleep(1)
    
    print(f"Total books scraped: {len(all_books)}")
    save_to_csv(all_books)
    print(f"Data saved to books_data.csv")

if __name__ == "__main__":
    main()