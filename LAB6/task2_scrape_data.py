#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import os

def scrape_product_data():
    # Initialize Chrome driver with options for better performance
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    # Create a screenshots directory for debugging
    screenshots_dir = "LAB6/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    # Create a list to store the scraped data
    all_products = []
    
    try:
        # Open the website
        driver.get("https://swoop.ge/")
        print("Opened swoop.ge")
        time.sleep(5)  # Give the page more time to fully load
        
        # Take a screenshot of the homepage
        driver.save_screenshot(f"{screenshots_dir}/homepage.png")
        print("Saved homepage screenshot")
        
        # Try to find and capture the full HTML structure for debugging
        try:
            html = driver.page_source
            with open(f"{screenshots_dir}/page_source.html", "w", encoding="utf-8") as f:
                f.write(html[:10000])  # Save first 10000 chars to avoid huge files
            print("Saved partial page source for debugging")
        except Exception as e:
            print(f"Error saving page source: {str(e)}")
        
        # Try to navigate to a product category using multiple approaches
        print("Attempting to navigate to a product category...")
        
        # First attempt: Try direct navigation to category page
        driver.get("https://swoop.ge/category/340/sporti-/sacurao-auzi/")
        print("Directly navigated to electronics category")
        time.sleep(5)  # Wait longer for page to load
        
        # Take a screenshot of the category page
        driver.save_screenshot(f"{screenshots_dir}/category_page.png")
        print("Saved category page screenshot")
        
        # Wait for page content to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            print("Main content loaded")
        except TimeoutException:
            print("Timed out waiting for main content")
        
        # Use JavaScript to find products on the page
        print("Using JavaScript to find product elements...")
        js_products = driver.execute_script("""
            // Try to find elements that look like product cards
            const productElements = [];
            
            // Look for elements with certain keywords in class names
            document.querySelectorAll('[class*="product"], [class*="card"], article, .item').forEach(el => {
                // Check if it contains both text and images (typical for product cards)
                if ((el.textContent && el.textContent.trim()) && 
                    (el.querySelector('img') || el.querySelector('[class*="image"]'))) {
                    productElements.push(el);
                }
            });
            
            return productElements;
        """)
        
        if js_products and len(js_products) > 0:
            print(f"Found {len(js_products)} products using JavaScript")
            
            # Extract product data using JavaScript for better reliability
            all_products_data = driver.execute_script("""
                const products = arguments[0];
                const data = [];
                
                products.forEach(product => {
                    // Find title element using various selectors
                    let title = null;
                    for (const selector of ['.title', '[class*="title"]', 'h2', 'h3', 'h4', '[class*="name"]']) {
                        const titleEl = product.querySelector(selector);
                        if (titleEl && titleEl.textContent.trim()) {
                            title = titleEl.textContent.trim();
                            break;
                        }
                    }
                    
                    // Find price element using various selectors
                    let price = null;
                    for (const selector of ['.price', '[class*="price"]', '[class*="cost"]']) {
                        const priceEl = product.querySelector(selector);
                        if (priceEl && priceEl.textContent.trim()) {
                            price = priceEl.textContent.trim();
                            break;
                        }
                    }
                    
                    if (title || price) {
                        data.push({
                            title: title || 'Unknown Title',
                            price: price || 'Unknown Price'
                        });
                    }
                });
                
                return data;
            """, js_products)
            
            if all_products_data and len(all_products_data) > 0:
                print(f"Successfully extracted data for {len(all_products_data)} products using JavaScript")
                
                # Add page number to the first page data
                for product in all_products_data:
                    product['page'] = 1
                    all_products.append(product)
                
                # Display the first 3 products
                for i, product in enumerate(all_products_data[:3]):
                    print(f"Product {i+1}: {product['title']} - {product['price']}")
            else:
                print("JavaScript extraction returned no product data")
        else:
            print("JavaScript detection found no products")
        
        # If JavaScript approach failed, try traditional Selenium approach
        if not all_products:
            print("\nTrying traditional Selenium approach...")
            # Find products with a variety of possible selectors
            products_found = False
            product_selector_used = None
            
            for selector in [
                ".product-card", 
                ".card", 
                "[class*='product']", 
                "article",
                ".item", 
                "div[class*='card']",
                # More generic selectors
                "div.grid > div",
                "ul > li",
                "div.container div.row > div"
            ]:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        print(f"Found {len(elements)} potential product elements with selector: {selector}")
                        # Validate these look like products
                        valid_products = []
                        for elem in elements:
                            # Check if it contains both text and potentially an image
                            if elem.text and (len(elem.text.strip()) > 10):
                                valid_products.append(elem)
                        
                        if valid_products:
                            products_found = True
                            product_selector_used = selector
                            print(f"Validated {len(valid_products)} elements as likely products")
                            break
                except Exception as e:
                    print(f"Error with selector {selector}: {str(e)}")
                    continue
            
            if products_found:
                # Extract data from the first page
                products = driver.find_elements(By.CSS_SELECTOR, product_selector_used)
                print(f"Found {len(products)} products on page 1")
                
                # Function to extract product information from the provided HTML structure
                def extract_product_info(product):
                    info = {
                        'title': 'Unknown',
                        'price': 'Unknown',
                        'original_price': 'Unknown',
                        'discount': 'Unknown',
                        'sold': 'Unknown',
                        'image_url': 'Unknown',
                        'link': 'Unknown'
                    }
                    
                    try:
                        # Extract title - using the class structure from your HTML
                        title_elements = product.find_elements(By.CSS_SELECTOR, ".text-primary_black-100-value.text-md.leading-5.font-tbcx-medium")
                        if title_elements:
                            info['title'] = title_elements[0].text.strip()
                        
                        # Extract price
                        price_elements = product.find_elements(By.CSS_SELECTOR, ".text-primary_black-100-value.text-2md.leading-5.font-tbcx-bold")
                        if price_elements:
                            info['price'] = price_elements[0].text.strip()
                        
                        # Extract original price
                        original_price_elements = product.find_elements(By.CSS_SELECTOR, ".text-md.leading-5.font-tbcx-regular.line-through")
                        if original_price_elements:
                            info['original_price'] = original_price_elements[0].text.strip()
                        
                        # Extract discount
                        discount_elements = product.find_elements(By.CSS_SELECTOR, ".text-md.leading-5.font-tbcx-bold.text-primary_green-10-value")
                        if discount_elements:
                            info['discount'] = discount_elements[0].text.strip()
                        
                        # Extract sold count - look for the text containing "გაყიდულია"
                        sold_elements = product.find_elements(By.XPATH, ".//*[contains(text(), 'გაყიდულია')]")
                        if sold_elements:
                            info['sold'] = sold_elements[0].text.strip()
                        
                        # Extract image URL
                        image_elements = product.find_elements(By.CSS_SELECTOR, "img.w-full.object-cover")
                        if image_elements:
                            info['image_url'] = image_elements[0].get_attribute('src')
                        
                        # Extract link - find the a tag that is a parent or ancestor of this element
                        link_elements = product.find_elements(By.XPATH, ".//ancestor::a | .//a")
                        if link_elements:
                            info['link'] = link_elements[0].get_attribute('href')
                        
                    except Exception as e:
                        print(f"Error extracting product info: {str(e)}")
                    
                    return info
                
                # Extract data from all products on first page
                for product in products:
                    try:
                        info = extract_product_info(product)
                        all_products.append(info)
                    except Exception as e:
                        print(f"Error extracting product data: {str(e)}")
                
                # Display the first 3 products
                for i, product in enumerate(all_products[:3]):
                    print(f"Product {i+1}: {product['title']} - {product['price']}")
            else:
                print("Could not find product elements with standard selectors")
        
        # Try to navigate to multiple pages (if we found products on first page)
        if all_products:
            # Try to find pagination elements
            pagination_found = False
            
            for selector in [
                ".pagination", 
                ".pager", 
                "nav[aria-label*='page']", 
                "[class*='pagination']",
                "ul.page-numbers"
            ]:
                try:
                    pagination = driver.find_elements(By.CSS_SELECTOR, selector)
                    if pagination:
                        pagination_found = True
                        print(f"Found pagination with selector: {selector}")
                        break
                except:
                    continue
            
            if pagination_found:
                print("Found pagination controls. Attempting to navigate to additional pages...")
                
                # Scrape 2 more pages (3 total including the first page)
                for page in range(2, 4):
                    # Try to click the next page button
                    next_clicked = False
                    
                    for selector in [
                        ".pagination .next", 
                        ".next-page", 
                        "[class*='pagination'] [class*='next']",
                        "a[aria-label='Next page']",
                        "//a[contains(@class, 'next')]",
                        "//button[contains(@class, 'next')]",
                        "a[rel='next']",
                        f"a[href*='page={page}']",
                        f"//a[text()='{page}']"
                    ]:
                        try:
                            elements = []
                            if selector.startswith("//"):
                                elements = driver.find_elements(By.XPATH, selector)
                            else:
                                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            
                            for element in elements:
                                if element.is_displayed() and element.is_enabled():
                                    print(f"Found navigation element with selector: {selector}")
                                    driver.save_screenshot(f"{screenshots_dir}/before_page{page}.png")
                                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                    time.sleep(1)
                                    element.click()
                                    next_clicked = True
                                    print(f"Clicked to navigate to page {page}")
                                    time.sleep(5)  # Wait longer for page to load
                                    driver.save_screenshot(f"{screenshots_dir}/after_page{page}.png")
                                    break
                            
                            if next_clicked:
                                break
                        except Exception as e:
                            print(f"Error with selector {selector}: {str(e)}")
                            continue
                    
                    if not next_clicked:
                        print(f"Could not navigate to page {page}")
                        break
                    
                    # Wait for page to load
                    time.sleep(3)
                    
                    # Extract data from this page using the appropriate method
                    if 'js_products' in locals() and js_products:
                        # Use JavaScript approach if it worked before
                        js_products = driver.execute_script("""
                            const productElements = [];
                            document.querySelectorAll('[class*="product"], [class*="card"], article, .item').forEach(el => {
                                if ((el.textContent && el.textContent.trim()) && 
                                    (el.querySelector('img') || el.querySelector('[class*="image"]'))) {
                                    productElements.push(el);
                                }
                            });
                            return productElements;
                        """)
                        
                        if js_products and len(js_products) > 0:
                            page_products_data = driver.execute_script("""
                                const products = arguments[0];
                                const data = [];
                                
                                products.forEach(product => {
                                    let title = null;
                                    for (const selector of ['.title', '[class*="title"]', 'h2', 'h3', 'h4', '[class*="name"]']) {
                                        const titleEl = product.querySelector(selector);
                                        if (titleEl && titleEl.textContent.trim()) {
                                            title = titleEl.textContent.trim();
                                            break;
                                        }
                                    }
                                    
                                    let price = null;
                                    for (const selector of ['.price', '[class*="price"]', '[class*="cost"]']) {
                                        const priceEl = product.querySelector(selector);
                                        if (priceEl && priceEl.textContent.trim()) {
                                            price = priceEl.textContent.trim();
                                            break;
                                        }
                                    }
                                    
                                    if (title || price) {
                                        data.push({
                                            title: title || 'Unknown Title',
                                            price: price || 'Unknown Price'
                                        });
                                    }
                                });
                                
                                return data;
                            """, js_products)
                            
                            if page_products_data:
                                print(f"Extracted {len(page_products_data)} products from page {page}")
                                
                                # Add page number to the data
                                for product in page_products_data:
                                    product['page'] = page
                                    all_products.append(product)
                        else:
                            print(f"JavaScript found no products on page {page}")
                    
                    elif product_selector_used:
                        # Use Selenium approach if that worked before
                        products = driver.find_elements(By.CSS_SELECTOR, product_selector_used)
                        if products:
                            print(f"Found {len(products)} products on page {page}")
                            
                            page_products = []
                            for product in products:
                                try:
                                    info = extract_product_info(product)
                                    info['page'] = page
                                    all_products.append(info)
                                    page_products.append(info)
                                except Exception as e:
                                    print(f"Error extracting product data: {str(e)}")
                            
                            print(f"Extracted data for {len(page_products)} products from page {page}")
                        else:
                            print(f"No products found on page {page}")
            else:
                print("No pagination controls found. Only scraped the first page.")
        
        # Convert the collected data to a DataFrame and display it
        if all_products:
            df = pd.DataFrame(all_products)
            print("\nScraped Product Data (first 5 rows):")
            print(df.head())
            print(f"Total products scraped: {len(all_products)}")
            
            # Save data to CSV
            csv_path = "LAB6/scraped_products.csv"
            df.to_csv(csv_path, index=False)
            print(f"Data saved to {csv_path}")
        else:
            print("No products were scraped")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Take a screenshot to help debug the issue
        try:
            driver.save_screenshot(f"{screenshots_dir}/error.png")
            print("Screenshot saved to LAB6/screenshots/error.png")
        except:
            print("Could not save screenshot")
        
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    scrape_product_data() 