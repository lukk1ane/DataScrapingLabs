import requests
from bs4 import BeautifulSoup
import json
import pickle
import time
from urllib.parse import urljoin
import os

class ScrapingTasks:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.scrapingcourse.com"
    
    def check_response(self, response, context=""):
        """Helper method to check response status and content"""
        print(f"Response status for {context}: {response.status_code}")
        if response.status_code not in [200, 302]:
            print(f"Warning: Unexpected status code for {context}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response text (first 200 chars): {response.text[:200]}")
            return False
        return True
    
    def find_available_products_url(self):
        """Try to find the correct products URL by testing different possibilities"""
        possible_urls = [
            f"{self.base_url}/products",
            f"{self.base_url}/ecommerce",
            f"{self.base_url}/shop",
            f"{self.base_url}/catalog",
            f"{self.base_url}/items"
        ]
        
        for url in possible_urls:
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    print(f"Found working products URL: {url}")
                    return url
            except Exception as e:
                print(f"Error testing URL {url}: {e}")
        
        print("Could not find a working products URL")
        return None
    
    def task1_basic_login(self):
        """Task 1: Basic login form handling"""
        print("=== TASK 1: Basic Login ===")
        
        # Navigate to login page
        login_url = f"{self.base_url}/login"
        response = self.session.get(login_url)
        
        if not self.check_response(response, "login page"):
            return False
        
        # Parse the login form
        soup = BeautifulSoup(response.content, 'html.parser')
        login_form = soup.find('form')
        
        if not login_form:
            print("Login form not found")
            return False
        
        # Extract form action and method
        form_action = login_form.get('action', '')
        form_method = login_form.get('method', 'post').lower()
        
        # Build the full URL for form submission
        if form_action:
            submit_url = urljoin(login_url, form_action)
        else:
            submit_url = login_url
        
        # Find actual field names from the form
        username_field = (soup.find('input', {'type': 'text'}) or 
                         soup.find('input', {'type': 'email'}) or 
                         soup.find('input', {'name': 'email'}) or
                         soup.find('input', {'name': 'username'}))
        password_field = soup.find('input', {'type': 'password'})
        
        if not username_field or not password_field:
            print("Could not find username or password fields")
            return False
        
        # Prepare login data with actual field names
        login_data = {
            username_field.get('name', 'username'): 'admin',
            password_field.get('name', 'password'): 'admin'
        }
        
        print(f"Submitting login form to: {submit_url}")
        print(f"Login data: {login_data}")
        
        # Submit login form
        if form_method == 'post':
            login_response = self.session.post(submit_url, data=login_data)
        else:
            login_response = self.session.get(submit_url, params=login_data)
        
        if not self.check_response(login_response, "login submission"):
            return False
        
        print("Login appears successful")
        
        # Try to find and access products page
        products_url = self.find_available_products_url()
        if products_url:
            products_response = self.session.get(products_url)
            if products_response.status_code == 200:
                self.extract_products(products_response.content, "Basic Login")
                return True
            else:
                print(f"Failed to access products page: {products_response.status_code}")
        
        return False
    
    def task2_csrf_login(self):
        """Task 2: CSRF token login form handling"""
        print("\n=== TASK 2: CSRF Token Login ===")
        
        # Navigate to CSRF login page
        csrf_login_url = f"{self.base_url}/login/csrf"
        response = self.session.get(csrf_login_url)
        
        if not self.check_response(response, "CSRF login page"):
            return False
        
        # Parse the login form and extract CSRF token
        soup = BeautifulSoup(response.content, 'html.parser')
        login_form = soup.find('form')
        
        if not login_form:
            print("Login form not found")
            return False
        
        # Look for CSRF token in various common locations
        csrf_token = None
        csrf_field_name = None
        
        # Check for hidden input with CSRF token
        csrf_inputs = [
            soup.find('input', {'name': 'csrf_token'}),
            soup.find('input', {'name': '_token'}),
            soup.find('input', {'name': 'authenticity_token'}),
            soup.find('input', {'type': 'hidden'})
        ]
        
        for csrf_input in csrf_inputs:
            if csrf_input and csrf_input.get('value'):
                csrf_token = csrf_input.get('value')
                csrf_field_name = csrf_input.get('name')
                break
        
        # Check for CSRF token in meta tags if not found in inputs
        if not csrf_token:
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                csrf_token = csrf_meta.get('content')
                csrf_field_name = 'csrf_token'
        
        print(f"CSRF Token found: {csrf_token}")
        print(f"CSRF Field name: {csrf_field_name}")
        
        # Extract form action
        form_action = login_form.get('action', '')
        submit_url = urljoin(csrf_login_url, form_action) if form_action else csrf_login_url
        
        # Find actual field names from the form
        username_field = (soup.find('input', {'type': 'text'}) or 
                         soup.find('input', {'type': 'email'}) or 
                         soup.find('input', {'name': 'email'}) or
                         soup.find('input', {'name': 'username'}))
        password_field = soup.find('input', {'type': 'password'})
        
        if not username_field or not password_field:
            print("Could not find username or password fields")
            return False
        
        # Prepare login data with actual field names
        login_data = {
            username_field.get('name', 'username'): 'admin',
            password_field.get('name', 'password'): 'admin'
        }
        
        # Add CSRF token if found
        if csrf_token and csrf_field_name:
            login_data[csrf_field_name] = csrf_token
        
        print(f"Submitting CSRF login form to: {submit_url}")
        print(f"Login data: {login_data}")
        
        # Submit login form
        login_response = self.session.post(submit_url, data=login_data)
        
        if not self.check_response(login_response, "CSRF login submission"):
            return False
        
        print("CSRF Login appears successful")
        
        # Try to find and access products page
        products_url = self.find_available_products_url()
        if products_url:
            products_response = self.session.get(products_url)
            if products_response.status_code == 200:
                self.extract_products(products_response.content, "CSRF Login")
                return True
            else:
                print(f"Failed to access products page: {products_response.status_code}")
        
        return False
    
    def task3_cookie_management(self):
        """Task 3: Cookie management and manipulation"""
        print("\n=== TASK 3: Cookie Management ===")
        
        # First, ensure we're logged in (using CSRF method)
        if not self.task2_csrf_login():
            print("Could not establish authenticated session for cookie management")
            return
        
        # Print all cookies
        print("\n--- Current Session Cookies ---")
        for cookie in self.session.cookies:
            print(f"Name: {cookie.name}, Value: {cookie.value[:50]}{'...' if len(cookie.value) > 50 else ''}")
            print(f"  Domain: {cookie.domain}, Path: {cookie.path}")
        
        # Save cookies to files
        try:
            with open('session_cookies.pkl', 'wb') as f:
                pickle.dump(self.session.cookies, f)
            print("\nCookies saved to 'session_cookies.pkl'")
            
            # Also save cookies as JSON for readability
            cookies_dict = {}
            for cookie in self.session.cookies:
                cookies_dict[cookie.name] = {
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path
                }
            
            with open('session_cookies.json', 'w') as f:
                json.dump(cookies_dict, f, indent=2)
            print("Cookies also saved as JSON to 'session_cookies.json'")
            
        except Exception as e:
            print(f"Error saving cookies: {e}")
        
        # Modify a cookie value
        print("\n--- Modifying Cookie Value ---")
        if self.session.cookies:
            # Find a session-related cookie to modify
            session_cookie = None
            for cookie in self.session.cookies:
                if any(keyword in cookie.name.lower() for keyword in ['session', 'auth', 'login']):
                    session_cookie = cookie
                    break
            
            if not session_cookie:
                # If no session cookie found, modify the first cookie
                session_cookie = list(self.session.cookies)[0]
            
            original_value = session_cookie.value
            print(f"Original cookie '{session_cookie.name}': {original_value[:50]}{'...' if len(original_value) > 50 else ''}")
            
            # Modify the cookie value
            self.session.cookies.set(session_cookie.name, 'modified_invalid_value')
            print(f"Modified cookie '{session_cookie.name}': modified_invalid_value")
            
            # Try to access protected page with modified cookie
            products_url = self.find_available_products_url()
            if products_url:
                test_response = self.session.get(products_url)
                
                if test_response.status_code == 200:
                    print("Still able to access protected page with modified cookie")
                else:
                    print(f"Access denied with modified cookie. Status: {test_response.status_code}")
        
        # Demonstrate loading cookies in a new session
        print("\n--- Loading Cookies in New Session ---")
        if os.path.exists('session_cookies.pkl'):
            try:
                new_session = requests.Session()
                new_session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                })
                
                # Load cookies from file
                with open('session_cookies.pkl', 'rb') as f:
                    saved_cookies = pickle.load(f)
                
                # Set cookies in new session
                new_session.cookies.update(saved_cookies)
                
                print("Cookies loaded in new session")
                
                # Try to access products page without logging in
                products_url = self.find_available_products_url()
                if products_url:
                    # Use the new session to test
                    temp_session = self.session
                    self.session = new_session
                    
                    products_url = self.find_available_products_url()
                    if products_url:
                        new_response = new_session.get(products_url)
                        
                        if new_response.status_code == 200:
                            print("Successfully accessed products page using saved cookies")
                            self.extract_products(new_response.content, "Saved Cookies")
                        else:
                            print(f"Failed to access products page with saved cookies. Status: {new_response.status_code}")
                    
                    # Restore original session
                    self.session = temp_session
                    
            except Exception as e:
                print(f"Error loading cookies: {e}")
        else:
            print("Cookie file not found")
    
    def extract_products(self, html_content, context=""):
        """Extract product titles and prices from the products page"""
        print(f"\n--- Extracting Products ({context}) ---")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for common product container patterns
        products = []
        
        # Try different selectors for products
        selectors = [
            '.product', '.item', '.card', 'article',
            '[class*="product"]', '[class*="item"]', '[class*="card"]'
        ]
        
        product_containers = []
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                product_containers = containers
                print(f"Found {len(containers)} containers using selector: {selector}")
                break
        
        if not product_containers:
            # Look for any elements that might contain product info
            product_containers = soup.find_all(['div', 'li', 'article'])
            print(f"Fallback: Found {len(product_containers)} potential containers")
        
        for container in product_containers:
            title = None
            price = None
            
            # Look for title
            title_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.name', '[class*="title"]', '[class*="name"]']
            for selector in title_selectors:
                title_elem = container.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    break
            
            # Look for price
            price_selectors = ['.price', '[class*="price"]', '[class*="cost"]']
            for selector in price_selectors:
                price_elem = container.select_one(selector)
                if price_elem:
                    price = price_elem.get_text().strip()
                    break
            
            # If no price found with selectors, look for text containing currency symbols
            if not price:
                price_text = container.get_text()
                if any(symbol in price_text for symbol in ['$', '€', '£', '¥']):
                    # Extract price using regex or simple string manipulation
                    import re
                    price_match = re.search(r'[\$€£¥]\d+\.?\d*', price_text)
                    if price_match:
                        price = price_match.group()
            
            if title or price:
                products.append({'title': title, 'price': price})
        
        # If no products found, try a different approach
        if not products:
            print("No products found with standard selectors. Trying alternative approach...")
            
            # Look for any text that might indicate products
            all_text = soup.get_text()
            if 'product' in all_text.lower() or '$' in all_text:
                print("Page appears to contain product-related content:")
                print(all_text[:300] + "..." if len(all_text) > 300 else all_text)
            else:
                print("Page does not appear to contain product information")
                print("Page title:", soup.find('title').get_text() if soup.find('title') else 'No title found')
        else:
            print(f"Found {len(products)} products:")
            for i, product in enumerate(products[:10], 1):  # Show first 10 products
                print(f"{i}. Title: {product['title']}, Price: {product['price']}")
            
            if len(products) > 10:
                print(f"... and {len(products) - 10} more products")
    
    def run_all_tasks(self):
        """Run all scraping tasks"""
        print("Starting Web Scraping Tasks...")
        print("=" * 50)
        
        try:
            success1 = self.task1_basic_login()
            
            # Create new session for task 2 to avoid interference
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            success2 = self.task2_csrf_login()
            self.task3_cookie_management()
            
            print(f"\n=== TASK SUMMARY ===")
            print(f"Task 1 (Basic Login): {'✓ Success' if success1 else '✗ Failed'}")
            print(f"Task 2 (CSRF Login): {'✓ Success' if success2 else '✗ Failed'}")
            print(f"Task 3 (Cookie Management): Completed")
            
        except Exception as e:
            print(f"Error during scraping tasks: {e}")
            import traceback
            traceback.print_exc()

# Improved Session Manager with better error handling
class SessionManager:
    """Manages multiple user sessions with monitoring and rotation"""
    
    def __init__(self):
        self.sessions = {}
        self.credentials = {}
        self.session_status = {}
        self.base_url = "https://www.scrapingcourse.com"
    
    def add_account(self, account_id, username, password):
        """Add a new account to manage"""
        self.credentials[account_id] = {'username': username, 'password': password}
        self.sessions[account_id] = requests.Session()
        self.session_status[account_id] = {'logged_in': False, 'last_check': None, 'error': None}
        
        # Set user agent
        self.sessions[account_id].headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def login_account(self, account_id, login_url=None):
        """Login a specific account"""
        if account_id not in self.sessions:
            print(f"Account {account_id} not found")
            return False
        
        if login_url is None:
            login_url = f"{self.base_url}/login/csrf"  # Use CSRF login by default
        
        session = self.sessions[account_id]
        creds = self.credentials[account_id]
        
        try:
            # Get login page
            response = session.get(login_url)
            if response.status_code != 200:
                error_msg = f"Failed to access login page: {response.status_code}"
                print(error_msg)
                self.session_status[account_id]['error'] = error_msg
                return False
            
            # Parse form and handle CSRF if needed
            soup = BeautifulSoup(response.content, 'html.parser')
            login_form = soup.find('form')
            
            if not login_form:
                error_msg = "Login form not found"
                print(error_msg)
                self.session_status[account_id]['error'] = error_msg
                return False
            
            # Find actual field names
            username_field = (soup.find('input', {'type': 'text'}) or 
                             soup.find('input', {'type': 'email'}) or 
                             soup.find('input', {'name': 'email'}) or
                             soup.find('input', {'name': 'username'}))
            password_field = soup.find('input', {'type': 'password'})
            
            if not username_field or not password_field:
                error_msg = "Could not find username or password fields"
                print(error_msg)
                self.session_status[account_id]['error'] = error_msg
                return False
            
            # Prepare login data
            login_data = {
                username_field.get('name', 'username'): creds['username'],
                password_field.get('name', 'password'): creds['password']
            }
            
            # Handle CSRF token
            csrf_inputs = [
                soup.find('input', {'name': 'csrf_token'}),
                soup.find('input', {'name': '_token'}),
                soup.find('input', {'name': 'authenticity_token'}),
                soup.find('input', {'type': 'hidden'})
            ]
            
            for csrf_input in csrf_inputs:
                if csrf_input and csrf_input.get('value'):
                    login_data[csrf_input.get('name')] = csrf_input.get('value')
                    break
            
            # Submit login
            form_action = login_form.get('action', '')
            submit_url = urljoin(login_url, form_action) if form_action else login_url
            
            login_response = session.post(submit_url, data=login_data)
            
            # Check if login successful
            if login_response.status_code in [200, 302]:
                self.session_status[account_id]['logged_in'] = True
                self.session_status[account_id]['last_check'] = time.time()
                self.session_status[account_id]['error'] = None
                print(f"Successfully logged in account {account_id}")
                return True
            else:
                error_msg = f"Login failed - Status: {login_response.status_code}"
                print(error_msg)
                self.session_status[account_id]['error'] = error_msg
                return False
                
        except Exception as e:
            error_msg = f"Error logging in: {e}"
            print(error_msg)
            self.session_status[account_id]['error'] = error_msg
            return False
    
    def check_session_validity(self, account_id):
        """Check if a session is still valid"""
        if account_id not in self.sessions:
            return False
        
        session = self.sessions[account_id]
        
        # Try multiple test URLs
        test_urls = [
            f"{self.base_url}/products",
            f"{self.base_url}/ecommerce",
            f"{self.base_url}/shop"
        ]
        
        for test_url in test_urls:
            try:
                response = session.get(test_url)
                if response.status_code == 200:
                    self.session_status[account_id]['logged_in'] = True
                    self.session_status[account_id]['last_check'] = time.time()
                    self.session_status[account_id]['error'] = None
                    return True
            except Exception as e:
                continue
        
        # If all URLs failed
        self.session_status[account_id]['logged_in'] = False
        self.session_status[account_id]['last_check'] = time.time()
        self.session_status[account_id]['error'] = "Session validation failed"
        return False
    
    def rotate_session(self):
        """Get the next available session"""
        valid_sessions = [aid for aid, status in self.session_status.items() 
                         if status['logged_in']]
        
        if not valid_sessions:
            print("No valid sessions available")
            return None, None
        
        # Simple round-robin rotation
        if not hasattr(self, '_rotation_index'):
            self._rotation_index = 0
        
        account_id = valid_sessions[self._rotation_index % len(valid_sessions)]
        self._rotation_index += 1
        
        return account_id, self.sessions[account_id]
    
    def monitor_sessions(self):
        """Monitor all sessions and report status"""
        print("\n=== Session Status Report ===")
        for account_id, status in self.session_status.items():
            last_check = status['last_check']
            last_check_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_check)) if last_check else 'Never'
            
            status_icon = '✓' if status['logged_in'] else '✗'
            status_text = 'Active' if status['logged_in'] else 'Inactive'
            
            print(f"Account {account_id}: {status_icon} {status_text} (Last checked: {last_check_str})")
            
            if status['error']:
                print(f"  Error: {status['error']}")
            
            # Alert if session is invalid
            if not status['logged_in']:
                print(f"  ⚠️  ALERT: Session {account_id} is invalidated!")
    
    def login_all_accounts(self):
        """Login all registered accounts"""
        print("Logging in all accounts...")
        success_count = 0
        for account_id in self.credentials:
            if self.login_account(account_id):
                success_count += 1
        
        print(f"Successfully logged in {success_count}/{len(self.credentials)} accounts")
        return success_count
    
    def demo_session_management(self):
        """Demonstrate session management capabilities"""
        print("=== SESSION MANAGER DEMO ===")
        
        # Add multiple demo accounts
        self.add_account('user1', 'admin', 'admin')
        self.add_account('user2', 'admin', 'admin')  # Same creds for demo
        self.add_account('user3', 'admin', 'admin')
        
        # Login all accounts
        success_count = self.login_all_accounts()
        
        # Monitor sessions
        self.monitor_sessions()
        
        # Only demonstrate rotation if we have valid sessions
        if success_count > 0:
            print("\n--- Session Rotation Demo ---")
            for i in range(min(5, success_count * 2)):  # Don't try more than we have
                result = self.rotate_session()
                if result[0] is not None:
                    account_id, session = result
                    print(f"Using session: {account_id}")
                    
                    # Test the session with a simple request
                    try:
                        response = session.get(f"{self.base_url}/login")
                        print(f"  Response status: {response.status_code}")
                    except Exception as e:
                        print(f"  Error testing session: {e}")
                else:
                    print("No valid sessions available for rotation")
                    break
        else:
            print("\n--- Session Rotation Demo ---")
            print("Skipping rotation demo - no valid sessions available")
        
        # Check all session validity
        print("\n--- Checking Session Validity ---")
        for account_id in self.credentials:
            is_valid = self.check_session_validity(account_id)
            print(f"Account {account_id}: {'Valid' if is_valid else 'Invalid'}")
        
        # Final status report
        self.monitor_sessions()

if __name__ == "__main__":
    # Run main tasks
    scraper = ScrapingTasks()
    scraper.run_all_tasks()
    
    print("\n" + "="*50)
    
    # Run bonus session manager demo
    print("Running Bonus Session Manager Demo...")
    manager = SessionManager()
    manager.demo_session_management()