#!/usr/bin/env python3
"""
LAB8 Task 3: Cookie Management and Session Persistence
Print all cookies, modify them, test access, and save/load cookies for persistence.
"""

import requests
from bs4 import BeautifulSoup
import pickle
import json
import sys
from urllib.parse import urljoin
import os


def extract_csrf_token(session, login_url):
    """Extract CSRF token from the login page."""
    try:
        response = session.get(login_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        csrf_selectors = [
            'input[name="_token"]',
            'input[name="csrf_token"]',
            'input[name="authenticity_token"]',
            'meta[name="csrf-token"]',
            'meta[name="_token"]'
        ]
        
        for selector in csrf_selectors:
            csrf_element = soup.select_one(selector)
            if csrf_element:
                token = csrf_element.get('value') or csrf_element.get('content')
                if token:
                    field_name = csrf_element.get('name', 'csrf_token')
                    return token, field_name
        
        return None, None
    except Exception as e:
        print(f"Error extracting CSRF token: {e}")
        return None, None


def login_and_extract_cookies(login_url):
    """Login and extract all session cookies."""
    session = requests.Session()
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print("Step 1: Getting login page and extracting form data...")
        response = session.get(login_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        form = soup.find('form')
        
        if not form:
            print("❌ No form found")
            return None, None
        
        # Extract form details
        action = form.get('action', '')
        form_url = urljoin(login_url, action) if action else login_url
        
        # Get CSRF token if needed
        csrf_token, csrf_field_name = extract_csrf_token(session, login_url)
        
        # Find field names
        email_field = 'email'
        password_field = 'password'
        
        for input_field in form.find_all('input'):
            input_type = input_field.get('type', '').lower()
            input_name = input_field.get('name', '')
            
            if input_type in ['text', 'email'] or 'email' in input_name.lower():
                email_field = input_name
            elif input_type == 'password':
                password_field = input_name
        
        print(f"Form URL: {form_url}")
        print(f"Email field: {email_field}, Password field: {password_field}")
        
        print("\nStep 2: Submitting login form...")
        login_data = {
            email_field: 'admin@admin.com',
            password_field: 'password'
        }
        
        if csrf_token and csrf_field_name:
            login_data[csrf_field_name] = csrf_token
            print(f"Added CSRF token: {csrf_token[:20]}...")
        
        # Add hidden fields
        for hidden_input in form.find_all('input', type='hidden'):
            name = hidden_input.get('name')
            value = hidden_input.get('value', '')
            if name and name != csrf_field_name:
                login_data[name] = value
        
        response = session.post(form_url, data=login_data, allow_redirects=True)
        response.raise_for_status()
        
        print(f"Login response status: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # Check if login was successful
        if 'login' in response.url.lower():
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('form'):
                print("❌ Login failed - still on login page")
                error_div = soup.find('div', class_='alert-danger') or soup.find('div', class_='error')
                if error_div:
                    print(f"Error message: {error_div.get_text().strip()}")
                return None, None
        
        print("✅ Login successful!")
        
        return session, response
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, None


def print_all_cookies(session):
    """Print all cookies stored in the session."""
    print("\n🍪 All Session Cookies:")
    print("=" * 60)
    
    if not session.cookies:
        print("No cookies found in session.")
        return {}
    
    cookies_dict = {}
    for cookie in session.cookies:
        print(f"Name: {cookie.name}")
        print(f"Value: {cookie.value}")
        print(f"Domain: {cookie.domain}")
        print(f"Path: {cookie.path}")
        print(f"Secure: {cookie.secure}")
        print(f"HTTP Only: {getattr(cookie, 'has_nonstandard_attr', lambda x: False)('HttpOnly')}")
        print(f"Expires: {cookie.expires}")
        print("-" * 40)
        
        cookies_dict[cookie.name] = {
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'secure': cookie.secure,
            'expires': cookie.expires
        }
    
    return cookies_dict


def modify_cookie_and_test_access(session, products_url):
    """Modify a cookie value and test if access is still valid."""
    print("\n🔧 Testing Cookie Modification:")
    print("=" * 50)
    
    if not session.cookies:
        print("❌ No cookies to modify")
        return False
    
    # Find the first session-related cookie to modify
    session_cookie = None
    for cookie in session.cookies:
        if any(keyword in cookie.name.lower() for keyword in ['session', 'auth', 'token', 'login']):
            session_cookie = cookie
            break
    
    if not session_cookie:
        # Just pick the first cookie
        session_cookie = list(session.cookies)[0]
    
    print(f"Modifying cookie: {session_cookie.name}")
    print(f"Original value: {session_cookie.value}")
    
    # Save original value
    original_value = session_cookie.value
    
    # Modify the cookie value
    modified_value = original_value + "_modified"
    session.cookies.set(session_cookie.name, modified_value, 
                       domain=session_cookie.domain, path=session_cookie.path)
    
    print(f"Modified value: {modified_value}")
    
    # Test access to protected page
    print(f"\nTesting access to {products_url} with modified cookie...")
    try:
        response = session.get(products_url)
        print(f"Response status: {response.status_code}")
        
        # Check if we're redirected to login page
        if 'login' in response.url.lower():
            print("❌ Access denied - redirected to login page")
            print("Cookie modification invalidated the session!")
            return False
        else:
            print("✅ Access still granted with modified cookie")
            return True
            
    except Exception as e:
        print(f"❌ Error testing access: {e}")
        return False
    finally:
        # Restore original cookie value
        session.cookies.set(session_cookie.name, original_value,
                           domain=session_cookie.domain, path=session_cookie.path)
        print(f"Restored original cookie value: {original_value}")


def save_cookies_to_file(session, filename):
    """Save session cookies to a file."""
    print(f"\n💾 Saving cookies to {filename}...")
    
    try:
        # Save as pickle file (preserves cookie objects)
        with open(filename + '.pkl', 'wb') as f:
            pickle.dump(session.cookies, f)
        
        # Also save as JSON for human readability
        cookies_dict = {}
        for cookie in session.cookies:
            cookies_dict[cookie.name] = {
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'secure': cookie.secure,
                'expires': cookie.expires
            }
        
        with open(filename + '.json', 'w') as f:
            json.dump(cookies_dict, f, indent=2, default=str)
        
        print(f"✅ Cookies saved to {filename}.pkl and {filename}.json")
        return True
        
    except Exception as e:
        print(f"❌ Error saving cookies: {e}")
        return False


def load_cookies_from_file(filename):
    """Load cookies from a file and create a new session."""
    print(f"\n📁 Loading cookies from {filename}.pkl...")
    
    try:
        with open(filename + '.pkl', 'rb') as f:
            cookies = pickle.load(f)
        
        # Create new session and load cookies
        new_session = requests.Session()
        new_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Copy cookies to new session
        for cookie in cookies:
            new_session.cookies.set(cookie.name, cookie.value,
                                   domain=cookie.domain, path=cookie.path)
        
        print(f"✅ Loaded {len(cookies)} cookies into new session")
        return new_session
        
    except Exception as e:
        print(f"❌ Error loading cookies: {e}")
        return None


def test_cookie_persistence(products_url, cookies_filename):
    """Test accessing protected page using saved cookies in a new session."""
    print("\n🔄 Testing Cookie Persistence:")
    print("=" * 50)
    
    new_session = load_cookies_from_file(cookies_filename)
    if not new_session:
        return False
    
    try:
        print(f"Accessing {products_url} with loaded cookies...")
        response = new_session.get(products_url)
        print(f"Response status: {response.status_code}")
        
        if 'login' in response.url.lower():
            print("❌ Access denied - cookies expired or invalid")
            return False
        else:
            print("✅ Access granted with saved cookies!")
            
            # Try to extract some content to verify we're on the right page
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"Page title: {title.get_text().strip()}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing persistence: {e}")
        return False


def main():
    """Main function to run Task 3."""
    print("🚀 LAB8 Task 3: Cookie Management and Session Persistence")
    print("=" * 60)
    
    login_url = "https://www.scrapingcourse.com/login/csrf"
    products_url = "https://www.scrapingcourse.com/ecommerce"
    cookies_filename = "session_cookies"
    
    # Step 1: Login and get session
    session, login_response = login_and_extract_cookies(login_url)
    if not session:
        print("❌ Failed to login and establish session")
        sys.exit(1)
    
    # Step 2: Print all cookies
    cookies_dict = print_all_cookies(session)
    
    # Step 3: Modify cookie and test access
    modify_cookie_and_test_access(session, products_url)
    
    # Step 4: Save cookies to file
    save_success = save_cookies_to_file(session, cookies_filename)
    if not save_success:
        print("❌ Failed to save cookies")
        sys.exit(1)
    
    # Step 5: Test cookie persistence with new session
    persistence_success = test_cookie_persistence(products_url, cookies_filename)
    
    print("\n📊 Task 3 Summary:")
    print("=" * 40)
    print(f"✅ Login successful: Yes")
    print(f"✅ Cookies printed: {len(cookies_dict)} cookies")
    print(f"✅ Cookie modification tested: Yes")
    print(f"✅ Cookies saved: Yes")
    print(f"✅ Cookie persistence tested: {'Yes' if persistence_success else 'No'}")
    
    if persistence_success:
        print("\n🎉 All cookie management tasks completed successfully!")
    else:
        print("\n⚠️  Cookie persistence failed - cookies may have expired")


if __name__ == "__main__":
    main() 