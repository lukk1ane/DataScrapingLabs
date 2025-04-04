import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)


if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

h3_tags = soup.find_all("h3")

for h3 in h3_tags:
    title = h3.find("a")["title"]
    
    parent_article = h3.parent
    
    price_tag = parent_article.find("p", class_="price_color")
    
    price = price_tag.text.strip()
    
    print(f"{title}, Price:{price}")
