from bs4 import BeautifulSoup


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

soup = BeautifulSoup(html_doc, 'html.parser')


print("Task 1: Extract Page Title")
title = soup.head.title.text
print(f"Page Title: {title}")


print("\nTask 2: Extract Main Heading and Tagline")
top_header = soup.find('div', id='top-header')
main_heading = top_header.h1.text
tagline = top_header.find('p', class_='tagline').text
print(f"Main Heading: {main_heading}")
print(f"Tagline: {tagline}")


print("\nTask 3: Extract Navigation Menu Items")
nav_menu = soup.find('ul', class_='nav-menu')
menu_items = nav_menu.find_all('li', class_='menu-item')
print("Menu Items:")
for item in menu_items:
    print(f"- {item.text}")


print("\nTask 4: Extract Product Table Data")
product_table = soup.find('table', id='product-table')
rows = product_table.find_all('tr')[1:]  
print("Product Table Data:")
for row in rows:
    cells = row.find_all('td')
    product = cells[0].text
    price = cells[1].text
    stock = cells[2].text
    print(f"Product: {product}, Price: {price}, Stock: {stock}")


print("\nTask 5: Store Table Data in a Dictionary")
table_data = []
for row in rows:
    cells = row.find_all('td')
    product_dict = {
        'Product': cells[0].text,
        'Price': cells[1].text,
        'Stock': cells[2].text
    }
    table_data.append(product_dict)
print("Table Data as List of Dictionaries:")
for item in table_data:
    print(item)


print("\nTask 6: Extract Section Titles and Descriptions")
sections_div = soup.find('div', class_='sections')
section_headings = sections_div.find_all('h2')
print("Section Titles and Descriptions:")
for heading in section_headings:
    title = heading.text
  
    description = heading.find_next('p', class_='description').text
    print(f"Title: {title}, Description: {description}")


print("\nTask 7: Extract Deeply Nested Elements")
sections_div = soup.find('div', class_='sections')
headings = sections_div.find_all('h2')
paragraphs = sections_div.find_all('p')
print("Deeply Nested Headings:")
for heading in headings:
    print(f"- {heading.text}")
print("Deeply Nested Paragraphs:")
for paragraph in paragraphs:
    print(f"- {paragraph.text}")


print("\nTask 8: Extract Elements Using IDs")
section1 = soup.find('h2', id='section-1').text
nav_home = soup.find('li', id='nav-home').text
print(f"Section 1 Text: {section1}")
print(f"Nav Home Text: {nav_home}")

print("\nTask 9: Extract Specific Paragraphs")
description_paragraphs = soup.find_all('p', class_='description')
print("Description Paragraphs:")
for paragraph in description_paragraphs:
    print(f"- {paragraph.text}")


print("\nFinal Task: All Visible Text")
visible_text = soup.get_text(separator='\n', strip=True)
print(visible_text)