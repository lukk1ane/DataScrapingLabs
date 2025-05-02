import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

driver_path = "/Users/atukaberadze/Desktop/chromedriver-mac-arm64/chromedriver"
os.chmod(driver_path, 0o755)

options = Options()
options.add_argument("--window-size=1024,768")
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(driver_path), options=options)
driver.get("https://books.toscrape.com/")

books = driver.find_elements(By.CLASS_NAME, "product_pod")

all_books = []
five_star_books = []

for book in books:
    title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
    price = book.find_element(By.CLASS_NAME, "price_color").text
    availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
    star_rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]

    book_data = {
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Rating": star_rating
    }

    all_books.append(book_data)
    if star_rating == "Five":
        five_star_books.append(book_data)

driver.quit()

with open("all_books.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Availability", "Rating"])
    writer.writeheader()
    writer.writerows(all_books)

with open("5_star_books.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Availability", "Rating"])
    writer.writeheader()
    writer.writerows(five_star_books)
