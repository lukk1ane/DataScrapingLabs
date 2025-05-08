from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

if not os.path.exists("image_screenshots"):
    os.makedirs("image_screenshots")

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get("https://swoop.ge")

    wait = WebDriverWait(driver, 10)
    product_images = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "a.group.flex.flex-col.gap-3.cursor-pointer img")
    ))

    for index, img in enumerate(product_images[:5]):
        driver.execute_script("arguments[0].scrollIntoView(true);", img)
        time.sleep(0.5)  # Small delay to ensure image is in view

        is_loaded = driver.execute_script("""
            return arguments[0].complete && 
                   typeof arguments[0].naturalWidth != 'undefined' && 
                   arguments[0].naturalWidth > 0;
        """, img)

        img_src = img.get_attribute("src")
        img_alt = img.get_attribute("alt")

        if is_loaded:
            try:
                img.screenshot(f"image_screenshots/image_{index + 1}.png")
            except Exception as e:
                print(f"  Error saving screenshot: {e}")

finally:
    # Close the browser
    driver.quit()
