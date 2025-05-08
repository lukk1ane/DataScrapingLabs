from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

driver = webdriver.Chrome()
driver.get("https://swoop.ge/category/110/sporti")
wait = WebDriverWait(driver, 10)

initial_results = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "a.group.flex.flex-col.gap-3.cursor-pointer")
))
initial_count = len(initial_results)
print(f"Initial results count: {initial_count}")

location_checkbox = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@id='checkbox-მდებარეობა-4']")
))
location_checkbox.click()

price_range = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//div[@role='radio']//p[contains(text(), '100₾ - 200₾')]//parent::div")
))
price_range.click()

payment_type = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@id='radio-გადახდის ტიპი-2']")
))
payment_type.click()

if initial_results:
    wait.until(EC.staleness_of(initial_results[0]))

filtered_results = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "a.group.flex.flex-col.gap-3.cursor-pointer")
))
filtered_count = len(filtered_results)
print(f"Filtered results count: {filtered_count}")

time.sleep(10)

driver.quit()
