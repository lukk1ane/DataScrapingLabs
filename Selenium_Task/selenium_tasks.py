from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

# ─── CONFIGURE YOUR DRIVER ─────────────────────────────────────────────────────
CHROMEDRIVER_PATH = '/mnt/data/chromedriver'  # point to your chromedriver
service = Service(CHROMEDRIVER_PATH)

# ─── TASK 1: FILL & SUBMIT PRACTICE FORM ────────────────────────────────────────
def task1(driver):
    # 1. Open the registration form
    driver.get('https://demoqa.com/automation-practice-form')
    time.sleep(1)  # quick pause so page assets load

    # 2. Locate elements using a variety of selectors
    first_name = driver.find_element(By.ID, 'firstName')                    # fast, reliable
    last_name  = driver.find_element(By.CSS_SELECTOR, 'input#lastName')     # CSS selector example
    email      = driver.find_element(By.XPATH, '//input[@id="userEmail"]')  # XPath example
    # gender radios share name="gender" so pick the “Male” label by text
    driver.find_element(By.XPATH, '//label[text()="Male"]').click()
    phone      = driver.find_element(By.ID, 'userNumber')
    address    = driver.find_element(By.CSS_SELECTOR, 'textarea#currentAddress')

    # 3. Enter data
    first_name.send_keys('John')
    last_name.send_keys('Doe')
    email.send_keys('john.doe@example.com')
    phone.send_keys('5551234567')
    address.send_keys('123 Selenium St, Webcity')

    # 4. Submit form
    driver.find_element(By.ID, 'submit').click()

    # 5. (Optional) verify submission modal appeared
    try:
        modal = driver.find_element(By.ID, 'example-modal-sizes-title-lg')
        print('Form submitted:', modal.is_displayed())
    except:
        print('Submission modal not found')
    time.sleep(1)


# ─── TASK 2: SCRAPE BOOKS.TOSCRAPE.COM ─────────────────────────────────────────
def task2(driver):
    # 1. Maximize for consistency
    driver.maximize_window()
    driver.get('https://books.toscrape.com/')
    time.sleep(1)

    rows = []
    # 2. Grab each book container
    books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')
    for book in books:
        # title is in <h3><a title="...">
        title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')
        price = book.find_element(By.CSS_SELECTOR, '.price_color').text
        # star-rating classes are like "star-rating Three"
        star_class = book.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class')
        rating = star_class.split()[1]  # e.g. "Three"
        availability = book.find_element(By.CSS_SELECTOR, '.availability').text.strip()

        rows.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Availability': availability
        })

    # 3. Write all books to CSV
    with open('all_books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title','Price','Rating','Availability'])
        writer.writeheader()
        writer.writerows(rows)

    # 4. Filter only 5-star books and save separately
    five_star = [r for r in rows if r['Rating'] == 'Five']
    with open('5_star__books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title','Price','Rating','Availability'])
        writer.writeheader()
        writer.writerows(five_star)

    print(f"Extracted {len(rows)} books, {len(five_star)} of them are 5-star.")

# ─── EXTRAS: HEADLESS & CUSTOM WINDOW SIZE ──────────────────────────────────────
def create_headless_driver():
    opts = Options()
    opts.add_argument('--headless')            # run without opening a window
    opts.add_argument('--window-size=1024,768')# specify custom size
    return webdriver.Chrome(service=service, options=opts)

def create_custom_size_driver(width, height):
    opts = Options()
    opts.add_argument(f'--window-size={width},{height}')
    return webdriver.Chrome(service=service, options=opts)

# ─── MAIN FLOW ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # normal browser
    driver = webdriver.Chrome(service=service)
    try:
        task1(driver)
        task2(driver)
    finally:
        driver.quit()

    # example: run headless
    headless_driver = create_headless_driver()
    try:
        task2(headless_driver)  # you could run just task2 in headless
    finally:
        headless_driver.quit()
