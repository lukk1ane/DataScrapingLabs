import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd


url = "https://books.toscrape.com/"
response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.content, "lxml")

main_container = soup.find("div", class_="col-sm-8 col-md-9")
if not main_container:
    print("Main container not found!")
    exit()

book_articles = main_container.find_all("article", class_="product_pod")

books_data_parent_child = []


print("Extracting data using parent-child relationships...")
for book in book_articles[:2]:  
   
    title_tag = book.find("h3").find("a")
    title = title_tag["title"] if title_tag else "N/A"


    price_tag = book.find("p", class_="price_color")
    price = price_tag.text.strip() if price_tag else "N/A"


    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag["class"][1] if rating_tag else "N/A" 


    books_data_parent_child.append({
        "title": title,
        "price": price,
        "rating": rating
    })
    
print("Data extracted using parent-child relationships:")
for book in books_data_parent_child:
    print(book)


books_data_sibling = []


print("\nExtracting data using sibling relationships...")
for book in book_articles[:2]:

    h3_tag = book.find("h3")
    title = h3_tag.find("a")["title"] if h3_tag else "N/A"


    product_price_div = h3_tag.find_next_sibling("div", class_="product_price")
    price_tag = product_price_div.find("p", class_="price_color") if product_price_div else None
    price = price_tag.text.strip() if price_tag else "N/A"

   
    books_data_sibling.append({
        "title": title,
        "price": price
    })


print("Data extracted using sibling relationships:")
for book in books_data_sibling:
    print(book)


tree = html.fromstring(response.content)

xpath_query = '//article[@class="product_pod"]'
book_elements = tree.xpath(xpath_query)


books_data_xpath = []


print("\nExtracting data using XPath...")
for book in book_elements[:2]:

    title = book.xpath('.//h3/a/@title')[0] if book.xpath('.//h3/a/@title') else "N/A"


    relative_url = book.xpath('.//h3/a/@href')[0] if book.xpath('.//h3/a/@href') else "N/A"
    full_url = f"https://books.toscrape.com/{relative_url}"


    books_data_xpath.append({
        "title": title,
        "url": full_url
    })


print("Data extracted using XPath:")
for book in books_data_xpath:
    print(book)

books_data_final = []

print("\nCombining and cleaning data...")
for book in book_articles[:2]:

    title_tag = book.find("h3").find("a")
    title = title_tag["title"] if title_tag else "N/A"

    price_tag = book.find("p", class_="price_color")
    price = price_tag.text.strip() if price_tag else "N/A"

    price_cleaned = float(price.replace("£", "")) if price != "N/A" else 0.0

    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag["class"][1] if rating_tag else "N/A"


    tree = html.fromstring(str(book))
    relative_url = tree.xpath('.//h3/a/@href')[0] if tree.xpath('.//h3/a/@href') else "N/A"
    full_url = f"https://books.toscrape.com/{relative_url}" if relative_url != "N/A" else "N/A"


    books_data_final.append({
        "title": title,
        "price": price_cleaned,
        "rating": rating,
        "url": full_url
    })


print("Final cleaned and organized data:")
for book in books_data_final:
    print(book)

df = pd.DataFrame(books_data_final)
df.to_csv("books_data.csv", index=False)
print("\nData saved to books_data.csv")