import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)

SWOOP_URL = "https://swoop.ge/"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

DUMMY_USERNAME = "testuser@example.com"
DUMMY_PASSWORD = "TestPassword123!"

SCREENSHOTS_DIR = "swoop_screenshots"
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)


def initialize_driver():
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("Using ChromeDriver from system PATH.")
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None
    return driver

def handle_cookie_banner(driver, wait_time=5):
    try:
        cookie_accept_button_xpath = "//div[contains(@class, 'fixed bottom-20')]//button[.//p[contains(text(),'ვეთანხმები')]]"
        cookie_accept_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, cookie_accept_button_xpath))
        )
        driver.execute_script("arguments[0].click();", cookie_accept_button)
        print("Accepted cookie consent via JavaScript click.")
        time.sleep(0.5)
    except TimeoutException:
        print("Cookie consent banner not found or timed out.")
    except Exception as e:
        print(f"Error handling cookie banner: {e}")

def task_1_login(driver, username, password):
    print("\n--- Task 1: Login Attempt ---")
    driver.get(SWOOP_URL)
    wait = WebDriverWait(driver, 20)
    handle_cookie_banner(driver)

    try:
        login_button_xpath = "//button[.//img[@alt='profile.svg'] and .//p[text()='შესვლა']]"
        print(f"Attempting to click login button with XPath: {login_button_xpath}")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", login_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", login_button)
        print("Clicked on the 'შესვლა' button.")

        email_field_id = "Email"; password_field_id = "Password"

        print(f"Waiting for email field with ID: {email_field_id}")
        email_field = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.ID, email_field_id)))
        print(f"Waiting for password field with ID: {password_field_id}")
        password_field = wait.until(EC.visibility_of_element_located((By.ID, password_field_id)))

        email_field.send_keys(username); password_field.send_keys(password)
        print(f"Entered Username: {username}"); print("Entered Password.")

        print("Login form fields filled (simulated). Navigating back to homepage.")
        driver.get(SWOOP_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    except TimeoutException:
        print("Timeout: Could not find login elements or form fields (Email/Password IDs might be incorrect on login page).")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task1_timeout_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
    except Exception as e:
        print(f"An error occurred during login: {e}")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task1_exception_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

def task_2_navigate_and_scrape(driver):
    print("\n--- Task 2: Navigate and Scrape ---")
    wait = WebDriverWait(driver, 20)
    driver.get(SWOOP_URL)
    handle_cookie_banner(driver)

    try:
        target_category_text = "დასვენება"
        dasveneba_link_xpath = f"//a[.//p[text()='{target_category_text}']]"
        print(f"Attempting to find category: '{target_category_text}' with XPath: {dasveneba_link_xpath}")
        dasveneba_link = wait.until(EC.element_to_be_clickable((By.XPATH, dasveneba_link_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest', inline: 'center'});", dasveneba_link)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", dasveneba_link)
        print(f"Navigated to '{target_category_text}' category.")
        wait.until(EC.url_contains("category/24/dasveneba"))

        item_card_xpath = "//a[contains(@class, 'group') and @href[contains(., '/offers/')]]"
        print(f"Waiting for item cards with XPath: {item_card_xpath}")
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, item_card_xpath)))
        print("Product listings loaded on category page.")

        item_cards = driver.find_elements(By.XPATH, item_card_xpath)
        print(f"Found {len(item_cards)} item cards. Scraping first few...")

        for i, card in enumerate(item_cards[:5]):
            title = "N/A"; price = "N/A"; href = "N/A"
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of(card))
                href = card.get_attribute('href')
                inner_html = card.get_attribute('innerHTML')

                title_match = re.search(r'<h4.*?class="[^"]*line-clamp-2[^"]*".*?>(.*?)</h4>', inner_html, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    print(f"  Item {i+1}: Could not parse title from InnerHTML.")

                price_match = re.search(r'<h4.*?class="[^"]*font-tbcx-bold[^"]*".*?>(.*?₾.*?)</h4>', inner_html, re.IGNORECASE | re.DOTALL)
                if price_match:
                    price_text = re.sub('<[^>]*>', '', price_match.group(1)).strip()
                    price = price_text
                else:
                    print(f"  Item {i+1}: Could not parse price from InnerHTML.")

                print(f"  Item {i+1}: Title: {title}, Price: {price}")

            except StaleElementReferenceException:
                print(f"  Item {i+1}: Card element became stale. Skipping.")
                continue
            except TimeoutException:
                 print(f"  Item {i+1}: Timed out waiting for card visibility.")
                 print(f"    Item href: {href}")
            except Exception as e:
                print(f"  Item {i+1}: Error processing card details: {e}")
                print(f"    Item href: {href}")

    except TimeoutException:
        print("Timeout: Could not navigate or find item cards for scraping in Task 2.")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task2_timeout_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
    except Exception as e:
        print(f"An error occurred during navigation and scraping in Task 2: {e}")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task2_exception_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

def task_3_apply_filter(driver):
    print("\n--- Task 3: Apply Category Filter ---")
    if "category" not in driver.current_url:
        print("Not on a category page. Navigating to 'დასვენება' for filter demo.")
        try:
            driver.get(SWOOP_URL)
            handle_cookie_banner(driver)
            target_category_text = "დასვენება"
            dasveneba_link_xpath = f"//a[.//p[text()='{target_category_text}']]"
            dasveneba_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, dasveneba_link_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest', inline: 'center'});", dasveneba_link)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", dasveneba_link)
            WebDriverWait(driver, 15).until(EC.url_contains("category"))
            print("Navigated to 'დასვენება' for filter task.")
        except Exception as e:
            print(f"Could not navigate to category for filter task: {e}. Skipping Task 3.")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, "task3_nav_failure.png"); driver.save_screenshot(screenshot_path)
            return

    wait = WebDriverWait(driver, 20)
    item_xpath_selector = "//a[contains(@class, 'group') and @href[contains(., '/offers/')]]"

    try:
        filter_label_text = "დიღომი"
        print(f"Looking for filter: '{filter_label_text}'")

        filter_xpath = f"//form[contains(@class, 'col-span-3')]//span[normalize-space()='{filter_label_text}']"
        filter_sidebar_xpath = "//form[contains(@class, 'col-span-3')]"
        wait.until(EC.visibility_of_element_located((By.XPATH, filter_sidebar_xpath)))

        filter_element = wait.until(EC.element_to_be_clickable((By.XPATH, filter_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_element)
        time.sleep(0.5)

        initial_items = driver.find_elements(By.XPATH, item_xpath_selector)
        initial_item_count = len(initial_items)
        first_item_href_before = initial_items[0].get_attribute("href") if initial_item_count > 0 else None
        print(f"Initial items before filter: {initial_item_count}. First item href: {first_item_href_before}")

        driver.execute_script("arguments[0].click();", filter_element)
        print(f"Clicked on filter element for: '{filter_label_text}'")

        print("Waiting for filter results to potentially update...")
        try:
            if first_item_href_before:
                WebDriverWait(driver, 15).until(
                    lambda d: (
                        len(d.find_elements(By.XPATH, item_xpath_selector)) == 0 or
                        (len(d.find_elements(By.XPATH, item_xpath_selector)) > 0 and \
                         d.find_elements(By.XPATH, item_xpath_selector)[0].get_attribute("href") != first_item_href_before)
                    )
                )
                print("Detected change in first item or list potentially became empty.")
            else:
                 WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, item_xpath_selector)))
                 print("Items appeared after filtering (list was initially empty).")
        except TimeoutException:
            print("First item did not change/disappear or list didn't populate within timeout. Proceeding.")
        except StaleElementReferenceException:
            print("Initial first item became stale quickly, indicating a list refresh happened.")

        time.sleep(1)

        print("Attempting to scrape items after filter...")
        try:
             filtered_items_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, item_xpath_selector)))
             print(f"Filter potentially applied. New item count: {len(filtered_items_elements)}")
        except TimeoutException:
            print("No items found after filtering.")
            filtered_items_elements = []


        if not filtered_items_elements:
            print("No items found after applying the filter.")
        else:
            print("Scraping items after filter:")
            items_to_scrape = filtered_items_elements[:3]

            for i, card_element in enumerate(items_to_scrape):
                title = "N/A"; price = "N/A"; href="N/A"
                try:
                    if not card_element.is_displayed():
                        print(f"  Filtered Item {i+1}: Element found but not displayed. Skipping.")
                        continue
                    href = card_element.get_attribute('href')

                    inner_html = card_element.get_attribute('innerHTML')
                    title_match = re.search(r'<h4.*?class="[^"]*line-clamp-2[^"]*".*?>(.*?)</h4>', inner_html, re.IGNORECASE | re.DOTALL)
                    price_match = re.search(r'<h4.*?class="[^"]*font-tbcx-bold[^"]*".*?>(.*?₾.*?)</h4>', inner_html, re.IGNORECASE | re.DOTALL)

                    if title_match: title = title_match.group(1).strip()
                    if price_match: price = re.sub('<[^>]*>', '', price_match.group(1)).strip()

                    print(f"  Filtered Item {i+1}: Title: {title}, Price: {price}")

                except StaleElementReferenceException:
                    print(f"  Filtered Item {i+1}: Element became stale during scraping. Skipping.")
                    continue
                except Exception as e:
                    print(f"  Filtered Item {i+1}: Error scraping details - {e}")
                    print(f"    Item href: {href}")

    except TimeoutException:
        print(f"Timeout: Could not find or apply filter '{filter_label_text}'. Selector XPath might be incorrect: {filter_xpath}")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task3_timeout_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
    except Exception as e:
        print(f"An error occurred while applying filter: {e}")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task3_exception_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

def task_4_check_images_and_screenshot(driver):
    print("\n--- Task 4: Check Homepage Images and Screenshot ---")
    driver.get(SWOOP_URL)
    wait = WebDriverWait(driver, 20)
    handle_cookie_banner(driver)

    try:
        image_xpath_selector = "//div[contains(@class,'swiper-slide')]//a[contains(@href, '/offers/')]/div[contains(@class,'relative')]//img"
        print(f"Waiting for images matching XPath: '{image_xpath_selector}'")
        wait.until(EC.visibility_of_element_located((By.XPATH, image_xpath_selector)))
        product_images = driver.find_elements(By.XPATH, image_xpath_selector)

        if not product_images:
            print("No product images found on the homepage with the specified XPath.")
            return

        print(f"Found {len(product_images)} potential product images. Checking first 5.")

        for i, img_element in enumerate(product_images[:5]):
            is_loaded = False; img_src = None; img_alt = None
            try:
                img_src = img_element.get_attribute('src')
                img_alt = img_element.get_attribute('alt')
                print(f"\nImage {i+1}: src: {img_src if img_src else 'N/A'}, alt: {img_alt if img_alt else 'N/A'}")

                if not img_src:
                    print(f"  Image {i+1}: No src attribute found. Skipping.")
                    continue

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img_element); time.sleep(0.5)

                is_loaded = driver.execute_script(
                    "return arguments[0].complete && typeof arguments[0].naturalWidth !== 'undefined' && arguments[0].naturalWidth > 0;",
                    img_element )

            except StaleElementReferenceException:
                 print(f"  Image {i+1}: Element became stale before processing.")
                 continue
            except Exception as e:
                 print(f"  Image {i+1}: Error checking/processing image: {e}")
                 continue

            if is_loaded:
                print(f"  Image {i+1}: Is fully loaded (checked via JavaScript).")
                try:
                    wait.until(EC.visibility_of(img_element))
                    filename_base = os.path.basename(img_src.split('?')[0]) if img_src else f"image_{i+1}"
                    sanitized_base = "".join([c if c.isalnum() or c in ('.', '_', '-') else '_' for c in filename_base])
                    base, ext = os.path.splitext(sanitized_base)
                    if not ext.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp'): ext = ".png"
                    final_filename = f"{base[:50]}{ext}"

                    filepath = os.path.join(SCREENSHOTS_DIR, f"swoop_image_{i+1}_{final_filename}")
                    img_element.screenshot(filepath)
                    print(f"  Screenshot saved to: {filepath}")
                except Exception as e:
                    print(f"  Image {i+1}: Could not save screenshot. Error: {e}")
            else:
                print(f"  Image {i+1}: Is NOT fully loaded or not visible (checked via JavaScript).")

    except TimeoutException:
        print("Timeout: Could not find product images on the homepage for Task 4.")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task4_timeout_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
    except Exception as e:
        print(f"An error occurred during image checking in Task 4: {e}")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "task4_exception_failure.png"); driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

def bonus_handle_pagination(driver):
    print("\n--- Bonus: Handle Pagination Dynamically ---")
    print("Navigating to 'დასვენება' for pagination demo.")
    driver.get(SWOOP_URL)
    handle_cookie_banner(driver)
    wait = WebDriverWait(driver, 20)
    try:
        target_category_text = "დასვენება"
        dasveneba_link_xpath = f"//a[.//p[text()='{target_category_text}']]"
        dasveneba_link = wait.until(EC.element_to_be_clickable((By.XPATH, dasveneba_link_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'nearest', inline: 'center'});", dasveneba_link)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", dasveneba_link)
        wait.until(EC.url_contains("category/24/dasveneba"))
        print("Navigated to 'დასვენება' for pagination.")
    except Exception as nav_err:
        print(f"Error navigating for pagination demo: {nav_err}. Aborting pagination test.")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, "bonus_nav_failure.png"); driver.save_screenshot(screenshot_path)
        return

    item_xpath_selector = "//a[contains(@class, 'group') and @href[contains(., '/offers/')]]"
    next_page_button_xpath = "//div[contains(@class, 'justify-center gap-1')]//div[last()][./img[@alt='right arrow']]"

    max_pages_to_load = 2
    pages_loaded = 0

    while pages_loaded < max_pages_to_load:
        current_page_num = pages_loaded + 1
        page_start_time = time.time()
        try:
            print(f"Waiting for items on page {current_page_num}...")
            grid_container_xpath = "//div[contains(@class, 'grid-cols-2') or contains(@class, 'grid-cols-3')]"
            wait.until(EC.presence_of_element_located((By.XPATH, grid_container_xpath)))
            wait.until(EC.visibility_of_element_located((By.XPATH, item_xpath_selector)))
            time.sleep(1)

            current_items_on_page = driver.find_elements(By.XPATH, item_xpath_selector)
            print(f"Page {current_page_num}: Found {len(current_items_on_page)} items.")

            if len(current_items_on_page) == 0 and pages_loaded > 0:
                 print("Found 0 items on a subsequent page.")
                 break

            print(f"Looking for next page button with XPath: {next_page_button_xpath}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_page_button_xpath)))

            if 'opacity-50' in next_button.get_attribute('class'):
                print("Next button appears disabled. Assuming end of pagination.")
                break
            print("Found clickable 'Next Page' button.")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", next_button)
            print(f"Clicked 'Next Page' (to load page {current_page_num + 1}). Waiting for URL update...")

            expected_next_page_param = f"page={current_page_num + 1}"
            try:
                WebDriverWait(driver, 20).until(EC.url_contains(expected_next_page_param))
                print(f"URL updated to contain '{expected_next_page_param}'. Page {current_page_num + 1} loaded.")
                pages_loaded += 1
            except TimeoutException:
                print(f"Timed out waiting for URL to contain '{expected_next_page_param}'. Pagination might have ended or URL pattern is different.")
                break

        except (TimeoutException, NoSuchElementException):
            print("No 'Next Page' button found or clickable with current selector. Assuming end of pagination.")
            break
        except ElementClickInterceptedException:
             print("Clicking 'Next Page' button was intercepted. Trying JS click again.")
             try:
                 driver.execute_script("arguments[0].click();", next_button)
                 print("Attempted force JS click. Waiting for URL update...")
                 expected_next_page_param = f"page={current_page_num + 1}"
                 WebDriverWait(driver, 20).until(EC.url_contains(expected_next_page_param))
                 print(f"URL updated after force click. Page {current_page_num + 1} loaded.")
                 pages_loaded += 1
             except Exception as js_e:
                 print(f"JS click also failed or wait timed out: {js_e}")
                 break
        except Exception as e:
            print(f"An error occurred during pagination (Page {current_page_num}): {e}")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"bonus_pagination_error_page_{pages_loaded}.png"); driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            break

        if pages_loaded >= max_pages_to_load:
            print(f"Reached max pages to load ({max_pages_to_load}).")
            break
        print(f"Page {current_page_num} processing took {time.time() - page_start_time:.2f} seconds.")
        time.sleep(1)

    final_items_count = 0
    try:
        time.sleep(1.5)
        final_items_count = len(driver.find_elements(By.XPATH, item_xpath_selector))
        print(f"Pagination loop finished. Items visible on final page ({driver.current_url}): {final_items_count}")
    except Exception as final_count_e:
        print(f"Could not count items on final page: {final_count_e}")

if __name__ == "__main__":
    driver = initialize_driver()
    if driver:
        try:
            task_1_login(driver, DUMMY_USERNAME, DUMMY_PASSWORD)
            print("-" * 50); time.sleep(1)

            task_2_navigate_and_scrape(driver)
            print("-" * 50); time.sleep(1)

            task_3_apply_filter(driver)
            print("-" * 50); time.sleep(1)

            task_4_check_images_and_screenshot(driver)
            print("-" * 50); time.sleep(1)

            bonus_handle_pagination(driver)
            print("-" * 50)

        except Exception as e:
            print(f"\nAn unexpected error occurred in the main script: {e}")
            try:
                screenshot_path = os.path.join(SCREENSHOTS_DIR, "main_script_error.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
            except: pass
        finally:
            print("\nClosing WebDriver.")
            time.sleep(3)
            driver.quit()
    else:
        print("WebDriver could not be initialized. Exiting.")



# OUTPUT 
# --------------------------------------------------

# Using ChromeDriver from system PATH.

# --- Task 1: Login Attempt ---
# Accepted cookie consent via JavaScript click.
# Attempting to click login button with XPath: //button[.//img[@alt='profile.svg'] and .//p[text()='შესვლა']]
# Clicked on the 'შესვლა' button.
# Waiting for email field with ID: Email
# Waiting for password field with ID: Password
# Entered Username: testuser@example.com
# Entered Password.
# Login form fields filled (simulated). Navigating back to homepage.
# --------------------------------------------------

# --- Task 2: Navigate and Scrape ---
# Cookie consent banner not found or timed out.
# Attempting to find category: 'დასვენება' with XPath: //a[.//p[text()='დასვენება']]
# Navigated to 'დასვენება' category.
# Waiting for item cards with XPath: //a[contains(@class, 'group') and @href[contains(., '/offers/')]]
# Product listings loaded on category page.
# Found 24 item cards. Scraping first few...
#   Item 1: Title: ეკონომ ნომერი 2 სტუმარზე ცხვარიჭამიაში, Price: 160.00₾
#   Item 2: Title: კოტეჯი 2 ადამიანზე ყვარელში, Price: 110.00₾
#   Item 3: Title: კოტეჯი 4 ადამიანზე ყვარელში, Price: 160.00₾
#   Item 4: Title: სასტუმროს ნომრები კახეთში საუზმით, Price: 80.00₾
#   Item 5: Title: სტანდარტული ნომერი 2 სტუმარზე, Price: 100.00₾
# --------------------------------------------------

# --- Task 3: Apply Category Filter ---
# Looking for filter: 'დიღომი'
# Initial items before filter: 24. First item href: https://swoop.ge/offers/482503/ekonom-nomeri-2-stumarze-cxvariamiashi/dasveneba/mtis-kurortebi/
# Clicked on filter element for: 'დიღომი'
# Waiting for filter results to potentially update...
# Detected change in first item or list potentially became empty.
# Attempting to scrape items after filter...
# Filter potentially applied. New item count: 1
# Scraping items after filter:
#   Filtered Item 1: Title: სტანდარტული ან ლუქს ნომერი 2 სტუმარზე, Price: 90.00₾
# --------------------------------------------------

# --- Task 4: Check Homepage Images and Screenshot ---
# Cookie consent banner not found or timed out.
# Waiting for images matching XPath: '//div[contains(@class,'swiper-slide')]//a[contains(@href, '/offers/')]/div[contains(@class,'relative')]//img'
# Found 23 potential product images. Checking first 5.

# Image 1: src: https://cdn.swoop.ge/ImagesStorage/dad82bab-a7b2-40a3-baf8-e79a9ff27a82.jpg, alt: ნომერი 2 სტუმარზე წინანდალში
#   Image 1: Is fully loaded (checked via JavaScript).
# /Users/ninobendianishvili/Library/Python/3.9/lib/python/site-packages/selenium/webdriver/remote/webelement.py:507: UserWarning: name used for saved screenshot does not match file type. It should end with a `.png` extension
#   warnings.warn(
#   Screenshot saved to: swoop_screenshots/swoop_image_1_dad82bab-a7b2-40a3-baf8-e79a9ff27a82.jpg

# Image 2: src: https://cdn.swoop.ge/ImagesStorage/b9ab5b7b-cb9a-4e3e-83f6-d1528a53e4a0.png, alt: Shoot 360 -ში შენთვის სასურველი ვარჯიშის რაოდენობა
#   Image 2: Is fully loaded (checked via JavaScript).
#   Screenshot saved to: swoop_screenshots/swoop_image_2_b9ab5b7b-cb9a-4e3e-83f6-d1528a53e4a0.png

# Image 3: src: https://cdn.swoop.ge/ImagesStorage/2ebf3180-a852-4286-ae47-93030b53bec8.png, alt: 31 მაისის ჩათვლით, წალკის კურორტზე, ნომერი 2 სტუმარზე
#   Image 3: Is fully loaded (checked via JavaScript).
#   Screenshot saved to: swoop_screenshots/swoop_image_3_2ebf3180-a852-4286-ae47-93030b53bec8.png

# Image 4: src: https://cdn.swoop.ge/ImagesStorage/edb6aa72-ffb9-4203-891a-0f4a40b3f36a.png, alt: მენიუ 4 პერსონაზე
#   Image 4: Is fully loaded (checked via JavaScript).
#   Screenshot saved to: swoop_screenshots/swoop_image_4_edb6aa72-ffb9-4203-891a-0f4a40b3f36a.png

# Image 5: src: https://cdn.swoop.ge/ImagesStorage/4c261076-59de-482d-8fdd-0a1215b1ad42.png, alt: 40%-იანი ფასდაკლება მობინექსის ინტერნეტ პაკეტზე
#   Image 5: Is fully loaded (checked via JavaScript).
#   Screenshot saved to: swoop_screenshots/swoop_image_5_4c261076-59de-482d-8fdd-0a1215b1ad42.png
# --------------------------------------------------

# --- Bonus: Handle Pagination Dynamically ---
# Navigating to 'დასვენება' for pagination demo.
# Cookie consent banner not found or timed out.
# Navigated to 'დასვენება' for pagination.
# Waiting for items on page 1...
# Page 1: Found 24 items.
# Looking for next page button with XPath: //div[contains(@class, 'justify-center gap-1')]//div[last()][./img[@alt='right arrow']]
# Found clickable 'Next Page' button.
# Clicked 'Next Page' (to load page 2). Waiting for URL update...
# URL updated to contain 'page=2'. Page 2 loaded.
# Page 1 processing took 2.71 seconds.
# Waiting for items on page 2...
# Page 2: Found 24 items.
# Looking for next page button with XPath: //div[contains(@class, 'justify-center gap-1')]//div[last()][./img[@alt='right arrow']]
# Found clickable 'Next Page' button.
# Clicked 'Next Page' (to load page 3). Waiting for URL update...
# URL updated to contain 'page=3'. Page 3 loaded.
# Reached max pages to load (2).
# Pagination loop finished. Items visible on final page (https://swoop.ge/category/24/dasveneba/?page=3): 24
# --------------------------------------------------

# Closing WebDriver.