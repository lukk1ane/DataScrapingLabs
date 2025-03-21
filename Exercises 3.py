
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

# Task 2: Extract Main Heading and Tagline
main_heading = soup.find('div', id='top-header').h1.string
tagline = soup.find('p', class_='tagline').string

# Task 3: Extract Navigation Menu Items
nav_items = [li.text for li in soup.select('ul.nav-menu li.menu-item')]

# Task 4: Extract Product Table Data
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]  # Skip header row
table_data = [[td.text for td in row.find_all('td')] for row in rows]

# Task 5: Store Table Data in Dictionary
products = [{'Product': row[0], 'Price': row[1], 'Stock': row[2]} for row in table_data]

# Task 6: Extract Section Titles and Descriptions
sections = soup.find('div', class_='sections')
section_titles = sections.find_all('h2')
section_descriptions = [h2.find_next_sibling('p').text for h2 in section_titles]
sections_data = list(zip([h2.text for h2 in section_titles], section_descriptions))

# Task 7: Extract Deeply Nested Elements
deep_titles = [h2.text for h2 in sections.find_all('h2')]
deep_paragraphs = [p.text for p in sections.find_all('p')]

# Task 8: Extract Elements Using IDs
section1_text = soup.find('h2', id='section-1').text
nav_home_text = soup.find('li', id='nav-home').text

# Task 9: Extract Specific Paragraphs
description_texts = [p.text for p in soup.find_all('p', class_='description')]

all_visible_text = soup.get_text(separator='\n', strip=True)

print("Page Title:", page_title)
print("Main Heading:", main_heading)
print("Tagline:", tagline)
print("Navigation Items:", nav_items)
print("Product Table Data:", table_data)
print("Product Dictionary:", products)
print("Sections (Titles and Descriptions):", sections_data)
print("Nested Section Titles:", deep_titles)
print("Nested Paragraphs:", deep_paragraphs)
print("Section 1 Title:", section1_text)
print("Nav Home Text:", nav_home_text)
print("Description Paragraphs:", description_texts)
print("\nAll Visible Text:\n", all_visible_text)

# --- Web Scraping from quotes.toscrape.com ---
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

quotes_divs = soup.find_all('div', class_='quote')
quotes = [(q.find('span', class_='text').text, q.find('small', class_='author').text) for q in quotes_divs]

print("\nQuotes and Authors:")
for quote, author in quotes:
    print(f"{quote} — {author}")

next_page = soup.find('li', class_='next')
next_page_link = url + next_page.a['href'] if next_page else None
print("\nNext Page URL:", next_page_link)

quote_tags = [tag.text for tag in soup.select('a.tag')]
print("\nTags on the Page:", quote_tags)
