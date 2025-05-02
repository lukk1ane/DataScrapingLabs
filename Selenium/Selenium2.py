import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

URL = "https://books.toscrape.com/"
ALL_BOOKS_FILE = "all-books.csv"
FIVE_STAR_FILE = "5-star-books.csv"

options = Options()

options.headless = False

driver = webdriver.Firefox(options=options)
driver.maximize_window()

driver.get(URL)

books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

all_books = []
five_star_books = []

for book in books:
    title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
    price = book.find_element(By.CSS_SELECTOR, ".price_color").text
    availability = book.find_element(By.CSS_SELECTOR, ".availability").text.strip()

    star_element = book.find_element(By.CSS_SELECTOR, "p.star-rating")
    star_classes = star_element.get_attribute("class").split()
    star_rating = star_classes[1]

    book_data = {
        "Title": title,
        "Price": price,
        "Star Rating": star_rating,
        "Availability": availability
    }
    all_books.append(book_data)

    if star_rating == "Five":
        five_star_books.append(book_data)

driver.quit()


def write_csv(file_name, data):
    with open(file_name, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Star Rating", "Availability"])
        writer.writeheader()
        writer.writerows(data)


write_csv(ALL_BOOKS_FILE, all_books)
write_csv(FIVE_STAR_FILE, five_star_books)

print(f"Saved {len(all_books)} books to {ALL_BOOKS_FILE}")
print(f"Saved {len(five_star_books)} 5-star books to {FIVE_STAR_FILE}")