from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
OUTPUT_DIR = os.path.join(os.getcwd(), "swoop_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)
BASE_URL = "https://swoop.ge/"

def setup_driver():
    options = Options()
    options.add_argument("--window-size=1200x800")
    options.add_argument("--start-maximized")

    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


def login(driver):
    print("\nLogin")
    driver.get(BASE_URL)

    try:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ვეთანხმები')]"))
            ).click()
            print("Cookie consent clicked.")
        except:
            print("Cookie consent not found or not clickable.")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-secondary_gray_10')]"))
        )
        login_button.click()
        print("'შესვლა' button clicked.")
    except Exception as e:
        print(f"Login error: {e}")


def scrape_product_data(driver):
    print("\nScrape Product Data")
    driver.get(BASE_URL)

    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
        )

        for product in products[:5]:
            try:
                title = product.find_element(By.CLASS_NAME, "title").text.strip()
                price = product.find_element(By.CLASS_NAME, "price").text.strip()
                print(f"Product: {title} | Price: {price}")
            except Exception as e:
                print(f"Error extracting product info: {e}")

    except Exception as e:
        print(f"Error scraping product data: {e}")


def apply_category_filter(driver):
    print("\nApply Category Filter")
    driver.get(BASE_URL)

    try:
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'კინო')]"))
        )
        filter_button.click()
        print("Category filter applied.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
        )
        print("Products reloaded.")

    except Exception as e:
        print(f"Error applying category filter: {e}")


def check_images_loaded(driver):
    print("\nCheck Images and Save Screenshots")
    driver.get(BASE_URL)

    try:
        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img"))
        )

        for idx, img in enumerate(images[:5]):
            try:
                is_loaded = driver.execute_script(
                    "return arguments[0].complete && arguments[0].naturalHeight !== 0", img
                )
                print(f"Image {idx + 1} loaded: {is_loaded}")

                if is_loaded:
                    img.screenshot(os.path.join(OUTPUT_DIR, f"image_{idx + 1}.png"))
                    print(f"Screenshot saved: image_{idx + 1}.png")

            except Exception as e:
                print(f" Error checking image {idx + 1}: {e}")

    except Exception as e:
        print(f"Error in image check: {e}")


def main():
    driver = setup_driver()
    if not driver:
        print("WebDriver setup failed.")
        return

    try:
        login(driver)
        scrape_product_data(driver)
        apply_category_filter(driver)
        check_images_loaded(driver)
    finally:
        print("\nAll tasks completed.")
        driver.quit()


if __name__ == "__main__":
    main()
