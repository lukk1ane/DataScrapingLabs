from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os

driver_path = "/Users/atukaberadze/Desktop/chromedriver-mac-arm64/chromedriver"
os.chmod(driver_path, 0o755)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")


driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
driver.get("https://demoqa.com/automation-practice-form")

try:
    driver.execute_script("""
        document.getElementById('fixedban').style.display = 'none';
        let modal = document.querySelector('.modal-content');
        if (modal) modal.style.display = 'none';
    """)
except:
    pass

driver.find_element(By.ID, "firstName").send_keys("John")
driver.find_element(By.ID, "lastName").send_keys("Doe")
driver.find_element(By.ID, "userEmail").send_keys("johndoe@example.com")

gender_radio = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
driver.execute_script("arguments[0].scrollIntoView(true);", gender_radio)
time.sleep(0.3)
gender_radio.click()

driver.find_element(By.ID, "userNumber").send_keys("1234567890")

driver.find_element(By.ID, "dateOfBirthInput").click()
driver.find_element(By.CLASS_NAME, "react-datepicker__year-select").send_keys("1990")
driver.find_element(By.CLASS_NAME, "react-datepicker__month-select").send_keys("January")
driver.find_element(By.CLASS_NAME, "react-datepicker__day--001").click()

subject_input = driver.find_element(By.ID, "subjectsInput")
subject_input.send_keys("Maths")
subject_input.send_keys(Keys.ENTER)
time.sleep(0.5)

hobby_checkbox = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
driver.execute_script("arguments[0].scrollIntoView(true);", hobby_checkbox)
time.sleep(0.3)
hobby_checkbox.click()

driver.find_element(By.ID, "currentAddress").send_keys("123 Main St")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)
driver.find_element(By.ID, "submit").click()

time.sleep(3)
driver.quit()
