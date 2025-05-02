from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
driver.maximize_window()


driver.get("https://demoqa.com/automation-practice-form")


driver.find_element(By.ID, "firstName").send_keys("John")
driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys("Doe")
driver.find_element(By.XPATH, "//input[@id='userEmail']").send_keys("john@example.com")
driver.find_element(By.XPATH, "//label[text()='Male']").click()
driver.find_element(By.ID, "userNumber").send_keys("1234567890")

driver.find_element(By.ID, "submit").click()

time.sleep(3)
driver.quit()
