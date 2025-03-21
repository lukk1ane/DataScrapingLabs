from bs4 import BeautifulSoup
import requests

html_doc = """
<html>
<head><title>Complex Page</title></head>
<body>
<div id='top-header' class='header'>
<h1>Main Heading</h1>
<p class='tagline'>Welcome to the test page.</p>
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
<p class='description'>Details about section 1.</p>
<h2 id='section-2'>Section 2</h2>
<p class='description'>Details about section 2.</p>
</div>
</div>
</body>
</html>
"""

doc = BeautifulSoup(html_doc, "html.parser")

# task 1
title_tag = doc.find("title")
print(title_tag.text)

# task 2
main_heading = doc.find("div", id="top-header").find("h1")
print(main_heading.text)
tagline = doc.find("p", class_="tagline")
print(tagline.text)

# task 3
nav_menu = doc.find("ul", class_="nav-menu")
menu_items = nav_menu.find_all("li", class_="menu-item")
menu_items_text = [item.text for item in menu_items]
print(menu_items_text)


# task 4 and task 5
def construct_product(parts):
    return {"Product": parts[0].text, "Price": parts[1].text, "Stock": parts[2].text}


product_table = doc.find("table", id="product-table")
product_rows = product_table.find_all("tr")[1:]
products = [construct_product(row.find_all("td")) for row in product_rows]
print(products)

# task 6 and task 7
section = doc.find("div", class_="sections")
section_headings = section.find_all("h2")
section_descriptions = section.find_all("p", class_="description")
section_data = [{"title": section_headings[i].text, "desc": section_descriptions[i].text}
                for i in range(len(section_headings))]
print(section_data)

# task 8
print(doc.find("h2", id="section-1").text)
print(doc.find("li", id="nav-home").text)

# task 9
descriptions = doc.find_all("p", class_="description")
print([item.text for item in descriptions])

# task 10
URL = "http://quotes.toscrape.com"
res = requests.get(URL)
main_page = BeautifulSoup(res.text, "html.parser")
items = main_page.find_all("div", class_="quote")
quotes_data = [{"author": item.find("small", class_="author").text, "quote": item.find("span", class_="text").text}
               for item in items]
print(quotes_data)

# task 11
next_page_link = main_page.find("li", class_="next").find("a").get("href")
print(URL + next_page_link)

# task 12
tags = main_page.select(".tag")
print([tag.text for tag in tags])