from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# Using the provided path
driver = webdriver.Chrome()
# Navigate to the form
driver.get("https://demoqa.com/automation-practice-form")
driver.maximize_window()

# Wait for the page to load
wait = WebDriverWait(driver, 10)

try:
    # Fill out first name and last name
    first_name = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
    first_name.send_keys("John")

    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Doe")

    # Fill out email
    email = driver.find_element(By.ID, "userEmail")
    email.send_keys("john.doe@example.com")

    # Select gender (using radio button)
    gender = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
    driver.execute_script("arguments[0].scrollIntoView();", gender)
    driver.execute_script("arguments[0].click();", gender)

    # Fill out mobile number
    mobile = driver.find_element(By.ID, "userNumber")
    mobile.send_keys("1234567890")

    # Fill out date of birth
    dob_input = driver.find_element(By.ID, "dateOfBirthInput")
    driver.execute_script("arguments[0].scrollIntoView();", dob_input)
    dob_input.click()

    # Select a date from the date picker
    month_select = driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")
    month_select.click()
    month_option = driver.find_element(By.XPATH, "//option[text()='May']")
    month_option.click()

    year_select = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_select.click()
    year_option = driver.find_element(By.XPATH, "//option[text()='2000']")
    year_option.click()

    # Select day 15
    day = driver.find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day--015')]")
    day.click()

    # Enter Subjects
    subjects_input = driver.find_element(By.ID, "subjectsInput")
    driver.execute_script("arguments[0].scrollIntoView();", subjects_input)
    subjects_input.send_keys("Computer Science")
    subjects_input.send_keys(Keys.ENTER)

    # Select Hobbies (checkboxes)
    sports_hobby = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
    driver.execute_script("arguments[0].scrollIntoView();", sports_hobby)
    driver.execute_script("arguments[0].click();", sports_hobby)

    reading_hobby = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-2']")
    driver.execute_script("arguments[0].click();", reading_hobby)

    # Upload Picture
    upload_button = driver.find_element(By.ID, "uploadPicture")
    driver.execute_script("arguments[0].scrollIntoView();", upload_button)

    # Provide path to a sample image file
    file_path = os.path.abspath("path/to/image.jpg")  # Update with your image path
    upload_button.send_keys(file_path)

    # Current Address
    current_address = driver.find_element(By.ID, "currentAddress")
    driver.execute_script("arguments[0].scrollIntoView();", current_address)
    current_address.send_keys("123 Testing Street, Selenium City, 12345")

    # Select State and City
    state_dropdown = driver.find_element(By.ID, "state")
    driver.execute_script("arguments[0].scrollIntoView();", state_dropdown)
    driver.execute_script("arguments[0].click();", state_dropdown)

    # Select NCR state
    state_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='NCR']")))
    state_option.click()

    # Select City
    city_dropdown = driver.find_element(By.ID, "city")
    driver.execute_script("arguments[0].click();", city_dropdown)

    # Select Delhi city
    city_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Delhi']")))
    city_option.click()

    # Submit the form
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    driver.execute_script("arguments[0].click();", submit_button)

    # Wait for confirmation dialog
    wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
    print("Form submitted successfully!")

    # Take a screenshot of the confirmation

    # Close the confirmation dialog
    close_button = driver.find_element(By.ID, "closeLargeModal")
    close_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    time.sleep(10)  # Wait to see the final result
    driver.quit()