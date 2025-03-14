import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_books_data(max_pages=3):
    base_url = "http://books.toscrape.com/catalogue/"
    current_page = "page-1.html"

    with open('books_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Define CSV headers
        fieldnames = ['Title', 'Price', 'Rating', 'Availability', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        page_num = 1
        while page_num <= max_pages:
            page_url = base_url + current_page
            print(f"Scraping page {page_num}: {page_url}")

            response = requests.get(page_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                books = soup.find_all('article', class_='product_pod')

                for book in books:
                    title = book.h3.a['title']
                    price = book.find('p', class_='price_color').text.strip()

                    rating_class = book.find('p', class_='star-rating')['class'][1].lower()
                    rating_mapping = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'}
                    rating = rating_mapping.get(rating_class, 'Unknown')

                    availability = book.find('p', class_='availability').text.strip()

                    category = "TBD"

                    writer.writerow({
                        'Title': title,
                        'Price': price,
                        'Rating': rating,
                        'Availability': availability,
                        'Category': category
                    })

                next_button = soup.select_one('li.next > a')
                if next_button and page_num < max_pages:
                    current_page = next_button['href']
                    page_num += 1
                    time.sleep(1)
                else:
                    break
            else:
                print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")
                break

    print(f"Scraping completed! Data saved to books_data.csv")


if __name__ == "__main__":
    scrape_books_data()