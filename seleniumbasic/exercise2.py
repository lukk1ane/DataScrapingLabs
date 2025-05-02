from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1024,768")
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
driver.get("https://books.toscrape.com/")

books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

all_books = []
five_star_books = []

for book in books:
    title = book.find_element(By.TAG_NAME, "h3").text
    price = book.find_element(By.CSS_SELECTOR, ".price_color").text
    availability = book.find_element(By.CSS_SELECTOR, ".instock").text.strip()
    star = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]
    
    all_books.append([title, price, star, availability])
    if star == "Five":
        five_star_books.append([title, price, star, availability])

with open("all_books.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Star", "Availability"])
    writer.writerows(all_books)

with open("5_star_books.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Star", "Availability"])
    writer.writerows(five_star_books)

driver.quit()
