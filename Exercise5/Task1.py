from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def automate_practice_form():
    # Initialize the driver with options to handle ads
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Navigate to the practice form
        driver.get("https://demoqa.com/automation-practice-form")

        # Wait for page to load and dismiss any ads
        time.sleep(2)  # Wait for page to stabilize

        # Close any ads that might be present
        try:
            # Try to close the ad if it exists
            driver.execute_script("""
                const iframes = document.getElementsByTagName('iframe');
                for (let iframe of iframes) {
                    if (iframe.title === 'Advertisement') {
                        iframe.style.display = 'none';
                    }
                }
            """)
        except:
            pass

        # Fill in the form using different selectors
        # First Name - using ID
        first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstName"))
        )
        first_name.send_keys("John")

        # Last Name - using CSS selector
        last_name = driver.find_element(By.CSS_SELECTOR, "#lastName")
        last_name.send_keys("Doe")

        # Email - using XPath
        email = driver.find_element(By.XPATH, "//input[@id='userEmail']")
        email.send_keys("john.doe@example.com")

        # Gender - using JavaScript click to avoid interception
        gender = driver.find_element(By.XPATH, "//label[contains(text(),'Male')]")
        driver.execute_script("arguments[0].click();", gender)

        # Mobile Number - using class name
        mobile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#userNumber"))
        )
        mobile.clear()
        mobile.send_keys("1234567890")

        # Date of Birth - using JavaScript to set value directly
        dob = driver.find_element(By.ID, "dateOfBirthInput")
        driver.execute_script("arguments[0].value = '03 Dec 2003';", dob)

        # Subjects - using ID and sending keys
        subjects = driver.find_element(By.ID, "subjectsInput")
        subjects.send_keys("CS")
        subjects.send_keys(webdriver.Keys.RETURN)

        # Hobbies - using JavaScript click to avoid interception
        hobbies = driver.find_element(By.XPATH, "//label[contains(text(),'Sports')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", hobbies)
        driver.execute_script("arguments[0].click();", hobbies)

        # Upload picture - using ID
        upload = driver.find_element(By.ID, "uploadPicture")
        upload.send_keys('D:/Python/DataScraping/Exercise1/DataScrapingLabs/Exercise5/yumaryumar.jpg')

        # Current Address - using CSS selector
        address = driver.find_element(By.CSS_SELECTOR, "#currentAddress")
        address.send_keys("21 V, KUTAISI SMN, Georgia")

        # State and City
        try:
            # Scroll to the state dropdown
            state_container = driver.find_element(By.ID, "state")
            driver.execute_script("arguments[0].scrollIntoView(true);", state_container)

            # Click to open state dropdown
            state_dropdown = driver.find_element(By.CSS_SELECTOR, "#state div div")
            state_dropdown.click()

            # Select state
            state_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='NCR']"))
            )
            state_option.click()

            city_container = driver.find_element(By.ID, "city")
            driver.execute_script("arguments[0].scrollIntoView(true);", city_container)

            # Click to open state dropdown
            city_dropdown = driver.find_element(By.CSS_SELECTOR, "#city div div")
            city_dropdown.click()

            # Select city
            city_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Delhi']"))
            )
            city_option.click()

        except Exception as e:
            print(f"State/City selection failed: {e}")

        # Submit form
        try:
            submit = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit)
            driver.execute_script("arguments[0].click();", submit)

            # Wait for submission confirmation
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg"))
            )
            print("Form submitted successfully!")
        except:
            print("Form submission confirmation not found.")

        time.sleep(3)

    finally:
        driver.quit()


# Run the function
automate_practice_form()
