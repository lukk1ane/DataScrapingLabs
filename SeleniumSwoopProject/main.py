
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login(driver):
    driver.get("https://swoop.ge")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "შესვლა"))
        )
        login_button.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpass")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    except Exception as e:
        print(f"Login error: {e}")

def scrape_data(driver):
    driver.get("https://swoop.ge")
    time.sleep(2)
    products = driver.find_elements(By.CLASS_NAME, "product-title")
    for product in products[:5]:
        print(product.text)

def apply_filter(driver):
    driver.get("https://swoop.ge")
    try:
        sidebar_filter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='sidebar-category']//a"))
        )
        sidebar_filter.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-item"))
        )
        print("Filter applied successfully")
    except Exception as e:
        print(f"Filter error: {e}")

def check_images(driver):
    driver.get("https://swoop.ge")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img"))
        )
        images = driver.find_elements(By.XPATH, "//img")[:5]
        for idx, img in enumerate(images):
            is_loaded = driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0", img
            )
            if is_loaded:
                print(f"Image {idx + 1} is fully loaded")
                img.screenshot(f"image_{idx + 1}.png")
            else:
                print(f"Image {idx + 1} is not fully loaded")
    except Exception as e:
        print(f"Image check error: {e}")

def handle_pagination(driver):
    driver.get("https://swoop.ge")
    try:
        while True:
            products = driver.find_elements(By.CLASS_NAME, "product-title")
            for product in products:
                print(product.text)
            next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
            if next_button:
                next_button.click()
                time.sleep(2)
            else:
                break
    except Exception as e:
        print(f"Pagination error: {e}")

def main():
    driver = setup_driver()
    login(driver)
    scrape_data(driver)
    apply_filter(driver)
    check_images(driver)
    handle_pagination(driver)
    driver.quit()

if __name__ == "__main__":
    main()
