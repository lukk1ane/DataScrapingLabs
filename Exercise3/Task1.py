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

# task 1
print("task 1")
title = soup.head.title.text
print(f"Page Title: {title}")
print("\n" + "-"*50 + "\n")

# task 2
print("task 2")
main_heading = soup.find('div', id='top-header').h1.text
tagline = soup.find('p', class_='tagline').text
print(f"Main Heading: {main_heading}")
print(f"Tagline: {tagline}")
print("\n" + "-"*50 + "\n")

# task 3
print("task 3")
nav_menu = soup.find('ul', class_='nav-menu')
menu_items = nav_menu.find_all('li', class_='menu-item')
print("Navigation Menu Items:")
for item in menu_items:
    print(f"- {item.text}")
print("\n" + "-"*50 + "\n")

# task 4
print("task 4")
product_table = soup.find('table', id='product-table')
rows = product_table.find_all('tr')[1:]  # Skip header row
print("Product Table Data:")
for row in rows:
    cells = row.find_all('td')
    product = cells[0].text
    price = cells[1].text
    stock = cells[2].text
    print(f"Product: {product}, Price: {price}, Stock: {stock}")
print("\n" + "-"*50 + "\n")

# task 5
print("task 5")
table_data = []
for row in rows:
    cells = row.find_all('td')
    product_dict = {
        "Product": cells[0].text,
        "Price": cells[1].text,
        "Stock": cells[2].text
    }
    table_data.append(product_dict)
print("Table Data as List of Dictionaries:")
for item in table_data:
    print(item)
print("\n" + "-"*50 + "\n")

# task 6
print("task 6")
sections_div = soup.find('div', class_='sections')
section_headings = sections_div.find_all('h2')
print("Section Titles and Descriptions:")
for heading in section_headings:
    title = heading.text
    # Find the paragraph that immediately follows this heading
    description = heading.find_next('p').text
    print(f"Title: {title}")
    print(f"Description: {description}")
    print()
print("-"*50 + "\n")

# task 7
print("task 7")
sections_div = soup.find('div', class_='sections')
nested_headings = sections_div.find_all('h2')
nested_paragraphs = sections_div.find_all('p')

print("Deeply Nested Headings:")
for heading in nested_headings:
    print(f"- {heading.text}")

print("\nDeeply Nested Paragraphs:")
for paragraph in nested_paragraphs:
    print(f"- {paragraph.text}")
print("\n" + "-"*50 + "\n")

# task 8
print("task 8")
section1_heading = soup.find('h2', id='section-1').text
nav_home = soup.find('li', id='nav-home').text
print(f"Section 1 Heading: {section1_heading}")
print(f"Nav Home Text: {nav_home}")
print("\n" + "-"*50 + "\n")

# task 9
print("task 9")
description_paragraphs = soup.find_all('p', class_='description')
print("Description Paragraphs:")
for paragraph in description_paragraphs:
    print(f"- {paragraph.text}")
print("\n" + "-"*50 + "\n")

# final task
print("final task")
visible_text = soup.get_text(separator='\n', strip=True).split('\n')
visible_text = [line for line in visible_text if line.strip()]  # Remove empty lines
print("All Visible Text:")
for line in visible_text:
    print(line)
