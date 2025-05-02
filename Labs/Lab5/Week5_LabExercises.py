from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
import os


# Task 1
def fill_demoqa_form(driver):
    driver.get("https://demoqa.com/automation-practice-form")
    driver.maximize_window()

    driver.find_element(By.ID, "firstName").send_keys("Ana")
    driver.find_element(By.ID, "lastName").send_keys("Abashidze")
    driver.find_element(By.ID, "userEmail").send_keys("ana@example.com")

    gender_radio = driver.find_element(By.XPATH, "//label[text()='Female']")
    driver.execute_script("arguments[0].scrollIntoView();", gender_radio)
    driver.execute_script("arguments[0].click();", gender_radio)

    driver.find_element(By.ID, "userNumber").send_keys("5551234567")

    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    time.sleep(2)


# Task 2
def scrape_books_toscrape(driver):
    driver.get("http://books.toscrape.com/")
    driver.maximize_window()

    books = []
    book_cards = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

    for book in book_cards:
        title = book.find_element(By.TAG_NAME, "h3").text
        price = book.find_element(By.CLASS_NAME, "price_color").text.replace("£", "")
        availability = book.find_element(By.CLASS_NAME, "instock").text.strip()
        rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        })

    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    five_star_books = [book for book in books if book["rating"] == "Five"]
    with open("5_star_books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(five_star_books)

    print(f"✔ Total books scraped: {len(books)}")
    print(f"✔ 5-star books saved: {len(five_star_books)}")


if __name__ == "__main__":
    options = Options()
    options.add_argument("window-size=1200x800")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    print("\nRunning Task 1: Fill DemoQA Form...")
    fill_demoqa_form(driver)

    print("\nRunning Task 2: Scrape Books and Save CSVs...")
    scrape_books_toscrape(driver)

    driver.quit()

    print("\nOutput Files:")
    print("books.csv:", "Exists" if os.path.exists("books.csv") else "Missing")
    print("5_star_books.csv:", "Exists" if os.path.exists("5_star_books.csv") else "Missing")
