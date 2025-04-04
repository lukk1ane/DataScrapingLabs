from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pprint
import csv

# Setup headless browser
options = Options()
# options.add_argument("--headless")  # Comment this line to see the browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Go to the dynamic page
driver.get("https://swoop.ge/category/15/kveba/")

# Wait for JavaScript to load items
time.sleep(5)  # You can increase if content doesn't fully load

# Get page source after JS render
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close browser
driver.quit()

# Extract all offer blocks
offer_blocks = soup.select('div.relative a.group')
offers = []

for a_tag in offer_blocks:
    title = a_tag.select_one('h4.text-primary_black-100-value')
    description = a_tag.select_one('div.text-primary_black-50-value')
    image_tag = a_tag.select_one('img')
    price_now = a_tag.select_one('h4.font-tbcx-bold')
    price_old = a_tag.select_one('h4.line-through')
    discount = a_tag.select_one('p.text-primary_green-10-value')
    sold = a_tag.select_one('div.text-primary_black-100-value.laptop\\:text-md')

    offers.append({
        'title': title.text.strip() if title else None,
        'description': description.text.strip() if description else None,
        'image': image_tag['src'] if image_tag else None,
        'price_now': price_now.text.strip() if price_now else None,
        'price_old': price_old.text.strip() if price_old else None,
        'discount': discount.text.strip() if discount else None,
        'sold': sold.text.strip() if sold else None,
        'link': 'https://swoop.ge' + a_tag['href'] if a_tag.has_attr('href') else None
    })

# Save results to CSV
csv_file_path = 'Results.csv'
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'description', 'image', 'price_now', 'price_old', 'discount', 'sold', 'link'])
    # Write header only if the file is empty
    if file.tell() == 0:
        writer.writeheader()
    writer.writerows(offers)
