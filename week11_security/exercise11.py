from bs4 import BeautifulSoup
import requests, pickle



def login_and_handle_cookies():
    # Task 1 and 2
    login_url = "https://www.scrapingcourse.com/login/csrf"

    session = requests.Session()
    response = session.get(login_url)

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "_token"})
    if csrf_token:
        csrf_token = csrf_token["value"]
    else:
        print("CSRF token not found!")
        return

    payload = {
        "_token": csrf_token,
        "email": "admin@example.com",
        "password": "password"
    }

    response = session.post(login_url, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    parent = soup.find_all(class_="product-item")
    products = []

    for product in parent:
        products.append({
            "Name": product.find(class_="product-name").text,
            "Price": product.find(class_="product-price").text
        })

    print(products)

    # Task 3
    # View current cookies
    for cookie in session.cookies:
        print(cookie.name, ":", cookie.value)

    # save cookies
    with open("cookies.pkl", "wb") as f:
        pickle.dump(session.cookies, f)

    # Modify a cookie
    session.cookies.set(
        name="scrapingcoursecom_session",
        value="tampered_value",
        domain="www.scrapingcourse.com",
        path="/"
    )

    # Make a new request to test effect of tampering
    tamper_response = session.get(login_url)

    print("\n[After Modifying Session Cookie]")
    print("Logged in?", "Logout" in tamper_response.text)

    # Start a NEW session
    new_session = requests.Session()

    # Load cookies
    with open("cookies.pkl", "rb") as f:
        loaded_cookies = pickle.load(f)
        new_session.cookies.update(loaded_cookies)

    # Try to access protected content
    response = new_session.get("https://www.scrapingcourse.com/dashboard", headers={"User-Agent": "Mozilla/5.0"})

    print("\n[Access with Loaded Cookies in New Session]")
    print("Logged in?", "Logout" in response.text)

    if "Logout" in response.text:
        soup = BeautifulSoup(response.text, "html.parser")
        products = []
        for product in soup.find_all(class_="product-item"):
            products.append({
                "Name": product.find(class_="product-name").text,
                "Price": product.find(class_="product-price").text
            })
        print(products)
    else:
        print("Session is not authenticated.")



if __name__ == "__main__":
    login_and_handle_cookies()
