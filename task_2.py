from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://swoop.ge/category/110/sporti")
wait = WebDriverWait(driver, 10)

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4[type='h4']")))

titles, prices, discount_prices, discounts = [], [], [], []


def scrape_current_page():
    page_cards = driver.find_elements(By.CSS_SELECTOR, "a.group.flex.flex-col.gap-3.cursor-pointer")
    count = 0
    for card in page_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h4[type='h4']").text
            original_price = card.find_element(By.CSS_SELECTOR, "h4.line-through").text.replace("₾", "")
            discounted_price = card.find_element(By.CSS_SELECTOR, "h4[weight='bold']").text.replace("₾", "")
            discount_percentage = card.find_element(By.CSS_SELECTOR, "p[weight='bold']").text

            titles.append(title)
            prices.append(original_price)
            discount_prices.append(discounted_price)
            discounts.append(discount_percentage)
            count += 1
        except:
            continue
    return count


page_num = 1

while page_num <= 10:  # Limit to 10 pages as safety
    items_on_page = scrape_current_page()
    print(f"Page {page_num}: Scraped {items_on_page} items")

    try:
        next_button = driver.find_element(By.XPATH,
                                          "//div[contains(@class, 'flex') and .//img[contains(@src, '/icons/ep_arrow-right-bold.svg')]]")

        if "disabled" in next_button.get_attribute("class"):
            print("Reached last page")
            break

        # Scroll to make button visible
        time.sleep(1)

        # Click the button
        next_button.click()

        # Wait for content to update
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4[type='h4']")))

        page_num += 1

    except Exception as e:
        print(f"Pagination error: {e}")
        break

data = {
    "Title": titles,
    "Original Price": prices,
    "Discounted Price": discount_prices,
    "Discount": discounts
}

df = pd.DataFrame(data)
print(f"Total: {len(df)} items from {page_num} pages")
df.to_csv("swoop_offers.csv", index=False, encoding="utf-8")

driver.quit()