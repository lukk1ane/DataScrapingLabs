from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fill_registration_form():
    # Initialize the WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the practice form website
        driver.get("https://demoqa.com/automation-practice-form")
        
        # Set a custom window size instead of maximizing to avoid compatibility issues
        driver.set_window_size(1920, 1080)
        
        # Retrieve and fill form elements using different selectors
        # First Name - using ID
        first_name = driver.find_element(By.ID, "firstName")
        first_name.send_keys("John")
        
        # Last Name - using ID
        last_name = driver.find_element(By.ID, "lastName")
        last_name.send_keys("Doe")
        
        # Email - using ID
        email = driver.find_element(By.ID, "userEmail")
        email.send_keys("john.doe@example.com")
        
        # Gender - using XPath
        gender = driver.find_element(By.XPATH, "//label[text()='Male']")
        gender.click()
        
        # Mobile Number - using ID
        mobile = driver.find_element(By.ID, "userNumber")
        mobile.send_keys("1234567890")
        
        # Date of Birth - using ID and clicking to select
        dob = driver.find_element(By.ID, "dateOfBirthInput")
        dob.click()
        # Select month
        month = Select(driver.find_element(By.CLASS_NAME, "react-datepicker__month-select"))
        month.select_by_visible_text("May")
        # Select year
        year = Select(driver.find_element(By.CLASS_NAME, "react-datepicker__year-select"))
        year.select_by_value("1990")
        # Select day
        day = driver.find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day') and text()='15']")
        day.click()
        
        # Subjects - using ID and CSS Selector with wait for autocomplete option
        logger.info("Entering subject 'Maths'")
        subjects = driver.find_element(By.ID, "subjectsInput")
        subjects.send_keys("Maths")
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".subjects-auto-complete__option"))
            ).click()
            logger.info("Selected subject 'Maths' from autocomplete")
        except Exception as e:
            logger.error(f"Failed to select subject from autocomplete: {str(e)}")
        
        # Hobbies - using XPath with wait
        logger.info("Selecting hobby 'Sports'")
        hobbies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Sports']"))
        )
        hobbies.click()
        logger.info("Selected hobby 'Sports'")
        
        # Address - using ID with wait
        logger.info("Entering address")
        address = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "currentAddress"))
        )
        address.send_keys("123 Main St, City, Country")
        logger.info("Entered address")
        
        # State - using ID and CSS Selector with wait, scroll into view to avoid interception
        logger.info("Selecting state")
        state = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "state"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", state)
        state.click()
        option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='react-select-3-option-0']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", option)
        option.click()
        logger.info("Selected state")
        
        # City - using ID and CSS Selector with wait, scroll into view to avoid interception
        logger.info("Selecting city")
        city = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "city"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", city)
        city.click()
        option_city = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id*='react-select-4-option-0']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", option_city)
        option_city.click()
        logger.info("Selected city")
        
        # Do not submit the form as per user request
        logger.info("Form filling completed, not submitting as per instructions")
        
        time.sleep(3)  # Wait to see the result
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    fill_registration_form()