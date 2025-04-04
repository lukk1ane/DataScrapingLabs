import requests
from bs4 import BeautifulSoup
import csv

# Target URL
url = "https://books.toscrape.com/"

# Send HTTP GET request
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find all product containers
books = soup.find_all("article", class_="product_pod")

# List to hold all data
data = []

for book in books:
    # Parent-child: h3 -> a (title is inside <a> tag which is child of <h3>)
    h3 = book.find("h3")
    a_tag = h3.find("a")
    title = a_tag['title']

    # XPath-like: find price using class selector
    price = book.find("p", class_="price_color").text.strip()

    # Sibling: a_tag is sibling to <p class="price_color">
    # Construct full URL for book detail page
    relative_url = a_tag['href']
    book_url = f"https://books.toscrape.com/catalogue/{relative_url.replace('../../../', '')}"

    # Descriptions are not available on the main page — leave blank or fetch from detail page if needed
    description = ""

    # Save book info
    data.append({
        "title": title,
        "price": price,
        "url": book_url,
        "description": description
    })

# Write to CSV
with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "price", "url", "description"])
    writer.writeheader()
    writer.writerows(data)

# Print the extracted data
for book in data:
    print(f"Title: {book['title']}")
    print(f"Price: {book['price']}")
    print(f"URL: {book['url']}")
    print(f"Description: {book['description']}\n")

print("Data has been saved to 'books.csv'")
