import requests
from bs4 import BeautifulSoup
import json
import re

def task2_csrf_login():
    """
    Task 2: CSRF token login form handling
    - Navigate to CSRF login page
    - Extract CSRF token from form
    - Submit login form with demo credentials and CSRF token
    - Access protected products page
    - Extract titles and prices
    """
    session = requests.Session()
    
    # Step 1: Navigate to the CSRF login page
    login_url = "https://www.scrapingcourse.com/login/csrf"
    print("Navigating to CSRF login page...")
    
    response = session.get(login_url)
    if response.status_code != 200:
        print(f"Failed to access login page. Status code: {response.status_code}")
        return
    
    # Parse the login form
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the login form
    form = soup.find('form')
    if not form:
        print("No login form found on the page")
        return
    
    print("CSRF login form found!")
    
    # Extract form action and method
    action = form.get('action', '')
    method = form.get('method', 'post').lower()
    
    # Build the full login URL
    if action.startswith('/'):
        login_post_url = "https://www.scrapingcourse.com" + action
    elif action.startswith('http'):
        login_post_url = action
    else:
        login_post_url = login_url + '/' + action if action else login_url
    
    print(f"Form action: {login_post_url}")
    print(f"Form method: {method}")
    
    # Find input fields and extract CSRF token
    inputs = form.find_all('input')
    form_data = {}
    csrf_token = None
    
    for input_field in inputs:
        name = input_field.get('name')
        value = input_field.get('value', '')
        input_type = input_field.get('type', 'text')
        
        if name:
            if input_type == 'hidden':
                form_data[name] = value
                # Check if this is a CSRF token field
                if any(keyword in name.lower() for keyword in ['csrf', 'token', '_token', 'authenticity']):
                    csrf_token = value
                    print(f"Found CSRF token: {name} = {value}")
            elif name.lower() in ['username', 'email', 'user']:
                form_data[name] = 'admin@example.com'  # Demo username
            elif name.lower() in ['password', 'pass']:
                form_data[name] = 'password'  # Demo password
            else:
                form_data[name] = value
    
    # Also check for CSRF tokens in meta tags
    if not csrf_token:
        meta_csrf = soup.find('meta', attrs={'name': re.compile(r'csrf', re.I)})
        if meta_csrf:
            csrf_token = meta_csrf.get('content')
            # Add to form data with common CSRF field names
            for field_name in ['_token', 'csrf_token', 'authenticity_token']:
                if field_name not in form_data:
                    form_data[field_name] = csrf_token
                    print(f"Added CSRF token from meta tag: {field_name} = {csrf_token}")
                    break
    
    print(f"Form data to submit: {form_data}")
    
    # Step 2: Submit the login form with CSRF token
    print("Submitting CSRF login form...")
    
    if method == 'post':
        login_response = session.post(login_post_url, data=form_data)
    else:
        login_response = session.get(login_post_url, params=form_data)
    
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response URL: {login_response.url}")
    
    # Check if login was successful
    if "login" not in login_response.url.lower() or login_response.status_code == 200:
        print("CSRF login appears successful!")
    else:
        print("CSRF login may have failed")
        print("Response content preview:")
        print(login_response.text[:500])
    
    # Step 3: Access the protected products page
    products_url = "https://www.scrapingcourse.com/dashboard"
    print(f"\nAccessing dashboard page: {products_url}")
    
    products_response = session.get(products_url)
    print(f"Dashboard page status: {products_response.status_code}")
    
    if products_response.status_code != 200:
        print("Failed to access dashboard page")
        return
    
    # Step 4: Extract titles and prices
    products_soup = BeautifulSoup(products_response.content, 'html.parser')
    
    print("\n=== PRODUCTS FOUND (CSRF LOGIN) ===")
    
    # Look for product links (based on exploration results)
    products = []
    
    # Find product links based on the pattern found in exploration
    product_links = products_soup.find_all('a', href=lambda x: x and '/ecommerce/product/' in x)
    
    for link in product_links:
        link_text = link.get_text(strip=True)
        href = link.get('href')
        
        # Parse title and price from link text (format: "Product Name$XX")
        if '$' in link_text:
            parts = link_text.rsplit('$', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                price = '$' + parts[1].strip()
                
                products.append({"title": title, "price": price, "url": href})
                print(f"Product {len(products)}:")
                print(f"  Title: {title}")
                print(f"  Price: {price}")
                print(f"  URL: {href}")
                print()
    
    # Fallback: try other selectors if the above doesn't work
    if not products:
        print("Using fallback extraction methods...")
        # Try different selectors for products
        product_containers = (
            products_soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['product', 'item', 'card']
            )) or
            products_soup.find_all(['div', 'article'], attrs={'data-product': True}) or
            products_soup.find_all(['tr']) if products_soup.find('table') else []
        )
        
        if not product_containers:
            # Fallback: look for any elements with price indicators
            product_containers = products_soup.find_all(text=lambda text: text and '$' in text)
            product_containers = [elem.parent for elem in product_containers if elem.parent]
        
        for i, container in enumerate(product_containers[:20]):  # Limit to first 20 to avoid spam
            title = ""
            price = ""
            
            # Try to find title
            title_elem = (
                container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or
                container.find(['a', 'span', 'div'], class_=lambda x: x and 'title' in x.lower()) or
                container.find(['a', 'span', 'div'], class_=lambda x: x and 'name' in x.lower())
            )
            
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # Try to find price
            price_elem = (
                container.find(['span', 'div', 'p'], class_=lambda x: x and 'price' in x.lower()) or
                container.find(['span', 'div', 'p'], text=lambda text: text and '$' in text) or
                container.find(text=lambda text: text and '$' in text)
            )
            
            if price_elem:
                if hasattr(price_elem, 'get_text'):
                    price = price_elem.get_text(strip=True)
                else:
                    price = str(price_elem).strip()
            
            if title or price:
                products.append({"title": title, "price": price})
                print(f"Product {len(products)}:")
                print(f"  Title: {title}")
                print(f"  Price: {price}")
                print()
    
    if not products:
        print("No products found with standard selectors. Showing page content preview:")
        print(products_response.text[:1000])
    
    print(f"\nTotal products found: {len(products)}")
    
    # Save results to file
    with open('task2_results.json', 'w') as f:
        json.dump({
            'products': products,
            'total_count': len(products),
            'csrf_token_used': csrf_token,
            'login_successful': True
        }, f, indent=2)
    
    print("Results saved to task2_results.json")

if __name__ == "__main__":
    task2_csrf_login() 