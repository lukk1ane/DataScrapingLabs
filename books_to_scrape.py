from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time


def setup_driver(headless=False, window_size=None):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()

    if window_size:
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    return driver


def get_star_rating(element):
    star_class = element.find_element(By.CLASS_NAME, "star-rating").get_attribute("class")
    rating_text = star_class.split()[-1]

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    return ratings.get(rating_text, 0)


def scrape_books():
    driver = setup_driver(headless=False)

    try:
        driver.get("https://books.toscrape.com/")
        time.sleep(2)

        book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        all_books = []
        five_star_books = []

        for book in book_elements:
            title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            price = book.find_element(By.CSS_SELECTOR, ".price_color").text
            star_rating = get_star_rating(book)
            availability = "In stock" if "instock" in book.find_element(By.CSS_SELECTOR, ".availability").get_attribute(
                "class") else "Out of stock"

            book_data = {
                "Title": title,
                "Price": price,
                "Star Rating": star_rating,
                "Availability": availability
            }

            all_books.append(book_data)

            if star_rating == 5:
                five_star_books.append(book_data)

        with open("all_books.csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = ["Title", "Price", "Star Rating", "Availability"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in all_books:
                writer.writerow(book)

        with open("5_star_books.csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = ["Title", "Price", "Star Rating", "Availability"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for book in five_star_books:
                writer.writerow(book)

        print(f"Scraped {len(all_books)} books. Found {len(five_star_books)} 5-star books.")

    finally:
        driver.quit()

    print("\nRunning in headless mode with custom window size (1024x768)...")
    headless_driver = setup_driver(headless=True, window_size=(1024, 768))

    try:
        headless_driver.get("https://books.toscrape.com/")
        time.sleep(2)

        book_count = len(headless_driver.find_elements(By.CSS_SELECTOR, "article.product_pod"))
        print(f"Found {book_count} books in headless mode.")

    finally:
        headless_driver.quit()


if __name__ == "__main__":
    scrape_books()