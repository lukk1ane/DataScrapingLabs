from bs4 import BeautifulSoup
import requests

# Static HTML to parse
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

# Parsing the HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Task 1: Extract Page Title
title = soup.title.text
print("Page Title:", title)

# Task 2: Extract Main Heading and Tagline
main_heading = soup.find('h1').text
tagline = soup.find('p', class_='tagline').text
print("Main Heading:", main_heading)
print("Tagline:", tagline)

# Task 3: Extract Navigation Menu Items
nav_items = [li.text for li in soup.select('.nav-menu .menu-item')]
print("Navigation Items:", nav_items)

# Task 4 & 5: Extract and Store Product Table Data
table_rows = soup.select('#product-table tr')[1:]
products = []
for row in table_rows:
    cells = row.find_all('td')
    products.append({
        "Product": cells[0].text,
        "Price": cells[1].text,
        "Stock": cells[2].text
    })
print("Product Table:", products)

# Task 6: Extract Section Titles and Descriptions
sections = {
    h2.text:
    h2.find_next_sibling('p').text for h2 in soup.select('.sections h2')
}
print("Sections:", sections)

# Task 7: Extract Deeply Nested Elements
section_headings = [h2.text for h2 in soup.select('.sections h2')]
descriptions = [p.text for p in soup.select('.sections p')]
print("Section Headings:", section_headings)
print("Descriptions:", descriptions)

# Task 8: Extract Elements Using IDs
section_1_text = soup.find('h2', id='section-1').text
nav_home_text = soup.find('li', id='nav-home').text
print("Section 1:", section_1_text)
print("Nav Home:", nav_home_text)

# Task 9: Extract Specific Paragraphs
descriptions_text = [p.text for p in soup.find_all('p', class_='description')]
print("Paragraph Descriptions:", descriptions_text)

# Task 10: Retrieve and Format All Visible Text
visible_text = soup.get_text(separator=' ', strip=True)
print("Visible Text:", visible_text)

# Part 2: Scraping from quotes.toscrape.com
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract All Quotes and Their Authors
quotes = []
for q in soup.select('.quote'):
    text = q.find('span', class_='text').text
    author = q.find('small', class_='author').text
    quotes.append((text, author))
print("Quotes and Authors:", quotes)

# Extract "Next" Page Link
next_page = soup.select_one('.next a')
next_page_link = url + next_page['href'] if next_page else "No next page"
print("Next Page Link:", next_page_link)

# Extract Tags Associated with Quotes
tags = [tag.text for tag in soup.select('.tag')]
print("Tags:", tags)
