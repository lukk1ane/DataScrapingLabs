#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

def check_and_save_images():
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    # Create a directory to save screenshots if it doesn't exist
    screenshots_dir = "LAB6/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    try:
        # Navigate directly to the swimming pool category
        driver.get("https://swoop.ge/category/340/sporti-/sacurao-auzi/")
        print("Directly navigated to swimming pool category")
        time.sleep(5)  # Wait for page to load
        
        # Take a screenshot
        driver.save_screenshot(f"{screenshots_dir}/category_page.png")
        print("Saved category page screenshot")
        
        # Wait for product images to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid img"))
            )
            print("Product images loaded")
        except TimeoutException:
            print("Timed out waiting for product images")
        
        # Find all product images
        try:
            # Find the product grid first
            grid = driver.find_element(By.CSS_SELECTOR, "div.grid")
            
            # Find all product images (excluding favorite icons)
            images = grid.find_elements(By.CSS_SELECTOR, "img.w-full.object-cover")
            
            print(f"Found {len(images)} product images")
            
            # Check first 5 images
            for i, img in enumerate(images[:5]):
                if i >= 5:
                    break
                    
                # Get image details
                src = img.get_attribute('src')
                alt = img.get_attribute('alt')
                
                # Check if image is loaded using JavaScript
                is_loaded = driver.execute_script("""
                    const img = arguments[0];
                    return img.complete && img.naturalHeight !== 0;
                """, img)
                
                print(f"Image {i+1}: {alt}")
                print(f"  Source: {src}")
                print(f"  Loaded: {is_loaded}")
                
                if is_loaded:
                    # Scroll to image
                    driver.execute_script("arguments[0].scrollIntoView(true);", img)
                    time.sleep(1)
                    
                    # Take screenshot of image
                    img.screenshot(f"{screenshots_dir}/image_{i+1}.png")
                    print(f"  Screenshot saved to image_{i+1}.png")
                else:
                    print("  Image not fully loaded")
                
        except NoSuchElementException:
            print("Could not find product grid or images")
        except Exception as e:
            print(f"Error checking images: {str(e)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Take a screenshot to help debug the issue
        try:
            driver.save_screenshot(f"{screenshots_dir}/error.png")
            print("Error screenshot saved to {screenshots_dir}/error.png")
        except:
            print("Could not save error screenshot")
        
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    check_and_save_images() 