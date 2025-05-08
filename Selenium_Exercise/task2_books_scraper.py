from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1200,800')
options.add_argument('--headless')

service = Service('./drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://books.toscrape.com/")

books = driver.find_elements(By.CLASS_NAME, "product_pod")

book_data = []

for book in books:
    title = book.find_element(By.TAG_NAME, "h3").text
    price = book.find_element(By.CLASS_NAME, "price_color").text
    availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
    stars = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]
    
    book_data.append({
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Stars": stars
    })

driver.quit()

df = pd.DataFrame(book_data)
df.to_csv("all_books.csv", index=False)

five_star_df = df[df["Stars"] == "Five"]
five_star_df.to_csv("5_star_books.csv", index=False)