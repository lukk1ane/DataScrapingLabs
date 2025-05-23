import requests
from bs4 import BeautifulSoup

# Function for Task 1: Login and scrape product information
def task_1():
    login_url = "https://www.scrapingcourse.com/login"
    products_url = "https://www.scrapingcourse.com/products"

    # Provided credentials for the demo
    login_data = {
        "username": "demo",
        "password": "demo"
    }

    # Create a session to handle cookies
    session = requests.Session()

    # Step 1: Post login request
    response = session.post(login_url, data=login_data)

    # Step 2: Check if login is successful by inspecting the response
    if response.ok:
        print("Login successful. Accessing products page...")

        # Step 3: Get the protected products page
        product_page = session.get(products_url)

        # Step 4: Parse the products page and extract titles and prices
        soup = BeautifulSoup(product_page.content, "html.parser")
        products = soup.find_all("div", class_="product-item")

        for product in products:
            title = product.find("h2").get_text(strip=True)
            price = product.find("span", class_="price").get_text(strip=True)
            print(f"Product Title: {title}, Price: {price}")
    else:
        print("Login failed!")

# Function for Task 2: Handle CSRF token and login
def task_2():
    login_url = "https://www.scrapingcourse.com/login/csrf"
    products_url = "https://www.scrapingcourse.com/products"

    # Create a session to handle cookies
    session = requests.Session()

    # Step 1: Get the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    # Step 2: Prepare login data with CSRF token
    login_data = {
        "username": "demo",
        "password": "demo",
        "csrf_token": csrf_token
    }

    # Step 3: Submit login request with CSRF token
    login_response = session.post(login_url, data=login_data)

    # Step 4: Check if login is successful
    if login_response.ok:
        print("Login successful. Accessing products page...")

        # Step 5: Get the protected products page
        product_page = session.get(products_url)

        # Step 6: Parse and extract products information
        soup = BeautifulSoup(product_page.content, "html.parser")
        products = soup.find_all("div", class_="product-item")

        for product in products:
            title = product.find("h2").get_text(strip=True)
            price = product.find("span", class_="price").get_text(strip=True)
            print(f"Product Title: {title}, Price: {price}")
    else:
        print("Login failed!")

# Function for Task 3: Handling and modifying cookies
def task_3():
    login_url = "https://www.scrapingcourse.com/login/csrf"
    products_url = "https://www.scrapingcourse.com/products"

    # Create a session to handle cookies
    session = requests.Session()

    # Step 1: Get the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    # Step 2: Prepare login data with CSRF token
    login_data = {
        "username": "demo",
        "password": "demo",
        "csrf_token": csrf_token
    }

    # Step 3: Submit login request
    login_response = session.post(login_url, data=login_data)

    if login_response.ok:
        print("Login successful. Accessing products page...")

        # Step 4: Get the protected products page
        product_page = session.get(products_url)

        # Step 5: Print all cookies stored in the session
        print("Cookies after login:")
        print(session.cookies.get_dict())

        # Step 6: Modify a cookie value (example: session cookie)
        session.cookies.set("session", "modified_session_value")

        # Step 7: Attempt to access the protected page with modified cookies
        modified_page = session.get(products_url)

        if modified_page.ok:
            print("Page accessed with modified cookie!")
        else:
            print("Failed to access page with modified cookie.")

        # Step 8: Save cookies to a file
        with open("cookies.txt", "w") as f:
            f.write(str(session.cookies.get_dict()))

        # Step 9: Load cookies from the file in a new session
        session2 = requests.Session()
        with open("cookies.txt", "r") as f:
            cookies = eval(f.read())  # Convert string back to dictionary
            session2.cookies.update(cookies)

        # Step 10: Try to access the products page without logging in again
        session2.get(products_url)
        print("Accessed the products page with loaded cookies.")
    else:
        print("Login failed!")

# Main function to run the tasks
def main():
    task_1()
    task_2()
    task_3()

if __name__ == "__main__":
    main()
