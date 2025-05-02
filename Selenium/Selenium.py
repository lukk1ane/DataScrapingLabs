from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://demoqa.com/automation-practice-form")

driver.maximize_window()
wait = WebDriverWait(driver, 10)

driver.find_element(By.ID, "firstName").send_keys("Erekle")

driver.find_element(By.ID, "lastName").send_keys("Bagrationi")

driver.find_element(By.CSS_SELECTOR, "input#userEmail").send_keys("erekle@example.com")

driver.find_element(By.XPATH, "//label[text()='Male']").click()

driver.find_element(By.ID, "userNumber").send_keys("5551234567")

driver.find_element(By.ID, "dateOfBirthInput").click()
Select(driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")).select_by_visible_text("May")
Select(driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")).select_by_visible_text("1995")
driver.find_element(By.XPATH, "//div[contains(@class,'react-datepicker__day') and text()='10']").click()

subjects_input = driver.find_element(By.ID, "subjectsInput")
subjects_input.send_keys("Maths")
subjects_input.send_keys(Keys.ENTER)

sports_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Sports']")))
driver.execute_script("arguments[0].scrollIntoView(true);", sports_checkbox)
time.sleep(1)
sports_checkbox.click()

driver.find_element(By.ID, "currentAddress").send_keys("Kutaisi, Georgia")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element(By.CSS_SELECTOR, "#state").click()
driver.find_element(By.XPATH, "//div[text()='NCR']").click()
driver.find_element(By.CSS_SELECTOR, "#city").click()
driver.find_element(By.XPATH, "//div[text()='Delhi']").click()

driver.find_element(By.ID, "submit").click()

time.sleep(15)
driver.quit()