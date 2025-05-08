from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re


def scrape_swoop_food_section(driver):
    try:
        print("Opening swoop.ge...")
        driver.get("https://swoop.ge/")
        print("Looking for 'კვება' link...")
        nutrition_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "კვება"))
        )

        print("Found 'კვება' link, clicking...")
        nutrition_link.click()

        print("Waiting for page to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "grid"))
        )

        time.sleep(3)

        all_titles = []
        all_prices = []
        all_discounts = []
        all_sold_counts = []

        print("Finding all 'relative' elements...")
        relative_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'relative')]")

        print(f"Found {len(relative_elements)} 'relative' elements.")

        valid_count = 0

        for index, element in enumerate(relative_elements):
            try:
                text_content = element.text.strip()

                if not text_content or text_content == "..." or len(text_content) < 10:
                    continue

                if "₾" not in text_content:
                    continue

                valid_count += 1

                price_match = re.search(r'\d+\.\d+₾', text_content)
                price = price_match.group(0) if price_match else "Unknown"

                discount_match = re.search(r'-\d+%', text_content)
                discount = discount_match.group(0) if discount_match else ""

                sold_match = re.search(r'გაყიდულია\s+(\d+)', text_content)
                sold_count = sold_match.group(1) if sold_match else "0"

                title = text_content
                if price_match:
                    title = title.replace(price, "")
                if discount_match:
                    title = title.replace(discount, "")
                if sold_match:
                    title = title.replace(sold_match.group(0), "")

                title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with a single space
                title = title.replace(" - ", "")  # Remove " - " that might remain
                title = title.strip()

                all_titles.append(title)
                all_prices.append(price)
                all_discounts.append(discount)
                all_sold_counts.append(sold_count)

                print(f"Processed item {valid_count}: {title} - {price} {discount} (Sold: {sold_count})")

            except Exception as e:
                print(f"Error processing element {index + 1}: {e}")

        df = pd.DataFrame({
            "Title": all_titles,
            "Price": all_prices,
            "Discount": all_discounts,
            "Sold Count": all_sold_counts
        })

        csv_filename = 'swoop_items.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    firefox_options = Options()

    driver = webdriver.Firefox(options=firefox_options)
    scrape_swoop_food_section(driver)