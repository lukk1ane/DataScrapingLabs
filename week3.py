from bs4 import BeautifulSoup
import requests

# Static HTML for parsing
task_html = """
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

soup = BeautifulSoup(task_html, 'html.parser')

# Task 1: Extract Page Title
title = soup.title.text
print("Page Title:", title)

# Task 2: Extract Main Heading and Tagline
main_heading = soup.find('h1').text
tagline = soup.find('p', class_='tagline').text
print("Main Heading:", main_heading)
print("Tagline:", tagline)

# Task 3: Extract Navigation Menu Items
nav_items = [item.text for item in soup.select('.nav-menu .menu-item')]
print("Navigation Menu:", nav_items)

# Task 4: Extract Product Table Data
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]  # Skip header
products = []
for row in rows:
    cols = row.find_all('td')
    products.append({"Product": cols[0].text, "Price": cols[1].text, "Stock": cols[2].text})
print("Product Table:", products)

# Task 6 & 7: Extract Section Titles and Descriptions
sections = {h2.text: h2.find_next_sibling('p').text for h2 in soup.select('.sections h2')}
print("Sections:", sections)

# Task 8: Extract Elements Using IDs
section1_text = soup.find('h2', id='section-1').text
nav_home_text = soup.find('li', id='nav-home').text
print("Section 1 Heading:", section1_text)
print("Navigation Home:", nav_home_text)

# Task 9: Extract Specific Paragraphs
descriptions = [p.text for p in soup.select('p.description')]
print("Descriptions:", descriptions)

# Task 10: Extract All Visible Text
visible_text = soup.get_text(separator=' ', strip=True)
print("Visible Text:", visible_text)

# ---- Web Scraping from Quotes Website ----
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all quotes and authors
quotes = [(quote.find('span', class_='text').text, quote.find('small', class_='author').text)
          for quote in soup.find_all('div', class_='quote')]
print("Quotes:", quotes)

# Extract "Next" page link
next_page = soup.select_one('li.next a')
next_page_url = url + next_page['href'] if next_page else None
print("Next Page URL:", next_page_url)

# Extract all quote tags
tags = [tag.text for tag in soup.select('.tag')]
print("Tags:", tags)
