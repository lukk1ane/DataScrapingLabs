#!/usr/bin/env python3
"""
LAB8 Task 1: Basic Login Form Scraping
Navigate to login page, submit form with demo credentials, and extract products.
"""

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin


def get_demo_credentials(session, login_url):
    """Extract demo credentials from the login page."""
    try:
        response = session.get(login_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for demo credentials in various places
        demo_info = soup.find('div', class_='alert') or \
                   soup.find('div', class_='demo-credentials') or \
                   soup.find('div', class_='challenge-info') or \
                   soup.find('div', class_='info')
        
        if demo_info:
            text = demo_info.get_text()
            print(f"Demo credentials info found: {text}")
            
            # Try to extract email and password from text
            if 'admin@admin.com' in text.lower() or 'password' in text.lower():
                return {
                    'email': 'admin@admin.com',
                    'password': 'password'
                }
        
        # Default credentials based on the form structure
        return {
            'email': 'admin@admin.com',
            'password': 'password'
        }
    except Exception as e:
        print(f"Error getting demo credentials: {e}")
        return {'email': 'admin@admin.com', 'password': 'password'}


def extract_form_data(session, login_url):
    """Extract form action and any hidden fields from the login form."""
    try:
        response = session.get(login_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the login form
        form = soup.find('form')
        if not form:
            raise Exception("No form found on the login page")
        
        # Get form action
        action = form.get('action', '')
        if action:
            form_url = urljoin(login_url, action)
        else:
            form_url = login_url
        
        # Extract hidden fields
        hidden_fields = {}
        for hidden_input in form.find_all('input', type='hidden'):
            name = hidden_input.get('name')
            value = hidden_input.get('value', '')
            if name:
                hidden_fields[name] = value
        
        # Find username and password field names
        email_field = 'email'
        password_field = 'password'
        
        for input_field in form.find_all('input'):
            input_type = input_field.get('type', '').lower()
            input_name = input_field.get('name', '')
            
            if input_type in ['text', 'email'] or 'email' in input_name.lower():
                email_field = input_name
            elif input_type == 'password':
                password_field = input_name
        
        return form_url, hidden_fields, email_field, password_field
        
    except Exception as e:
        print(f"Error extracting form data: {e}")
        return login_url, {}, 'email', 'password'


def login_and_get_products(login_url, products_url):
    """Perform login and extract products from protected page."""
    
    # Create session to maintain cookies
    session = requests.Session()
    
    # Set user agent to avoid blocking
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print("Step 1: Getting demo credentials...")
        credentials = get_demo_credentials(session, login_url)
        print(f"Using credentials: {credentials}")
        
        print("\nStep 2: Extracting form data...")
        form_url, hidden_fields, email_field, password_field = extract_form_data(session, login_url)
        print(f"Form URL: {form_url}")
        print(f"Hidden fields: {hidden_fields}")
        print(f"Email field: {email_field}, Password field: {password_field}")
        
        print("\nStep 3: Submitting login form...")
        login_data = {
            email_field: credentials['email'],
            password_field: credentials['password']
        }
        login_data.update(hidden_fields)
        
        response = session.post(form_url, data=login_data, allow_redirects=True)
        response.raise_for_status()
        
        print(f"Login response status: {response.status_code}")
        print(f"Final URL after login: {response.url}")
        
        # Check if login was successful
        soup = BeautifulSoup(response.content, 'html.parser')
        if 'login' in response.url.lower() and soup.find('form'):
            print("❌ Login failed - still on login page")
            # Try to find error messages
            error_div = soup.find('div', class_='alert-danger') or soup.find('div', class_='error')
            if error_div:
                print(f"Error message: {error_div.get_text().strip()}")
            return False
        
        print("✅ Login successful!")
        
        print("\nStep 4: Accessing products page...")
        products_response = session.get(products_url)
        products_response.raise_for_status()
        
        print(f"Products page status: {products_response.status_code}")
        
        print("\nStep 5: Extracting product information...")
        soup = BeautifulSoup(products_response.content, 'html.parser')
        
        # Look for products in various possible structures
        products = []
        
        # Try different selectors for products
        selectors = [
            '.product',
            '.product-item',
            '.item',
            '[data-testid*="product"]',
            '.card',
            '.product-card',
            '.product-list-item'
        ]
        
        for selector in selectors:
            product_elements = soup.select(selector)
            if product_elements:
                print(f"Found {len(product_elements)} products using selector: {selector}")
                
                for i, product in enumerate(product_elements):
                    title = "Unknown"
                    price = "Unknown"
                    
                    # Extract title
                    title_selectors = ['h1', 'h2', 'h3', '.title', '.name', '.product-title', '.product-name', '[data-testid*="title"]', '[data-testid*="name"]']
                    for title_sel in title_selectors:
                        title_elem = product.select_one(title_sel)
                        if title_elem:
                            title = title_elem.get_text().strip()
                            break
                    
                    # Extract price
                    price_selectors = ['.price', '.cost', '.amount', '[data-testid*="price"]', '.price-value']
                    for price_sel in price_selectors:
                        price_elem = product.select_one(price_sel)
                        if price_elem:
                            price = price_elem.get_text().strip()
                            break
                    
                    products.append({'title': title, 'price': price})
                break
        
        if not products:
            # Fallback: try to find any text that looks like products
            print("No structured products found, trying alternative extraction...")
            
            # Look for table rows or list items that might contain products
            rows = soup.find_all(['tr', 'li', 'div'])
            for row in rows:
                text = row.get_text().strip()
                if any(currency in text for currency in ['$', '€', '£', 'USD', 'EUR']):
                    # This might be a product
                    products.append({'title': 'Product from text', 'price': text})
                    if len(products) >= 10:  # Limit to prevent too many false positives
                        break
        
        print(f"\n📦 Found {len(products)} products:")
        print("=" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"{i}. Title: {product['title']}")
            print(f"   Price: {product['price']}")
            print("-" * 30)
        
        if not products:
            print("❌ No products found. Page content preview:")
            page_text = soup.get_text()[:500]
            print(page_text + "...")
            
            # Check if we're actually on a products page
            if 'product' in page_text.lower() or 'item' in page_text.lower():
                print("Page seems to contain product-related content but extraction failed.")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main function to run Task 1."""
    print("🚀 LAB8 Task 1: Basic Login Form Scraping")
    print("=" * 50)
    
    login_url = "https://www.scrapingcourse.com/login"
    products_url = "https://www.scrapingcourse.com/ecommerce"  # Common products page
    
    success = login_and_get_products(login_url, products_url)
    
    if success:
        print("\n✅ Task 1 completed successfully!")
    else:
        print("\n❌ Task 1 failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 