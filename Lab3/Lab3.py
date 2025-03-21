import requests
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


#Task 1
print("Task 1")
title = soup.head.title.text
print(f"Page title: {title}\n")

#Task 2
print("Task 2")
main_heading = soup.find('div', id='top-header').h1.text
tagline = soup.find('p', class_='tagline').text
print(f"Main heading: {main_heading}")
print(f"Tagline: {tagline}\n")

#Task 3
print("Task 3")
nav_items = soup.find('ul', class_='nav-menu').find_all('li', class_='menu-item')
print("Navigation menu items:")
for item in nav_items:
    print(f"- {item.text}")
print()

#Task 4
print("Task 4")
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]
print("Product table data:")
for row in rows:
    cells = row.find_all('td')
    product = cells[0].text
    price = cells[1].text
    stock = cells[2].text
    print(f"Product: {product}, Price: {price}, Stock: {stock}")
print()

#Task 5
print("Task 5")
table_data = []
for row in rows:
    cells = row.find_all('td')
    product_dict = {
        "Product": cells[0].text,
        "Price": cells[1].text,
        "Stock": cells[2].text
    }
    table_data.append(product_dict)
print("Table data as a list of dictionaries:")
for item in table_data:
    print(item)
print()

#Task 6
print("Task 6")
section_div = soup.find('div', class_='sections')
section_h2 = section_div.find_all('h2')
print("Selection titles and description")
for selection in section_h2:
    title = selection.text
    description = selection.find_next('p', class_="description").text
    print(f"Title: {title}, Description: {description}")
print()

#Task 7
print("Task 7")
section_div = soup.find('div', class_='sections')
nested_heading = section_div.find_all('h2')
nested_paragraph = section_div.find_all('p')
print("Nested headings:")
for item in nested_heading:
    print(f"Heading: {item.text}")
print("Nested paragraphs:")
for paragraph in nested_paragraph:
    print(f"Paragraph: {paragraph.text}")

#Task 8
print("Task 8")
select_h2 = soup.find("h2", id="section-1").text
select_li = soup.find("li", id="nav-home").text
print(f"Select heading: {select_h2}")
print(f"Select list: {select_li}")
print()

#Task 9
print("Task 9")
descriptions = soup.find_all('p', class_="description")
print("Descriptions:")
for description in descriptions:
    print(f"Description: {description.text}")
print()

#Task 10
print("Task10")
formatedText = soup.get_text(separator='\n', strip=True)
print(f"Formated text: {formatedText}")



#Second part
print("Second Part")
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print("All Quotes and Their Authors")
quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    text = quote.find('span', class_="text").text
    author = quote.find('small', class_="author").text
    print(f"Quote: {text}")
    print(f"Author: {author}")
    print("-" * 50)
print()


print("\nThe 'Next' Page Link:")
next_page = soup.find('li', class_='next')
if next_page:
    next_url = url + next_page.a['href']
    print(f"Next page URL: {next_url}")
else:
    print("No next page found.")


print("All tags")
allTags = soup.find_all('a', class_='tag')
for tag in allTags:
    print(f"Tag: {tag.text}")