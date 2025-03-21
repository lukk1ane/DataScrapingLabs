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

soup = BeautifulSoup(html_doc, 'html.parser')

# Task 1: Extract Page Title
page_title = soup.title.string
print("Page Title:", page_title)

# Task 2: Extract Main Heading and Tagline
main_heading = soup.find('div', id='top-header').h1.string
tagline = soup.find('p', class_='tagline').string
print("Main Heading:", main_heading)
print("Tagline:", tagline)

# Task 3: Extract Navigation Menu Items
nav_items = [li.string for li in soup.find('ul', class_='nav-menu').find_all('li', class_='menu-item')]
print("Navigation Menu Items:", nav_items)

# Task 4: Extract Product Table Data
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]  # Skip the header row
products = []
for row in rows:
    cols = row.find_all('td')
    product = {
        'Product': cols[0].string,
        'Price': cols[1].string,
        'Stock': cols[2].string
    }
    products.append(product)
print("Products:", products)

# Task 5: Store Table Data in a Dictionary
product_dicts = [{'Product': row.find_all('td')[0].string, 'Price': row.find_all('td')[1].string, 'Stock': row.find_all('td')[2].string} for row in rows]
print("Product Dictionaries:", product_dicts)

# Task 6: Extract Section Titles and Descriptions
sections = soup.find('div', class_='sections')
section_titles = [h2.string for h2 in sections.find_all('h2')]
section_descriptions = [p.string for p in sections.find_all('p', class_='description')]
print("Section Titles:", section_titles)
print("Section Descriptions:", section_descriptions)

# Task 7: Extract Deeply Nested Elements
nested_headings = [h2.string for h2 in sections.find_all('h2')]
nested_paragraphs = [p.string for p in sections.find_all('p')]
print("Nested Headings:", nested_headings)
print("Nested Paragraphs:", nested_paragraphs)

# Task 8: Extract Elements Using IDs
section_1_text = soup.find('h2', id='section-1').string
nav_home_text = soup.find('li', id='nav-home').string
print("Section 1 Text:", section_1_text)
print("Nav Home Text:", nav_home_text)

# Task 9: Extract Specific Paragraphs
description_paragraphs = [p.string for p in soup.find_all('p', class_='description')]
print("Description Paragraphs:", description_paragraphs)

# Retrieve and format all visible text from the HTML document
visible_text = soup.get_text(separator=' ', strip=True)
print("Visible Text:", visible_text)

# Second part: Scraping data from http://quotes.toscrape.com
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all quotes and authors
quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    text = quote.find('span', class_='text').string
    author = quote.find('small', class_='author').string
    print(f"Quote: {text} - Author: {author}")

# Extract the link to the "Next" page
next_page = soup.find('li', class_='next')
if next_page:
    next_page_url = next_page.find('a')['href']
    print("Next Page URL:", url + next_page_url)

# Extract all tags associated with the quotes
tags = [tag.string for tag in soup.select('.tag')]
print("Tags:", tags)