#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
import os

def handle_dynamic_pagination():
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
        
        # Save a screenshot of the homepage
        driver.save_screenshot(f"{screenshots_dir}/homepage.png")
        print("Saved homepage screenshot")
        
        # Try to navigate to a category with pagination
        print("Attempting to navigate to a product category...")
        category_found = False
        
        try:
            # Try different approaches to find and click a category
            for selector in [
                "a[href*='/category/electronics']",
                "a[href*='/products']",
                "a[href*='/category']", 
                "//a[contains(@href, '/category')]",
                "//a[contains(text(), 'ელექტრონიკა')]",  # Georgian for "electronics"
                ".category-item"
            ]:
                try:
                    elements = []
                    if selector.startswith("//"):
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                print(f"Found category link with selector: {selector}")
                                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                element.click()
                                category_found = True
                                print(f"Clicked on category: {element.text or element.get_attribute('href')}")
                                time.sleep(3)  # Wait for navigation
                                break
                    
                    if category_found:
                        break
                except Exception as e:
                    print(f"Error with selector {selector}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error finding category through UI: {str(e)}")
        
        # If UI navigation fails, try direct navigation
        if not category_found:
            print("UI navigation failed. Trying direct navigation...")
            driver.get("https://swoop.ge/category/electronics")
            print("Directly navigated to electronics category")
            time.sleep(3)  # Wait for page to load
        
        # Take a screenshot of the category page
        driver.save_screenshot(f"{screenshots_dir}/category_page.png")
        print("Saved category page screenshot")
        
        # Find and identify product elements
        print("Looking for product elements...")
        products_found = False
        product_selector_used = None
        
        for selector in [
            ".product-card", 
            ".card", 
            "[class*='product']",
            "article", 
            ".item", 
            "div[class*='card']"
        ]:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 0:
                    print(f"Found {len(elements)} product elements with selector: {selector}")
                    products_found = True
                    product_selector_used = selector
                    break
            except Exception as e:
                print(f"Error with product selector {selector}: {str(e)}")
                continue
        
        if not products_found:
            print("Could not find product elements with standard selectors")
            print("Listing some page elements for debugging:")
            divs = driver.find_elements(By.CSS_SELECTOR, "div[class]")
            for i, div in enumerate(divs[:10]):  # Show first 10 divs
                print(f"Div {i+1}: class='{div.get_attribute('class')}' text='{div.text[:30]}...'")
            return
        
        # Get initial products for comparison
        print("Getting initial product data for later comparison...")
        initial_products = driver.find_elements(By.CSS_SELECTOR, product_selector_used)
        
        # Function to extract product information
        def extract_product_info(product):
            info = {'title': None, 'price': None}
            
            # Try different selectors for title
            for selector in [".product-title", "h2", "h3", ".title", "[class*='title']", ".name"]:
                try:
                    element = product.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text.strip():
                        info['title'] = element.text.strip()
                        break
                except:
                    continue
            
            # Try different selectors for price
            for selector in [".product-price", ".price", "[class*='price']", ".cost"]:
                try:
                    element = product.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text.strip():
                        info['price'] = element.text.strip()
                        break
                except:
                    continue
            
            return info
        
        # Extract initial product data (first 5 products)
        initial_product_data = []
        for i, product in enumerate(initial_products[:5]):
            try:
                info = extract_product_info(product)
                if info['title']:
                    initial_product_data.append(info)
                    print(f"Initial product {i+1}: {info['title']}")
            except Exception as e:
                print(f"Error extracting initial product data: {str(e)}")
        
        if not initial_product_data:
            print("Could not extract any initial product data")
            return
        
        # Define a function to check if products have changed (more robust)
        def products_have_changed():
            try:
                # Find current products
                current_products = driver.find_elements(By.CSS_SELECTOR, product_selector_used)
                
                # If the count has changed dramatically, that's a good sign
                if abs(len(current_products) - len(initial_products)) > 2:
                    print("Product count has changed significantly")
                    return True
                
                # Extract data from current products
                current_product_data = []
                for product in current_products[:5]:
                    info = extract_product_info(product)
                    if info['title']:
                        current_product_data.append(info)
                
                # Compare product titles
                initial_titles = [p['title'] for p in initial_product_data if p['title']]
                current_titles = [p['title'] for p in current_product_data if p['title']]
                
                # Calculate how many titles have changed
                changed_count = sum(1 for title in current_titles if title not in initial_titles)
                
                # If more than half the products have changed, consider it a page change
                if changed_count >= len(initial_titles) // 2:
                    print(f"{changed_count} out of {len(initial_titles)} products have changed")
                    return True
                
                return False
                
            except StaleElementReferenceException:
                # If we get this exception, the DOM has been updated
                print("Detected StaleElementReferenceException - DOM has been updated")
                return True
        
        # Look for pagination elements
        print("\nLooking for pagination controls...")
        pagination_found = False
        pagination_element = None
        
        for selector in [
            ".pagination",
            ".pager",
            "nav[aria-label*='page']",
            "[class*='pagination']",
            ".pages",
            "ul.page-numbers",
            "//div[contains(@class, 'pagination')]",
            "//ul[contains(@class, 'pagination')]"
        ]:
            try:
                elements = []
                if selector.startswith("//"):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    for element in elements:
                        if element.is_displayed():
                            print(f"Found pagination with selector: {selector}")
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            pagination_element = element
                            pagination_found = True
                            
                            # Take a screenshot of the pagination element
                            driver.save_screenshot(f"{screenshots_dir}/pagination_element.png")
                            print("Saved screenshot of pagination element")
                            break
                
                if pagination_found:
                    break
            except Exception as e:
                print(f"Error with pagination selector {selector}: {str(e)}")
                continue
        
        if not pagination_found:
            print("No pagination controls found. Examining the page for potential pagination elements:")
            
            # Look for elements that might contain pagination controls
            potential_elements = []
            
            for selector in ["a[href*='page'], button[class*='page'], div[class*='page']"]:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                potential_elements.extend(elements)
            
            if potential_elements:
                print(f"Found {len(potential_elements)} potential pagination elements")
                for i, element in enumerate(potential_elements[:5]):
                    print(f"Potential element {i+1}: {element.tag_name} - {element.get_attribute('class')}")
            else:
                print("No potential pagination elements found")
                driver.save_screenshot(f"{screenshots_dir}/no_pagination.png")
                return
        
        # Look for next page button
        print("\nLooking for next page button...")
        next_button_clicked = False
        
        # Try to find the next page button using multiple approaches
        for selector in [
            ".next-page",
            ".next",
            "[aria-label='Next page']",
            "[class*='next']",
            "a.next",
            "button.next",
            "a[rel='next']",
            "//a[contains(@class, 'next')]",
            "//button[contains(@class, 'next')]",
            "//a[contains(text(), 'Next')]",
            "//a[contains(text(), 'შემდეგი')]",  # Georgian for "next"
            "//button[contains(text(), 'Next')]",
            "//button[contains(text(), 'შემდეგი')]"
        ]:
            try:
                elements = []
                # Different approach based on selector type
                if selector.startswith("//"):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            print(f"Found next button with selector: {selector}")
                            # Take screenshot before clicking
                            driver.save_screenshot(f"{screenshots_dir}/before_next_click.png")
                            # Scroll to the element
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            # Click the next button
                            element.click()
                            next_button_clicked = True
                            print("Clicked next page button")
                            break
                
                if next_button_clicked:
                    break
            except Exception as e:
                print(f"Error with next button selector {selector}: {str(e)}")
                continue
        
        if not next_button_clicked:
            print("Could not find or click next page button. Trying JavaScript pagination detection...")
            
            # Try clicking any "2" link that might represent page 2
            try:
                page_2_elements = driver.find_elements(By.XPATH, "//a[text()='2']")
                if page_2_elements:
                    for element in page_2_elements:
                        if element.is_displayed():
                            print("Found page 2 link")
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            element.click()
                            next_button_clicked = True
                            print("Clicked page 2 link")
                            break
            except Exception as e:
                print(f"Error finding page 2 link: {str(e)}")
            
            if not next_button_clicked:
                print("Could not find any pagination controls to interact with")
                driver.save_screenshot(f"{screenshots_dir}/pagination_failure.png")
                return
        
        # Take screenshot after clicking next
        time.sleep(2)  # Short wait for initial page change
        driver.save_screenshot(f"{screenshots_dir}/after_next_click.png")
        print("Saved screenshot after clicking next")
        
        # Wait for the page to update - look for loading indicators first
        print("\nWaiting for page update after pagination...")
        try:
            # Wait for any loading indicators to disappear
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, 
                ".loading, .spinner, .loader, [class*='loading'], [class*='loader']"))
            )
            print("Loading indicator disappeared")
        except TimeoutException:
            print("No loading indicator found or it didn't disappear")
        
        # Wait for products to change using our custom condition
        print("Waiting for product content to update...")
        products_changed = False
        
        try:
            WebDriverWait(driver, 15).until(lambda d: products_have_changed())
            products_changed = True
            print("Products have been dynamically updated!")
        except TimeoutException:
            print("Timeout waiting for products to update")
            driver.save_screenshot(f"{screenshots_dir}/timeout_no_update.png")
        
        if products_changed:
            # Take a screenshot after the update
            driver.save_screenshot(f"{screenshots_dir}/after_products_changed.png")
            print("Saved screenshot after products changed")
            
            # Get the updated products for comparison
            print("\nExtracting updated product data...")
            updated_products = driver.find_elements(By.CSS_SELECTOR, product_selector_used)
            
            # Extract data from updated products
            updated_product_data = []
            for i, product in enumerate(updated_products[:5]):
                try:
                    info = extract_product_info(product)
                    if info['title']:
                        updated_product_data.append(info)
                        print(f"Updated product {i+1}: {info['title']}")
                except Exception as e:
                    print(f"Error extracting updated product data: {str(e)}")
            
            # Compare initial and updated products
            print("\nComparing initial and updated products:")
            
            initial_titles = [p['title'] for p in initial_product_data if p['title']]
            updated_titles = [p['title'] for p in updated_product_data if p['title']]
            
            changed_count = sum(1 for title in updated_titles if title not in initial_titles)
            
            if changed_count > 0:
                print(f"Confirmed: {changed_count} out of {len(updated_titles)} products have changed after pagination")
                
                # Display which products have changed
                print("\nChanged products:")
                for title in updated_titles:
                    if title not in initial_titles:
                        print(f"- {title}")
            else:
                print("Products appear to be the same despite pagination")
        
        # Check if we have more pages to navigate
        print("\nChecking for additional pages...")
        page_links = []
        
        if pagination_element:
            # Look for page number links
            selectors = ["a.page-link", "a[class*='page']", "button[class*='page']", "a:not([class*='next']):not([class*='prev'])"]
            
            for selector in selectors:
                try:
                    links = pagination_element.find_elements(By.CSS_SELECTOR, selector)
                    if links:
                        page_links = links
                        break
                except:
                    continue
        
        if page_links:
            print(f"Found {len(page_links)} pagination links")
            
            # Extract page numbers
            page_numbers = []
            for link in page_links:
                try:
                    text = link.text.strip()
                    if text.isdigit():
                        page_numbers.append(int(text))
                except:
                    continue
            
            if page_numbers:
                max_page = max(page_numbers)
                print(f"Maximum page number found: {max_page}")
            else:
                print("Could not determine page numbers")
        else:
            print("No individual page links found")
        
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
    handle_dynamic_pagination() 