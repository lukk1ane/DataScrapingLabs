from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import os
import logging
from selenium.webdriver.chrome.options import Options

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_books(mode="normal", width=None, height=None):
    # Set up Chrome options
    chrome_options = Options()
    
    if mode == "headless":
        chrome_options.add_argument("--headless")
    if mode == "custom" and width and height:
        chrome_options.add_argument(f"--window-size={width},{height}")
    if mode == "normal":
        chrome_options.add_argument("--start-maximized")
    
    # Initialize the WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        logger.info(f"Starting browser in {mode} mode")
        # Navigate to the books website
        driver.get("https://books.toscrape.com/")
        
        # Wait for the page to load
        time.sleep(2)
        logger.info("Page loaded, extracting book details")
        
        # Extract book details using CSS selectors
        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        all_books_data = []
        five_star_books = []
        
        for book in books:
            title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
            rating_element = book.find_element(By.CSS_SELECTOR, "p.star-rating")
            rating = rating_element.get_attribute("class").split()[-1]
            availability = book.find_element(By.CSS_SELECTOR, "p.availability").text.strip()
            
            book_data = {
                "Title": title,
                "Price": price,
                "Star Rating": rating,
                "Availability": availability
            }
            all_books_data.append(book_data)
            
            # Check for 5-star rating
            if rating == "Five":
                five_star_books.append(book_data)
        
        # Ensure LAB5 directory exists
        os.makedirs("LAB5", exist_ok=True)
        
        # Write all books to CSV
        logger.info("Writing all books to CSV")
        with open("LAB5/all_books.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Title", "Price", "Star Rating", "Availability"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in all_books_data:
                writer.writerow(book)
        logger.info("All books data saved to CSV")
        
        # Write 5-star books to a separate CSV
        logger.info("Writing 5-star books to CSV")
        with open("LAB5/5_star_books.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Title", "Price", "Star Rating", "Availability"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in five_star_books:
                writer.writerow(book)
        logger.info("5-star books data saved to CSV")
        
        logger.info(f"Scraped {len(all_books_data)} books. {len(five_star_books)} are 5-star rated.")
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Run in normal maximized mode
    logger.info("Running in normal mode (maximized)...")
    scrape_books(mode="normal")
    
    # Run in custom window size
    logger.info("Running in custom window size mode...")
    scrape_books(mode="custom", width=800, height=600)
    
    # Run in headless mode
    logger.info("Running in headless mode...")
    scrape_books(mode="headless")