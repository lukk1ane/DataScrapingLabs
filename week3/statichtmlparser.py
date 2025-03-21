from bs4 import BeautifulSoup
import warnings
from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

html_doc = """
<!DOCTYPE html>
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

# Task 1
if soup.head and soup.head.title:
    title = soup.head.title.text
    print(f"Page Title: {title}")
else:
    print("Page title not found")

# Task 2
main_heading = soup.find('div', id='top-header').h1.text
tagline = soup.find('p', class_='tagline').text
print(f"Main Heading: {main_heading}")
print(f"Tagline: {tagline}")

# Task 3
nav_items = soup.find('ul', class_='nav-menu').find_all('li', class_='menu-item')
print("Navigation Menu Items:")
for item in nav_items:
    print(f"- {item.text}")

# Task 4 & 5
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]  
products = []

for row in rows:
    cells = row.find_all('td')
    product_dict = {
        'Product': cells[0].text,
        'Price': cells[1].text,
        'Stock': cells[2].text
    }
    products.append(product_dict)

print("Products:")
for product in products:
    print(product)

# Task 6 & 7
sections_div = soup.find('div', class_='sections')
section_headings = sections_div.find_all('h2')
section_paragraphs = sections_div.find_all('p', class_='description')

print("Sections:")
for i, (heading, paragraph) in enumerate(zip(section_headings, section_paragraphs)):
    print(f"Section {i+1}: {heading.text}")
    print(f"Description: {paragraph.text}")

# Task 8
section1_heading = soup.find('h2', id='section-1').text
nav_home = soup.find('li', id='nav-home').text
print(f"Section 1 Heading: {section1_heading}")
print(f"Nav Home Text: {nav_home}")

# Task 9
description_paragraphs = soup.find_all('p', class_='description')
print("Description Paragraphs:")
for p in description_paragraphs:
    print(f"- {p.text}")

visible_text = soup.get_text(separator='\n', strip=True)
print("All Visible Text:")
print(visible_text)
