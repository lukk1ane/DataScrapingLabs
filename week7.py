import requests
from bs4 import BeautifulSoup
import re

# Configuration
BASE_URL = "https://www.scrapingcourse.com"
LOGIN_URL = f"{BASE_URL}/login"
PROTECTED_URL = f"{BASE_URL}/products"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': LOGIN_URL
}


def get_actual_credentials():
    """Extract the current demo credentials from the server response"""
    try:
        session = requests.Session()
        response = session.get(LOGIN_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the error message containing current demo credentials
        error_div = soup.find(class_=re.compile('error|alert', re.I))
        if error_div:
            error_text = error_div.get_text(strip=True)
            if "Demo Credentials" in error_text:
                # Extract email and password from message
                email = re.search(r"Email:([^|]+)", error_text).group(1).strip()
                password = re.search(r"Password:([^\|]+)", error_text).group(1).strip()
                return {'email': email, 'password': password}

        return None
    except Exception as e:
        print(f"Error getting credentials: {e}")
        return None


def login(session: requests.Session) -> bool:
    """Perform login with dynamically obtained credentials"""
    try:
        # First get the current demo credentials from the page
        credentials = get_actual_credentials()
        if not credentials:
            print("Could not extract demo credentials from page")
            return False

        print(f"\nUsing server-provided demo credentials:")
        print(f"Email: {credentials['email']}")
        print(f"Password: {credentials['password']}")

        # Get CSRF token from cookies
        csrf_token = session.cookies.get('XSRF-TOKEN')
        if not csrf_token:
            print("No CSRF token found in cookies")
            return False

        # Prepare login data
        login_data = {
            '_token': csrf_token,
            'email': credentials['email'],
            'password': credentials['password']
        }

        # Submit login
        response = session.post(LOGIN_URL, data=login_data)

        # Check for successful login (should redirect from login page)
        if response.status_code == 200 and "login" not in response.url.lower():
            print("Login successful!")
            return True

        print("\nLogin failed. Possible reasons:")
        print("- Website structure may have changed")
        print("- The demo credentials might be temporarily unavailable")
        print("- The site might be blocking automated access")

        return False

    except Exception as e:
        print(f"\nLogin error: {e}")
        return False


def main():
    print("=== Scraping Course Demo ===")

    # Initialize session
    session = requests.Session()
    session.headers.update(HEADERS)

    # Test connection
    try:
        print("\nTesting connection...")
        response = session.get(BASE_URL, timeout=10)
        print(f"Connected to {BASE_URL} (Status: {response.status_code})")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Attempt login with dynamically obtained credentials
    if not login(session):
        print("\nPlease try the following:")
        print(f"1. Manually visit {LOGIN_URL} to check current demo credentials")
        print("2. Verify the login form structure hasn't changed")
        print("3. Try again later if the site is having issues")
        return

    # If login succeeded, access protected content
    print("\nAccessing protected content...")
    try:
        response = session.get(PROTECTED_URL)
        if response.status_code == 200:
            print("\nSuccessfully accessed protected content!")
            print("Page content sample:")
            print(response.text[:500])  # Show first 500 characters
        else:
            print(f"\nFailed to access protected content (Status: {response.status_code})")
    except Exception as e:
        print(f"\nError accessing protected content: {e}")


if __name__ == "__main__":
    main()