from bs4 import BeautifulSoup
import requests

doc = """
<html>
<head><title>Complex Page</title></head>
<body>
<div id='top-header' class='header'>
<h1>Main Heading</h1>
<p class='tagline'>Welcome to the test page.
</p>
</div>
<div id='navigation'>
<ul class='nav-menu'>
<li id='nav-home' class='menu-item'>Home</li>
<li id='nav-about' class='menu-item'>About</li>
<li id='nav-contact' class='menu-item'>Contact</li>
</ul>
</div>
<div class='content'>
<table id='product-table'>
<tr><th>Product</th><th>Price</th><th>Stock</th></tr>
<tr><td>Book A</td><td>$10</td><td>In Stock</td></tr>
<tr><td>Book B</td><td>$15</td><td>Out of Stock</td></tr>
</table>
<div class='sections'>
<h2 id='section-1'>Section 1</h2>
<p class='description'>Details about section 1.
</p>
<h2 id='section-2'>Section 2</h2>
<p class='description'>Details about section 2.
</p>
</div>
</div>
</body>
</html>
"""

soup = BeautifulSoup(doc, "html.parser")

title = soup.title.text
print("Task 1 - Page Title:", title)

main_heading = soup.find("div", id="top-header").h1.text
tagline = soup.find("p", class_="tagline").text.strip()
print("Task 2 - Main Heading:", main_heading)
print("Task 2 - Tagline:", tagline)

menu_items = [item.text for item in soup.select("ul.nav-menu li.menu-item")]
print("Task 3 - Navigation Menu Items:", menu_items)

product_table = soup.find("table", id="product-table")
products_data = []
for row in product_table.find_all("tr")[1:]:  # Skip header row
    columns = row.find_all("td")
    product_name = columns[0].text
    price = columns[1].text
    stock = columns[2].text
    products_data.append((product_name, price, stock))
print("Task 4 - Product Table Data:")
for product in products_data:
    print(f"  Product: {product[0]}, Price: {product[1]}, Stock: {product[2]}")

product_dict_list = []
for row in product_table.find_all("tr")[1:]:  # Skip header row
    columns = row.find_all("td")
    product_dict = {
        "Product": columns[0].text,
        "Price": columns[1].text,
        "Stock": columns[2].text
    }
    product_dict_list.append(product_dict)
print("Task 5 - Product Dictionary List:", product_dict_list)

sections_div = soup.find("div", class_="sections")
section_data = {}
section_headings = sections_div.find_all("h2")
for heading in section_headings:
    section_title = heading.text
    description = heading.find_next("p", class_="description").text.strip()
    section_data[section_title] = description
print("Task 6 - Section Titles and Descriptions:", section_data)

section_headings = [heading.text for heading in sections_div.find_all("h2")]
section_paragraphs = [para.text.strip() for para in sections_div.find_all("p")]
print("Task 7 - Deeply Nested Headings:", section_headings)
print("Task 7 - Deeply Nested Paragraphs:", section_paragraphs)

section_1 = soup.find("h2", id="section-1").text
nav_home = soup.find("li", id="nav-home").text
print("Task 8 - Section 1 Heading:", section_1)
print("Task 8 - Nav Home Text:", nav_home)

description_paragraphs = [p.text.strip() for p in soup.find_all("p", class_="description")]
print("Task 9 - Description Paragraphs:", description_paragraphs)

visible_text = soup.get_text(separator=" ", strip=True)
print("All Visible Text:", visible_text)

print("\n--- Scraping quotes.toscrape.com ---")
url = 'http://quotes.toscrape.com'
response = requests.get(url)
quotes_soup = BeautifulSoup(response.text, "html.parser")

quotes = quotes_soup.find_all("div", class_="quote")
print("All Quotes and Their Authors:")
for quote in quotes:
    quote_text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    print(f'"{quote_text}" - {author}')

next_button = quotes_soup.find("li", class_="next")
if next_button:
    next_url = url + next_button.a["href"]
    print("The 'Next' Page Link:", next_url)
else:
    print("No 'Next' page link found")

tags = [tag.text for tag in quotes_soup.find_all("a", class_="tag")]
print("Tags found on the page:", tags)