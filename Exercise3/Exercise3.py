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

#Task1:
title = soup.title.string
print("Page Title:", title)


#Task2:
main_heading = soup.find('div', id='top-header').h1.string
tagline = soup.find('div', id='top-header').p.string
print("Main Heading:", main_heading)
print("Tagline:", tagline)

#Task3:
nav_items = [li.string for li in soup.find('ul', class_='nav-menu').find_all('li', class_='menu-item')]
print("Navigation Menu Items:", nav_items)


#Task4:
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]  # Skip header row
products = []
for row in rows:
    cols = row.find_all('td')
    products.append({
        'Product': cols[0].string,
        'Price': cols[1].string,
        'Stock': cols[2].string
    })
print("Product Table Data:", products)

#Task5: so storing is already done in task4 


#Task6:
sections = soup.find('div', class_='sections')
section_titles = [h2.string for h2 in sections.find_all('h2')]
descriptions = [p.string for p in sections.find_all('p', class_='description')]
print("Section Titles:", section_titles)
print("Descriptions:", descriptions)

#Task7:
headings = [h2.string for h2 in soup.find('div', class_='sections').find_all('h2')]
paragraphs = [p.string for p in soup.find('div', class_='sections').find_all('p')]
print("Headings:", headings)
print("Paragraphs:", paragraphs)


#Task8:
section_1 = soup.find('h2', id='section-1').string
nav_home = soup.find('li', id='nav-home').string
print("Section 1:", section_1)
print("Nav Home:", nav_home)

#Task9:
description_paragraphs = [p.string for p in soup.find_all('p', class_='description')]
print("Description Paragraphs:", description_paragraphs)


#Final Retriving
visible_text = soup.get_text()
print("All Visible Text:", visible_text)