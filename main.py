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

# Task 1

page_title = soup.title.text
print("title text: ", page_title)

# Task 2

main_heading = soup.find('div', id='top-header').h1.text
tagline = soup.find('p', class_='tagline').text
print("main heading: ", main_heading)
print("tagline: ", tagline)

# Task 3

menu = soup.find('ul', class_='nav-menu')
menu_items = [li.text for li in menu.find_all('li', class_='menu-item')]
print("menu items: ", menu_items)

# Task 4

table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]

products = []

for row in rows:
    columns = row.find_all('td')
    product = columns[0].text.strip()
    price = columns[1].text.strip()
    stock = columns[2].text.strip()
    products.append({"product name":product, "price": price, "stock status": stock})

for p in products:
    print(p)


# Task 5
products_new = []

for row in rows:
    columns = row.find_all('td')
    product_data = {
        "product name": columns[0].text.strip(),
        "price": columns[1].text.strip(),
        "stock status": columns[2].text.strip()
    }
    products_new.append(product_data)

print(products_new)


# Task 6

section_div = soup.find('div', class_='sections')
section_titles = section_div.find_all('h2')

sections = []
for s in section_titles:
    description = s.find_next_sibling('p', class_='description')
    sections.append({"title": s.text.strip(), "description": description.text.strip()})

print(sections)


# Task 7

headings = [h2.text.strip() for h2 in section_div.find_all('h2')]
p_elements = [p.text.strip() for p in section_div.find_all('p')]

print("Headings: ", headings)
print("Paragraphs: ", p_elements)


# Task 8

section1 = section_div.find('h2', id='section-1').text.strip()
nav_home = soup.find('li', id='nav-home').text.strip()
print(section1)
print(nav_home)


# Task 9

desc_ps = [p.text.strip() for p in soup.find_all('p', class_='description')]
print(desc_ps)

visible_text = soup.get_text(separator=' ', strip=True)
print(visible_text)


# Last part

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup_new = BeautifulSoup(response.text, 'html.parser')

quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    print(f"Quote: {text}")
    print(f"Author: {author}")
    print('-' * 50)


next_button = soup.find('li', class_='next')
if next_button:
    next_page_url = next_button.find('a')['href']
    print(f"Next Page URL: {url}{next_page_url}")
else:
    print("No Next Page Found")


tags = soup.select('span.tag')
print("Tags associated with quotes:")
for tag in tags:
    print(tag.text)