import time
import csv
import os
import platform
import random 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

CHROMEDRIVER_PATH = "/Users/ninobendianishvili/Documents/py_ttf_1/DataScrapingLabs/week9/chromedriver"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_driver(custom_options=None):
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = custom_options if custom_options else Options()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def task_1_fill_form():
    print("--- Starting Task 1: Fill Registration Form ---")
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://demoqa.com/automation-practice-form")
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        try:
            fixed_banner = driver.find_element(By.ID, "fixedban")
            driver.execute_script("arguments[0].style.display = 'none';", fixed_banner)
        except Exception:
            pass 

        first_name_input = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        first_name_input.send_keys("Nino")

        last_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='lastName']")))
        last_name_input.send_keys("Bendianishvili")

        email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#userEmail")))
        email_input.send_keys("bendianishvili.nino@kiu.edu.ge")

        gender_female_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='gender-radio-2']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", gender_female_label)
        time.sleep(0.5) 
        gender_female_label.click()

        mobile_number = "".join([str(random.randint(0, 9)) for _ in range(10)])
        mobile_input = wait.until(EC.element_to_be_clickable((By.ID, "userNumber")))
        driver.execute_script("arguments[0].scrollIntoView(true);", mobile_input)
        time.sleep(0.5)
        mobile_input.send_keys(mobile_number)

        dob_input_container = wait.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput")))
        driver.execute_script("arguments[0].scrollIntoView(true);", dob_input_container)
        time.sleep(0.5)
        dob_input_container.click()

        month_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
        month_select.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@class='react-datepicker__month-select']/option[text()='February']"))).click()

        year_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__year-select")))
        year_select.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@class='react-datepicker__year-select']/option[text()='2003']"))).click()
        
        day_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'react-datepicker__day--002') and text()='2' and not(contains(@class, 'react-datepicker__day--outside-month'))]")))
        day_element.click()

        subjects_input_container = wait.until(EC.visibility_of_element_located((By.ID, "subjectsInput")))
        driver.execute_script("arguments[0].scrollIntoView(true);", subjects_input_container)
        time.sleep(0.5)
        
        actions = ActionChains(driver)
        
        subjects_to_add = ["Computer Science", "English"] 
        for subject in subjects_to_add:
            actions.move_to_element(subjects_input_container).click().send_keys(subject).perform()
            try:
                subject_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(@class, 'subjects-auto-complete__option') and text()='{subject}']")))
                subject_option.click()
            except: 
                print(f"Could not find exact subject option for {subject}, trying Enter key.")
                actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5) 


        all_hobbies_labels = driver.find_elements(By.XPATH, "//div[@id='hobbiesWrapper']//label[contains(@for, 'hobbies-checkbox-')]")
        if all_hobbies_labels:
            num_hobbies_to_select = random.randint(1, min(2, len(all_hobbies_labels))) 
            selected_hobbies = random.sample(all_hobbies_labels, num_hobbies_to_select)
            for hobby_label in selected_hobbies:
                driver.execute_script("arguments[0].scrollIntoView(true);", hobby_label)
                time.sleep(0.3)
                hobby_label.click()
        
        upload_picture_input = wait.until(EC.presence_of_element_located((By.ID, "uploadPicture")))
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_picture_input)
        time.sleep(0.5)
        dummy_file_path = os.path.join(SCRIPT_DIR, "dummy.txt")
        if not os.path.exists(dummy_file_path):
            with open(dummy_file_path, "w") as f:
                f.write("This is a dummy file for upload test.")
        upload_picture_input.send_keys(dummy_file_path)

        random_address = f"{random.randint(100, 999)} Random Street, Suite {random.randint(1,100)}, Tbilisi, Georgia"
        current_address_input = wait.until(EC.element_to_be_clickable((By.ID, "currentAddress")))
        driver.execute_script("arguments[0].scrollIntoView(true);", current_address_input)
        time.sleep(0.5)
        current_address_input.send_keys(random_address)

        submit_button_for_scroll = driver.find_element(By.ID, "submit") 
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button_for_scroll)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -200);") 
        time.sleep(0.5)

        state_dropdown_container = wait.until(EC.element_to_be_clickable((By.ID, "state")))
        state_dropdown_container.click()
        ncr_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'react-select-3-option') and text()='NCR']")))
        ncr_option.click()

        city_dropdown_container = wait.until(EC.element_to_be_clickable((By.ID, "city")))
        city_dropdown_container.click()
        delhi_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'react-select-4-option') and text()='Delhi']")))
        delhi_option.click()

        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit_button)
        time.sleep(0.5) 
        driver.execute_script("arguments[0].click();", submit_button)
        
        try:
            confirmation_modal_header = wait.until(
                EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
            )
            if "Thanks for submitting the form" in confirmation_modal_header.text:
                print(f"Submission Confirmed! Modal Title: {confirmation_modal_header.text}")
            else:
                print(f"Modal appeared, but title is unexpected: {confirmation_modal_header.text}")
            
            close_button = wait.until(EC.element_to_be_clickable((By.ID, "closeLargeModal")))
            driver.execute_script("arguments[0].click();", close_button)
            print("Confirmation modal closed.")
        except Exception as e:
            print(f"Could not find or interact with confirmation modal: {e}")
            if driver: print(f"Current URL after submit: {driver.current_url}")

        print("Task 1: Form automation completed.")
        time.sleep(3) 

    except Exception as e:
        print(f"An error occurred in Task 1: {e}")
        if driver:
            screenshot_path = os.path.join(SCRIPT_DIR, "task1_error_screenshot.png")
            try:
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except Exception as se:
                print(f"Could not save screenshot: {se}")
    finally:
        if driver:
            driver.quit()
        print("--- Task 1 Finished ---")

def run_book_extraction(driver, all_books_csv_name, five_star_csv_name, mode_description):
    print(f"\nStarting book extraction in {mode_description}...")
    try:
        driver.get("https://books.toscrape.com/")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product_pod")))

        all_books_data = []
        five_star_books_data = []

        book_container_selector = "article.product_pod"
        title_selector = "h3 a"
        price_selector = "div.product_price p.price_color"
        rating_selector = "p.star-rating" 
        availability_selector = "div.product_price p.instock.availability"

        book_elements = driver.find_elements(By.CSS_SELECTOR, book_container_selector)
        print(f"Found {len(book_elements)} books on the first page ({mode_description}).")

        for book_element in book_elements:
            try:
                title = book_element.find_element(By.CSS_SELECTOR, title_selector).get_attribute("title")
                price_text = book_element.find_element(By.CSS_SELECTOR, price_selector).text
                rating_classes = book_element.find_element(By.CSS_SELECTOR, rating_selector).get_attribute("class")
                rating_word = rating_classes.split(" ")[-1] 
                rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                star_rating_value = rating_map.get(rating_word, 0)
                availability_text = book_element.find_element(By.CSS_SELECTOR, availability_selector).text.strip()

                book_details = {
                    "Title": title,
                    "Price": price_text,
                    "Star Rating": star_rating_value,
                    "Availability": availability_text
                }
                all_books_data.append(book_details)

                if star_rating_value == 5:
                    five_star_books_data.append(book_details)
            
            except Exception as e_book:
                print(f"Error extracting details for one book: {e_book}")
                all_books_data.append({
                    "Title": "Extraction Error", "Price": "N/A", 
                    "Star Rating": 0, "Availability": "N/A"
                })

        all_books_csv_path = os.path.join(SCRIPT_DIR, all_books_csv_name)
        with open(all_books_csv_path, mode='w', newline='', encoding='utf-8') as file:
            if all_books_data:
                writer = csv.DictWriter(file, fieldnames=all_books_data[0].keys())
                writer.writeheader()
                writer.writerows(all_books_data)
        print(f"All book data saved to: {all_books_csv_path}")

        five_star_csv_path = os.path.join(SCRIPT_DIR, five_star_csv_name)
        with open(five_star_csv_path, mode='w', newline='', encoding='utf-8') as file:
            if five_star_books_data:
                writer = csv.DictWriter(file, fieldnames=five_star_books_data[0].keys())
                writer.writeheader()
                writer.writerows(five_star_books_data)
                print(f"5-star book data saved to: {five_star_csv_path} ({len(five_star_books_data)} books)")
            elif all_books_data: 
                writer = csv.DictWriter(file, fieldnames=all_books_data[0].keys())
                writer.writeheader()
                print(f"No 5-star books found. Empty 5-star CSV created: {five_star_csv_path}")
            else:
                 print(f"No data extracted, skipping CSV creation for 5-star books.")

        print(f"Book extraction completed for {mode_description}.")
        if "headless" not in mode_description.lower():
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred during book extraction ({mode_description}): {e}")

def task_2_scrape_books():
    print("\n--- Starting Task 2: Scrape Book Information ---")
    driver_maximized, driver_custom_size, driver_headless = None, None, None 

    try:
        print("\nRunning extraction in MAXIMIZED window mode...")
        maximized_options = Options()
        driver_maximized = setup_driver(maximized_options)
        driver_maximized.maximize_window()
        run_book_extraction(driver_maximized, "books_all_maximized.csv", "5_star_books_maximized.csv", "Maximized Window Mode")
    except Exception as e:
        print(f"Error in Maximized mode for Task 2: {e}")
    finally:
        if driver_maximized:
            driver_maximized.quit()

    try:
        print("\nRunning extraction in CUSTOM window size (800x600)...")
        custom_size_options = Options()
        driver_custom_size = setup_driver(custom_size_options)
        driver_custom_size.set_window_size(800, 600)
        run_book_extraction(driver_custom_size, "books_all_custom_size.csv", "5_star_books_custom_size.csv", "Custom Window Size (800x600) Mode")
    except Exception as e:
        print(f"Error in Custom Size mode for Task 2: {e}")
    finally:
        if driver_custom_size:
            driver_custom_size.quit()

    try:
        print("\nRunning extraction in HEADLESS mode...")
        headless_options = Options()
        headless_options.add_argument("--headless")
        headless_options.add_argument("--window-size=1920,1080") 
        driver_headless = setup_driver(headless_options)
        run_book_extraction(driver_headless, "books_all_headless.csv", "5_star_books_headless.csv", "Headless Mode")
    except Exception as e:
        print(f"Error in Headless mode for Task 2: {e}")
    finally:
        if driver_headless:
            driver_headless.quit()
    
    print("--- Task 2 Finished ---")


if __name__ == "__main__":
    task_1_fill_form()
    
    print("\n" + "="*50 + "\n") 
    
    task_2_scrape_books()

    print("\nAll tasks completed. Check your project directory for CSV files and dummy.txt.")