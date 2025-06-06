import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
from urllib.parse import urljoin, urlparse


# 1. User-Agent Rotation: Cycle through at least 5 different browser User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/14.1.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

base_url = "https://books.toscrape.com/"



# 2. Smart Delays: Variable delays (1-3s for navigation, 3-6s for reading pages)
def smart_delay(page_type="navigation"):
    if page_type == "navigation":
        delay = random.uniform(1, 3)
    else:
        delay = random.uniform(3, 6)
    time.sleep(delay)


# 3. Session Management: Use persistent sessions with cookie handling
def get_session():
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    return session


# 6. Request Headers: Include realistic Accept, Referer, and other headers
def get_random_headers(referer=None):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    if referer:
        headers["Referer"] = referer
    return headers

def make_request_with_retry(session, url, max_retries=3, referer=None):
    for attempt in range(max_retries):
        try:
            headers = get_random_headers(referer)
            session.headers.update(headers)
            
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                print(f"failed to fetch {url} after {max_retries} attempts: {e}")
                return None
            
            # 5. Error Handling: Retry mechanism with exponential backoff
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"request failed, retrying in {wait_time:.2f}s...")
            time.sleep(wait_time)
    
    return None

def extract_star_rating(soup):
    rating_element = soup.find("p", class_=re.compile(r"star-rating"))
    if rating_element:
        rating_text = rating_element.get("class")[1]
        rating_map = {
            "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
        }
        return rating_map.get(rating_text, 0)
    return 0

def scrape_book(session, book_url, category):    
    response = make_request_with_retry(session, book_url, referer=base_url)
    if not response:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    smart_delay("reading")
    
    try:
        title = soup.find("h1").text.strip()
        price_element = soup.find("p", class_="price_color")
        price = price_element.text.strip() if price_element else "N/A"
        availability_element = soup.find("p", class_="instock availability")
        availability = availability_element.text.strip() if availability_element else "N/A"
        star_rating = extract_star_rating(soup)
        description_element = soup.find("div", id="product_description")
        if description_element and description_element.find_next_sibling("p"):
            description = description_element.find_next_sibling("p").text.strip()
        else:
            description = "no description available"
        
        return {
            "title": title,
            "price": price,
            "availability": availability,
            "star_rating": star_rating,
            "description": description,
            "category": category
        }
        
    except Exception as e:
        print(f"error extracting book details from {book_url}: {e}")
        return None

def get_categories(session):
    response = make_request_with_retry(session, base_url)
    if not response:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    smart_delay("navigation")
    
    categories = []
    category_links = soup.find("div", class_="side_categories").find_all("a")[1:]
    
    for link in category_links:
        category_name = link.text.strip()
        category_url = urljoin(base_url, link.get("href"))
        categories.append({
            "name": category_name,
            "url": category_url
        })
    
    return categories

def scrape_category_books(session, category_url, category_name, target_books=7):
    books = []
    page = 1
    
    while len(books) < target_books:
        if page == 1:
            url = category_url
        else:
            url = category_url.replace("index.html", f"page-{page}.html")
        
        response = make_request_with_retry(session, url, referer=base_url)
        if not response:
            break
            
        soup = BeautifulSoup(response.text, "html.parser")
        smart_delay("navigation")
        
        book_links = soup.find_all("h3")
        if not book_links:
            break
        
        for book_link in book_links:
            if len(books) >= target_books:
                break
                
            relative_url = book_link.find("a").get("href")
            book_url = urljoin(category_url, relative_url)
            
            book_data = scrape_book(session, book_url, category_name)
            
            if book_data and book_data["star_rating"] >= 4:
                books.append(book_data)
        
        page += 1
        
        if page > 10:
            break
    
    return books

def validate_book_data(book):
    required_fields = ["title", "price", "availability", "star_rating", "description", "category"]
    
    for field in required_fields:
        if field not in book or not book[field]:
            return False
    
    if not isinstance(book["star_rating"], int) or book["star_rating"] < 1 or book["star_rating"] > 5:
        return False
    
    return True

def save_to_csv(books, filename="scraped_books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "price", "availability", "star_rating", "description", "category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for book in books:
            book["description"] = book["description"].replace("\n", " ").replace("\r", " ")
            writer.writerow(book)
    

def main():
    session = get_session()
    all_books = []
    
    categories = get_categories(session)
    if len(categories) < 3:
        print("could not fetch 3 categories")
        return
    
    selected_categories = random.sample(categories, 3)
    books_per_category = 7
    
    for category in selected_categories:
        category_books = scrape_category_books(
            session, 
            category["url"], 
            category["name"], 
            books_per_category
        )
        all_books.extend(category_books)
        
        smart_delay("navigation")
    
    if len(all_books) < 20:
        print(f"only found {len(all_books)} books with 4+ stars")
    
    save_to_csv(all_books)
    

    star_distribution = {}
    for book in all_books:
        stars = book["star_rating"]
        star_distribution[stars] = star_distribution.get(stars, 0) + 1
    
    print(f"star rating distribution: {star_distribution}")

main()
