#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def apply_filters_and_scrape():
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    # Create a screenshots directory for debugging
    screenshots_dir = "LAB6/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    try:
        # Open the website
        driver.get("https://swoop.ge/")
        print("Opened swoop.ge")
        time.sleep(3)  # Allow page to fully load
        
        # Save screenshot of homepage
        driver.save_screenshot(f"{screenshots_dir}/homepage.png")
        print("Saved homepage screenshot")
        
        # Use direct navigation to the swimming pool category
        driver.get("https://swoop.ge/category/340/sporti-/sacurao-auzi/")
        print("Directly navigated to swimming pool category")
        time.sleep(5)  # Wait longer for page to load
        
        # Take a screenshot
        driver.save_screenshot(f"{screenshots_dir}/category_page.png")
        print("Saved category page screenshot")
        
        # Wait for the product grid to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid"))
            )
            print("Product grid loaded")
        except TimeoutException:
            print("Timed out waiting for product grid")
        
        # Now look for filter options
        try:
            # Find different types of filter elements
            filter_options = []
            
            # Look for filter buttons
            filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='filter']")
            if filter_buttons:
                filter_options.extend(filter_buttons)
                print(f"Found {len(filter_buttons)} filter buttons")
            
            # Look for filter dropdowns
            filter_dropdowns = driver.find_elements(By.CSS_SELECTOR, "select[class*='filter'], div[role='combobox']")
            if filter_dropdowns:
                filter_options.extend(filter_dropdowns)
                print(f"Found {len(filter_dropdowns)} filter dropdowns")
            
            # Look for checkboxes or radio buttons
            filter_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'], input[type='radio']")
            if filter_checkboxes:
                filter_options.extend(filter_checkboxes)
                print(f"Found {len(filter_checkboxes)} filter checkboxes/radios")
            
            if filter_options:
                # Count products before filtering
                products_before = len(driver.find_elements(By.CSS_SELECTOR, "div.grid > div.relative"))
                print(f"Products before filtering: {products_before}")
                
                # Click the first available filter
                filter_element = filter_options[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", filter_element)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", filter_element)
                print(f"Clicked on filter element")
                
                # Wait for page to update
                time.sleep(3)
                
                # Count products after filtering
                products_after = len(driver.find_elements(By.CSS_SELECTOR, "div.grid > div.relative"))
                print(f"Products after filtering: {products_after}")
                
                if products_before != products_after:
                    print("Filter successfully applied!")
                else:
                    print("Filter may not have been applied or had no effect")
            else:
                print("No filter elements found")
        except Exception as e:
            print(f"Error working with filters: {str(e)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Take a screenshot to help debug the issue
        try:
            driver.save_screenshot(f"{screenshots_dir}/error.png")
            print("Error screenshot saved")
        except:
            print("Could not save error screenshot")
        
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    apply_filters_and_scrape() 