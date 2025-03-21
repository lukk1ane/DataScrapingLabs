import requests
from bs4 import BeautifulSoup

html_doc = """"
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
title_text = soup.find('title').get_text()
# print(title_text)

# Task 2
h1_text = soup.find('div', id='top-header').find('h1').get_text()
# print(h1_text)

# Task 3
# nav_items = soup.find('div', id='navigation').find_all('li')
# for item in nav_items:
#     print(item.get_text())
    
# Task 4 - 5
product_table = soup.find('table', id='product-table')
rows = product_table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    if(len(cols) == 0):
        continue
    dict = {'Product': cols[0].get_text(), 'Price': cols[1].get_text(), 'Stock': cols[2].get_text()}
    data.append(dict)
    # for col in cols:
    #     print(col)
    #     print(col.get_text())
    #     print(col)
        
# Task 5
# print(data)


# Task 6
sections = soup.find('div', class_='sections')
h2s = sections.find_all('h2')
# for h2 in h2s:
#     print("h2:", h2.get_text(), "p:",  h2.find_next_sibling('p').get_text())

# Task 7
divs = soup.find_all('div', class_='sections')
headings = []
paragraphs = []
for div in divs:
    h2 = div.find_all('h2')
    p = div.find('p')
    if h2:
        headings.append([h.get_text() for h in h2])
    if p:
        paragraphs.append([p.get_text() for p in p])
# print(headings)
# print(paragraphs)

# Task 8
h2 = soup.find('h2', id= 'section-1')
li = soup.find('li', id = 'nav-home')
# print(h2.get_text())
# print(li.get_text())

# Task 9
ps = soup.find_all('p', class_='description')
# for p in ps:
#     print(p.get_text())

all_txt = soup.get_text()
# print(all_txt)



# Task 10
url = "https://quotes.toscrape.com/"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    
quoteSoap = BeautifulSoup(html_content, 'html.parser')

divs = quoteSoap.find_all('div', class_='quote')
quotes = []
for div in divs:
    quote = div.find('span', class_='text').get_text()
    author = div.find('small', class_='author').get_text()
    quotes.append({'quote': quote, 'author': author})
    
# for quote in quotes:
    # print(quote)
# Task 11
next_page = quoteSoap.find('li', class_='next')
next_page_url = next_page.find('a')['href']
print(f'{url}{next_page_url[1:]}')

# Task 12
tags = quoteSoap.find_all('a', class_='tag')
print([tag.get_text() for tag in tags])

