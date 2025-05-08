from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
from bs4 import BeautifulSoup



def task1():
    email = "your_email_or_phone"
    password = "your_password"

    options = Options()
    options.add_argument("--headless=new")  # Use non-headless if CAPTCHA shows up
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://swoop.ge/")

    try:
        # Click login button via JavaScript
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[3]/button/p"))
        )
        driver.execute_script("arguments[0].click();", login_button)

        # Wait for login form to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email")))

        # Enter credentials
        email_input = driver.find_element(By.ID, "Email")
        password_input = driver.find_element(By.ID, "Password")

        email_input.send_keys(email)
        password_input.send_keys(password)

        # Submit the form (simulate Enter or use the submit button if needed)
        password_input.submit()

        time.sleep(3)
        print("Login attempt completed.")
    except Exception as e:
        print("Login failed:", e)
    finally:
        driver.quit()


def task2():
    base_url = "https://swoop.ge/category/24/dasveneba/"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    for page in range(1, 6):  # Pages 1 to 5
        url = f"{base_url}?page={page}" if page > 1 else base_url
        print(f"\n Scraping page {page}: {url}")
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        h2_tag = soup.find("h2")
        product_grid = h2_tag.find_next_sibling("div", class_="grid") if h2_tag else None

        if not product_grid:
            print("Product grid not found on this page.")
            continue

        products = product_grid.find_all("div", class_="relative", recursive=False)
        print(f"Found {len(products)} products on page {page}:\n")

        for product in products:
            product_page = product.find("a")

            outer_divs = product_page.find_all("div", recursive=False) if product_page else []
            name_and_price_div = outer_divs[1].find_all("div", recursive=False) if len(outer_divs) > 1 else []

            name_div = name_and_price_div[0] if len(name_and_price_div) > 0 else None
            product_name = name_div.find("h4").text.strip() if name_div and name_div.find("h4") else None
            place_name = name_div.find("div").text.strip() if name_div and name_div.find("div") else None

            print("Name:", product_name)
            print("Place:", place_name)
            print("-" * 40)

    driver.quit()


def task3():
    url = "https://swoop.ge/category/24/dasveneba/"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    try:
        # Wait until the checkbox is clickable
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "checkbox-მდებარეობა-0")))
        driver.execute_script("arguments[0].click();", checkbox)

        print("✅ Filter checkbox clicked successfully.")
    except Exception as e:
        print(f"❌ Failed to click checkbox: {e}")

    driver.quit()


def task4():
    url = "https://swoop.ge"

    # Setup headless browser
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait until at least one product image is visible
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
        )
    except Exception as e:
        print("Images did not load in time.")
        driver.quit()
        return

    images = driver.find_elements(By.TAG_NAME, "img")
    print(f"Found {len(images)} images. Attempting to capture 5 valid ones...\n")

    os.makedirs("screenshots", exist_ok=True)

    index = 0
    success_count = 0

    while success_count < 5 and index < len(images):
        img = images[index]

        is_loaded = driver.execute_script(
            "return arguments[0].complete && "
            "typeof arguments[0].naturalWidth != 'undefined' && "
            "arguments[0].naturalWidth > 0", img)

        if is_loaded:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", img)
                time.sleep(1)  # wait until its rendered
                if img.size['width'] > 0 and img.size['height'] > 0:
                    img.screenshot(f"screenshots/image_{success_count + 1}.png")
                    print(f"Image {index + 1} loaded and saved.")
                    success_count += 1
                else:
                    print(f"Image {index + 1} has 0 width/height, skipping.")
            except Exception as e:
                print(f"Error capturing image {index + 1}: {e}")
        else:
            print(f"Image {index + 1} not fully loaded, skipping.")

        index += 1

    driver.quit()



if __name__ == '__main__':
    # task1()
    # task2()
    # task3()
    task4()
