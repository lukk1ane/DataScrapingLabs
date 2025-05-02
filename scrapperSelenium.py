from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
# Task1
driver = webdriver.Chrome()

driver.get("https://demoqa.com/automation-practice-form")
# required_elements = driver.find_elements(By.CSS_SELECTOR, "[required]")
f_name = driver.find_element(By.ID, "firstName").send_keys("saba")
l = driver.find_element(By.ID, "lastName").send_keys("danelia")
label = driver.find_element(By.XPATH, "//label[normalize-space(text())='Other']").click()
mob = driver.find_element(By.ID, "userNumber").send_keys("5556667717")

submit = driver.find_element(By.CSS_SELECTOR,"button[type='submit']").submit()
time.sleep(10)
driver.quit()


# Task 2


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def mode(mode):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if mode == "h":
        options.add_argument("--headless=new")
    elif mode == "w":
        width = 1024
        height = 1024
        options.add_argument(f'--window-size={width},{height}')
    else:
        options.add_argument("--start-maximized")
    return options

# change mode function parameter
""" 'w' - for windowed mode, 'h' - for headless mode, '' - for maximized """
options  = mode("")
driver = webdriver.Chrome(options=options)
driver.get("https://books.toscrape.com/")
time.sleep(10)
books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
book_data = []

for book in books:
    title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
    price = book.find_element(By.CSS_SELECTOR, ".price_color").text
    availability = book.find_element(By.CSS_SELECTOR, ".availability").text.strip()
    star_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
    star_rating = star_class.split()[-1]

    book_data.append({
        "Title": title,
        "Price": price,
        "Star Rating": star_rating,
        "Availability": availability
    })

save_to_csv(book_data, "all_books.csv")

        # Filter only 5-star books
five_star_books = [book for book in book_data if book["Star Rating"].lower() == "five"]
save_to_csv(five_star_books, "5_star_books.csv")


driver.quit()