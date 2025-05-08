from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import time
from urllib.parse import urljoin

SWOOP_URL = "https://swoop.ge/"
TIMEOUT = 15
SCREENSHOT_DIR = "swoop_images"


def check_swoop_images(driver):
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    try:
        print(f"Opening {SWOOP_URL}...")
        driver.get(SWOOP_URL)

        print(f"Waiting for product images to load (timeout: {TIMEOUT} seconds)...")
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'w-full')]"))
        )

        time.sleep(2)

        all_images = driver.find_elements(By.XPATH, "//img[contains(@class, 'w-full')]")
        print(f"Found {len(all_images)} product images")

        for i, img in enumerate(all_images[:5]):
            try:
                is_loaded = driver.execute_script(
                    "return arguments[0].complete && "
                    "typeof arguments[0].naturalWidth != 'undefined' && "
                    "arguments[0].naturalWidth > 0", img)

                print(f"Image {i + 1}: {'Loaded successfully' if is_loaded else 'Failed to load'}")

                if is_loaded:
                    img_src = img.get_attribute('src')

                    if img_src:
                        try:
                            if not img_src.startswith(('http://', 'https://')):
                                img_src = urljoin("https://swoop.ge/", img_src)

                            print(f"Downloading image from: {img_src}")

                            response = requests.get(img_src, timeout=10)

                            if response.status_code == 200:
                                filepath = os.path.join(SCREENSHOT_DIR, f"swoop_image_{i + 1}.png")
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                                print(f"Image downloaded and saved to {filepath}")
                            else:
                                raise Exception(f"Failed to download image: HTTP {response.status_code}")

                        except Exception as download_error:
                            print(f"Error downloading image {i + 1}: {download_error}")
                            print("Falling back to screenshot method...")

                            driver.execute_script("arguments[0].scrollIntoView(true);", img)
                            time.sleep(0.5)

                            filepath = os.path.join(SCREENSHOT_DIR, f"swoop_image_{i + 1}.png")
                            img.screenshot(filepath)
                            print(f"Fallback screenshot saved to {filepath}")
                    else:
                        print(f"No src attribute found for image {i + 1}")
                        filepath = os.path.join(SCREENSHOT_DIR, f"swoop_image_{i + 1}.png")
                        img.screenshot(filepath)
                        print(f"Fallback screenshot saved to {filepath}")

            except Exception as e:
                print(f"Error checking image {i + 1}: {e}")

        print("Image checking complete!")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    firefox_options = Options()

    driver = webdriver.Firefox(options=firefox_options)
    check_swoop_images(driver)