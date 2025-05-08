#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def login_to_swoop():
    # Initialize Chrome driver (already installed on Arch Linux)
    driver = webdriver.Chrome()
    
    try:
        # Open the website
        driver.get("https://swoop.ge/")
        print("Opened swoop.ge")
        
        # Add a small delay to ensure the page is fully loaded
        time.sleep(3)
        
        print("Looking for login button...")
        
        # Try multiple methods to find the login button
        login_button = None
        
        # Method 1: Try the most specific selector based on the HTML provided
        try:
            print("Trying to find button with data-testid='outline-button' containing 'შესვლა'...")
            login_button = driver.find_element(By.XPATH, 
                "//button[@data-testid='outline-button' and .//p[contains(text(), 'შესვლა')]]")
            print("Found login button with method 1")
        except NoSuchElementException:
            print("Method 1 failed")
        
        # Method 2: Try finding by data-testid only
        if not login_button:
            try:
                print("Trying to find button with data-testid='outline-button'...")
                login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='outline-button']")
                print("Found login button with method 2")
            except NoSuchElementException:
                print("Method 2 failed")
        
        # Method 3: Try finding by text content
        if not login_button:
            try:
                print("Trying to find button containing text 'შესვლა'...")
                login_button = driver.find_element(By.XPATH, "//button[.//p[contains(text(), 'შესვლა')]]")
                print("Found login button with method 3")
            except NoSuchElementException:
                print("Method 3 failed")
        
        # Method 4: Try finding by class
        if not login_button:
            try:
                print("Trying to find button with laptop:flex class...")
                login_button = driver.find_element(By.CSS_SELECTOR, "button.laptop\\:flex")
                print("Found login button with method 4")
            except NoSuchElementException:
                print("Method 4 failed")
                
        # If all methods failed, print all buttons on the page for debugging
        if not login_button:
            print("All methods failed. Listing all buttons on page:")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for i, btn in enumerate(buttons):
                print(f"Button {i+1}: {btn.get_attribute('outerHTML')[:100]}...")
            
            print("\nTrying to find any element containing 'შესვლა':")
            georgian_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'შესვლა')]")
            for i, elem in enumerate(georgian_elements):
                print(f"Element {i+1}: {elem.get_attribute('outerHTML')[:100]}...")
            
            raise Exception("Could not find login button with any method")
        
        # Now we have the login button, click it
        print("Clicking login button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        time.sleep(1)  # Small delay after scrolling
        login_button.click()
        print("Clicked on login button")
        
        # Wait for login form to appear (trying multiple selectors)
        print("Waiting for login form to appear...")
        login_form_found = False
        
        for form_selector in [
            "form.login-form", 
            "form", 
            ".login-form", 
            ".modal", 
            ".login-modal",
            ".auth-form",
            "div[role='dialog']"
        ]:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, form_selector))
                )
                print(f"Login form found with selector: {form_selector}")
                login_form_found = True
                break
            except TimeoutException:
                continue
        
        if not login_form_found:
            print("Could not find login form with standard selectors.")
            print("Checking if any new elements appeared after clicking login...")
            
            # Get all input elements that might be part of a login form
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[type='text'], input[type='password']")
            if inputs:
                print(f"Found {len(inputs)} input fields that might be part of login form")
                login_form_found = True
            else:
                print("No input fields found that could be part of login form")
        
        # Try to find username/email and password fields
        if login_form_found:
            print("Looking for username/email field...")
            username_field = None
            password_field = None
            
            for email_selector in [
                "input[type='email']", 
                "input[name='email']", 
                "input[placeholder*='email']",
                "input[placeholder*='mail']", 
                "input[type='text']"
            ]:
                try:
                    username_field = driver.find_element(By.CSS_SELECTOR, email_selector)
                    print(f"Found username field with selector: {email_selector}")
                    break
                except NoSuchElementException:
                    continue
            
            print("Looking for password field...")
            for pwd_selector in ["input[type='password']"]:
                try:
                    password_field = driver.find_element(By.CSS_SELECTOR, pwd_selector)
                    print(f"Found password field with selector: {pwd_selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if username_field and password_field:
                username_field.send_keys("test_username@example.com")
                password_field.send_keys("test_password")
                print("Entered login credentials")
            else:
                print("Could not find both username and password fields")
        
        # Wait to see the result (for demonstration purposes)
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Take a screenshot to help debug the issue
        try:
            driver.save_screenshot("LAB6/login_debug.png")
            print("Screenshot saved to LAB6/login_debug.png")
        except:
            print("Could not save screenshot")
        
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    login_to_swoop() 