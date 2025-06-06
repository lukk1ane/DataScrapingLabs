import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from fake_useragent import UserAgent

BASE_URL = 'https://books.toscrape.com/'
CATEGORY_URL = BASE_URL + 'catalogue/category/books/'
CSV_FILE = 'books_scraped.csv'

ua = UserAgent()
USER_AGENTS = [ua.chrome, ua.firefox, ua.safari, ua.opera, ua.edge]

STAR_MAP = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}

def get_headers(referer=None):
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': referer if referer else BASE_URL,
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

def smart_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def retry_request(session, url, headers, max_retries=3):
    backoff = 1
    for attempt in range(max_retries):
        try:
            resp = session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(backoff)
                backoff *= 2
    return None

def get_categories(session):
    resp = retry_request(session, BASE_URL, get_headers())
    soup = BeautifulSoup(resp.text, 'html.parser')
    cats = soup.select('div.side_categories ul li ul li a')
    categories = []
    for cat in cats:
        name = cat.text.strip()
        url = BASE_URL + cat['href']
        categories.append({'name': name, 'url': url})
    return categories

def parse_book(session, url, referer):
    headers = get_headers(referer)
    smart_delay(3, 6)
    resp = retry_request(session, url, headers)
    if not resp:
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')
    try:
        title = soup.h1.text.strip()
        price = soup.select_one('p.price_color').text.strip()
        availability = soup.select_one('p.instock.availability').text.strip()
        desc = soup.select_one('article.product_page > p')
        description = desc.text.strip() if desc else ""
        category = soup.select('ul.breadcrumb li a')[-1].text.strip()
        star = soup.select_one('p.star-rating')
        for k in STAR_MAP:
            if star and k in star['class']:
                rating = STAR_MAP[k]
                break
        else:
            rating = 0
        return {
            'title': title,
            'price': price,
            'availability': availability,
            'star_rating': rating,
            'description': description,
            'category': category
        }
    except Exception as e:
        return None

def scrape_books():
    session = requests.Session()
    books = []
    categories = get_categories(session)
    random.shuffle(categories)
    selected_categories = categories[:3]

    for cat in selected_categories:
        page_url = cat['url']
        while page_url and len(books) < 20:
            headers = get_headers(BASE_URL)
            smart_delay(1, 3)
            resp = retry_request(session, page_url, headers)
            if not resp:
                break
            soup = BeautifulSoup(resp.text, 'html.parser')
            book_links = [BASE_URL + 'catalogue/' + x.a['href'].replace('../../../', '') for x in soup.select('h3')]
            random.shuffle(book_links)
            for book_url in book_links:
                if len(books) >= 20:
                    break
                data = parse_book(session, book_url, page_url)
                if data and data['star_rating'] >= 4:
                    # Data validation
                    if all(data.values()):
                        books.append(data)
            next_btn = soup.select_one('li.next a')
            if next_btn:
                page_url = cat['url'].rsplit('/', 1)[0] + '/' + next_btn['href']
            else:
                break
    return books

def save_csv(books):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'title', 'price', 'availability', 'star_rating', 'description', 'category'
        ])
        writer.writeheader()
        for b in books:
            writer.writerow(b)

if __name__ == "__main__":
    books = scrape_books()
    save_csv(books)
    print(f"Scraped {len(books)} books. Saved to {CSV_FILE}")
