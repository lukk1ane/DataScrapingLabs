from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time


def scrape_books():
    # Initialize Chrome options
    chrome_options = Options()

    # Run in different modes (comment/uncomment as needed)
    # chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--window-size=1024,768")  # Custom window size

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # Maximize window (overrides custom size if set)

    try:
        # Navigate to the books website
        driver.get("https://books.toscrape.com/")
        time.sleep(2)  # Wait for page to load

        # Find all book elements
        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        # Prepare CSV files
        with open('all_books.csv', 'w', newline='', encoding='utf-8') as all_books_file, \
                open('5_star_books.csv', 'w', newline='', encoding='utf-8') as five_star_file:

            all_writer = csv.writer(all_books_file)
            five_star_writer = csv.writer(five_star_file)

            # Write headers
            all_writer.writerow(['Title', 'Price', 'Rating', 'Availability'])
            five_star_writer.writerow(['Title', 'Price', 'Rating', 'Availability'])

            for book in books:
                # Extract book details
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                price = book.find_element(By.CSS_SELECTOR, "p.price_color").text

                # Rating is in the class name (e.g., "star-rating Five")
                rating_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
                rating = rating_class.split()[-1]  # Get the last word (One, Two, etc.)

                # Availability might not be visible on first page, but we can try
                availability = "Available"
                try:
                    availability = book.find_element(By.CSS_SELECTOR, "p.availability").text.strip()
                except:
                    pass

                # Write to all books file
                all_writer.writerow([title, price, rating, availability])

                # Write to 5-star books file if applicable
                if rating == "Five":
                    five_star_writer.writerow([title, price, rating, availability])

        print("Scraping completed. Data saved to all_books.csv and 5_star_books.csv")

    finally:
        driver.quit()


# Run the function
scrape_books()