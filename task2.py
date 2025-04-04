import requests
from bs4 import BeautifulSoup
import time
import csv
import os

def scrape_books_to_scrape():
    """
    Function to scrape book titles and prices from books.toscrape.com
    using parent-child relationships.
    """
    print("Starting to scrape books.toscrape.com...")
    
    try:
        # Send HTTP request to BooksToScrape.com
        url = "https://books.toscrape.com/"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []
            
        print(f"Successfully connected to {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all book containers
        book_containers = soup.select('article.product_pod')
        print(f"Found {len(book_containers)} books on the page")
        
        if not book_containers:
            print("No book containers found. The website structure might have changed.")
            return []
        
        # Extract book titles and prices
        books = []
        for container in book_containers:
            # Get the title using the h3 element
            h3_tag = container.find('h3')
            title = h3_tag.find('a').get('title') if h3_tag else "Title not found"
            
            # Navigate to find the price using parent relationships
            price_element = container.find('p', class_='price_color')
            price = price_element.text if price_element else "Price not found"
            
            # Get the rating
            rating_element = container.find('p', class_='star-rating')
            rating = rating_element.get('class')[1] if rating_element and 'class' in rating_element.attrs else "Rating not found"
            
            # Get the book URL
            url_element = container.find('a')
            book_url = url + url_element.get('href') if url_element else "URL not found"
            
            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "url": book_url
            })
        
        # Print results
        print("\n--- Books from books.toscrape.com ---")
        for i, book in enumerate(books, 1):
            print(f"Book {i}:")
            print(f"Title: {book['title']}")
            print(f"Price: {book['price']}")
            print(f"Rating: {book['rating']}")
            print(f"URL: {book['url']}")
            print("-" * 50)
            
        # Save to CSV
        with open('books_to_scrape.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=books[0].keys())
            writer.writeheader()
            writer.writerows(books)
            
        print(f"Saved data to books_to_scrape.csv")
        return books
            
    except Exception as e:
        print(f"Error while scraping books.toscrape.com: {e}")
        return []

def scrape_zoomer():
    """
    Function to scrape product data from zoomer.ge using parent-child relationships,
    sibling relationships, and attribute selection.
    """
    print("\nStarting to scrape zoomer.ge...")
    
    try:
       
        url = "https://zoomer.ge/smartphones"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        print(f"Connecting to {url}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []
            
        print(f"Successfully connected to {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        product_containers = soup.select('div.product-layout')
        print(f"Found {len(product_containers)} product containers")
        
        if not product_containers:
           
            product_containers = soup.select('div.product-grid-item')
            print(f"Trying alternate selector. Found {len(product_containers)} product containers")
        
        if not product_containers:
            
            print("No product containers found. The website structure might have changed.")
            print("HTML sample:")
            print(soup.prettify()[:1000]) 
            return []
        
        products = []
        for container in product_containers[:10]:  
            try:
       
                name_element = container.select_one('h4.product-name') or container.select_one('h3.product-title')
                name = name_element.text.strip() if name_element else "Name not found"
                
               
                price_element = container.select_one('span.price-new') or container.select_one('span.price')
                price = price_element.text.strip() if price_element else "Price not found"
                
               
                url_element = container.select_one('a.product-img') or container.select_one('a.product-image')
                product_url = ""
                if url_element and url_element.has_attr('href'):
                    product_url = url_element['href']
                    if not product_url.startswith('http'):
                        product_url = f"https://zoomer.ge{product_url}"
                else:
                    product_url = "URL not found"
                
                
                img_element = container.select_one('img')
                img_url = img_element['src'] if img_element and img_element.has_attr('src') else "Image URL not found"
                if img_url and not img_url.startswith('http'):
                    img_url = f"https://zoomer.ge{img_url}"
                
                
                description_element = container.select_one('div.description') or container.select_one('p.description')
                description = description_element.text.strip() if description_element else "Description not found"
                
                products.append({
                    "name": name,
                    "price": price,
                    "url": product_url,
                    "img_url": img_url,
                    "description": description
                })
            except Exception as e:
                print(f"Error processing a product: {e}")
   
        print("\n--- Products from zoomer.ge ---")
        for i, product in enumerate(products, 1):
            print(f"Product {i}:")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"URL: {product['url']}")
            print(f"Image URL: {product['img_url']}")
            print(f"Description: {product['description']}")
            print("-" * 50)
        
       
        if products:
            with open('zoomer_products.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=products[0].keys())
                writer.writeheader()
                writer.writerows(products)
                
            print(f"Saved data to zoomer_products.csv")
        
        return products
            
    except Exception as e:
        print(f"Error while scraping zoomer.ge: {e}")
        return []

def scrape_mymarket():
    """
    Function to scrape product data from mymarket.ge using parent-child relationships,
    sibling relationships, and attribute selection.
    """
    print("\nStarting to scrape mymarket.ge...")
    
    try:
        
        url = "https://mymarket.ge/ka/search/electronics"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        print(f"Connecting to {url}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []
            
        print(f"Successfully connected to {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
    
        product_containers = soup.select('div.article-in-list') or soup.select('div.s-article-item')
        print(f"Found {len(product_containers)} product containers")
        
        if not product_containers:
            print("No product containers found. The website structure might have changed.")
            print("HTML sample:")
            print(soup.prettify()[:1000])  
            return []
        
        products = []
        for container in product_containers[:10]:  
            try:
              
                name_element = container.select_one('p.article-title') or container.select_one('h5.product-title')
                name = name_element.text.strip() if name_element else "Name not found"
                
                
                price_element = container.select_one('div.article-price') or container.select_one('div.product-price')
                price = price_element.text.strip() if price_element else "Price not found"
                
             
                url_element = container.select_one('a.link-to-product') or container.select_one('a')
                product_url = ""
                if url_element and url_element.has_attr('href'):
                    product_url = url_element['href']
                    if not product_url.startswith('http'):
                        product_url = f"https://mymarket.ge{product_url}"
                else:
                    product_url = "URL not found"
                
             
                img_element = container.select_one('img.article-image') or container.select_one('img')
                img_url = img_element['src'] if img_element and img_element.has_attr('src') else "Image URL not found"
                if img_url and not img_url.startswith('http'):
                    img_url = f"https://mymarket.ge{img_url}"
                
              
                location_element = container.select_one('div.location') or container.select_one('div.product-location')
                location = location_element.text.strip() if location_element else "Location not found"
                
                products.append({
                    "name": name,
                    "price": price,
                    "url": product_url,
                    "img_url": img_url,
                    "location": location
                })
            except Exception as e:
                print(f"Error processing a product: {e}")
        
       
        print("\n--- Products from mymarket.ge ---")
        for i, product in enumerate(products, 1):
            print(f"Product {i}:")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"URL: {product['url']}")
            print(f"Image URL: {product['img_url']}")
            print(f"Location: {product['location']}")
            print("-" * 50)
        
     
        if products:
            with open('mymarket_products.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=products[0].keys())
                writer.writeheader()
                writer.writerows(products)
                
            print(f"Saved data to mymarket_products.csv")
        
        return products
            
    except Exception as e:
        print(f"Error while scraping mymarket.ge: {e}")
        return []

def main():
    print("Web Scraping Script Started")
    print("=" * 50)
    
   
    output_dir = "scraped_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
   
    books = scrape_books_to_scrape()
    
   
    time.sleep(2)
    

    zoomer_products = scrape_zoomer()
    

    time.sleep(2)
    
    
    mymarket_products = scrape_mymarket()
    
    print("\nScraping completed!")
    print(f"Total books scraped: {len(books)}")
    print(f"Total zoomer.ge products scraped: {len(zoomer_products)}")
    print(f"Total mymarket.ge products scraped: {len(mymarket_products)}")
    print("=" * 50)

if __name__ == "__main__":
    main()