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

WEBSITE = "https://swoop.ge/"
# Navigate to the form
driver.get(WEBSITE)
driver.maximize_window()

# Wait for the page to load
wait = WebDriverWait(driver, 2)

try:

    # task1
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'შესვლა')]")))
    login_button.click()

    wait.until(EC.visibility_of_element_located((By.ID, "LoginForm")))
    email_field = wait.until(EC.element_to_be_clickable((By.ID, "Email")))
    example_email = "example@gmail.com"
    email_field.send_keys(example_email)
    time.sleep(2)
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "Password")))
    example_password = 'example_pass'
    password_field.send_keys(example_password)
    time.sleep(5)
    driver.get(WEBSITE)

except Exception as e:
    print(e)
finally:
    time.sleep(5)
    driver.quit()



