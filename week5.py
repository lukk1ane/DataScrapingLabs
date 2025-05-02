from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import time


def task1_form_automation():
    """Automate form submission on demoqa.com"""
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("https://demoqa.com/automation-practice-form")

        # Fill form fields
        driver.find_element(By.ID, "firstName").send_keys("John")
        driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys("Doe")
        driver.find_element(By.XPATH, "//input[@id='userEmail']").send_keys("john.doe@example.com")
        driver.find_element(By.XPATH, "//label[contains(text(),'Male')]").click()
        driver.find_element(By.CSS_SELECTOR, "input[placeholder='Mobile Number']").send_keys("1234567890")

        # Date of Birth
        driver.find_element(By.ID, "dateOfBirthInput").click()
        driver.find_element(By.CLASS_NAME, "react-datepicker__month-select").send_keys("May")
        driver.find_element(By.CLASS_NAME, "react-datepicker__year-select").send_keys("1990")
        driver.find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day') and text()='15']").click()

        # Continue with other fields
        driver.find_element(By.ID, "subjectsInput").send_keys("Maths" + Keys.RETURN)
        driver.find_element(By.XPATH, "//label[contains(text(),'Sports')]").click()
        driver.find_element(By.ID, "uploadPicture").send_keys("/path/to/your/file.txt")
        driver.find_element(By.CSS_SELECTOR, "textarea#currentAddress").send_keys("123 Main St, City, Country")

        # State and City
        driver.find_element(By.ID, "state").click()
        driver.find_element(By.XPATH, "//div[text()='NCR']").click()
        driver.find_element(By.ID, "city").click()
        driver.find_element(By.XPATH, "//div[text()='Delhi']").click()

        # Submit
        driver.find_element(By.ID, "submit").click()

        # Verify submission
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
            )
            print("Form submitted successfully!")
        except:
            print("Form submission may not have been successful.")

        time.sleep(2)

    finally:
        driver.quit()


def task2_book_scraping():
    """Scrape book information from books.toscrape.com"""
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.get("https://books.toscrape.com/")
        time.sleep(2)

        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        with open('all_books.csv', 'w', newline='', encoding='utf-8') as all_books_file, \
                open('5_star_books.csv', 'w', newline='', encoding='utf-8') as five_star_file:

            all_writer = csv.writer(all_books_file)
            five_star_writer = csv.writer(five_star_file)

            all_writer.writerow(['Title', 'Price', 'Rating', 'Availability'])
            five_star_writer.writerow(['Title', 'Price', 'Rating', 'Availability'])

            for book in books:
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                price = book.find_element(By.CSS_SELECTOR, "div.product_price p.price_color").text
                rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]
                availability = book.find_element(By.CSS_SELECTOR, "div.product_price p.instock").text

                all_writer.writerow([title, price, rating, availability])
                if rating == "Five":
                    five_star_writer.writerow([title, price, rating, availability])

        print("Book scraping complete. Check the CSV files.")

    finally:
        driver.quit()


def run_headless_example():
    """Example of running in headless mode with custom window size"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1200, 800)

    try:
        driver.get("https://books.toscrape.com/")
        print("Page title in headless mode:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    print("Running Task 1: Form Automation")
    task1_form_automation()

    print("\nRunning Task 2: Book Scraping")
    task2_book_scraping()
