from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service = Service('./drivers/chromedriver.exe')  # Adjust for your OS
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://demoqa.com/automation-practice-form")
driver.maximize_window()

driver.find_element(By.ID, "firstName").send_keys("John")
driver.find_element(By.ID, "lastName").send_keys("Doe")
driver.find_element(By.ID, "userEmail").send_keys("johndoe@example.com")
driver.find_element(By.XPATH, "//label[@for='gender-radio-1']").click()
driver.find_element(By.ID, "userNumber").send_keys("1234567890")

driver.execute_script("window.scrollBy(0, 500);")
driver.find_element(By.ID, "submit").click()

time.sleep(3)
driver.quit()