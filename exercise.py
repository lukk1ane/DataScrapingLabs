import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://books.toscrape.com/"

# Send an HTTP GET request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all book title elements (inside <h3>)
books = soup.find_all("h3")

# Extract titles and corresponding prices
for book in books:
    title = book.a["title"]  # Extract book title
    price = book.find_parent("article").find("p", class_="price_color").text
    print(f"Title: {title} - Price: {price}")
