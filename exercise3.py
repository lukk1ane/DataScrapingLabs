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

# task1
print(soup.find('title').text)
# task2
print(soup.find('div', id = 'top-header').find('h1').text)
print(soup.find('p',class_ = 'tagline').text)
# task3
for i in [li.text for li in soup.find_all('li', class_='menu-item')]:
    print(i)
# task4
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:] 
products = [[td.text for td in row.find_all('td')] for row in rows]
for i in products:
    print(i)
# Task5
product_list = [{"Product : " : p[0], "Price : " : p[1], "Stock : " : p[2]} for p in products]
print(product_list)
# task6
elements = soup.find('div', class_ = 'sections').find_all('h2')
descriptions = [h2.find_next_sibling('p').text for h2 in elements]
print(descriptions)
# task7
headings_text = [h2.text for h2 in soup.select("div.sections h2")]
paragraphs_text = [p.text for p in soup.select("div.sections p")]
print(paragraphs_text)
# task8
print(soup.find('h2', id = 'section-1').text)
print(soup.find('li', id = 'nav-home').text)
# task9
descriptions_text = [p.text for p in soup.find_all('p', class_='description')]
for i in descriptions_text:
    print(i)
from bs4 import BeautifulSoup


# -----

soup = BeautifulSoup(html_doc, "html.parser")
text = soup.get_text(separator=" ") 

# -----

url = 'http://quotes.toscrape.com'
response = requests.get(url)
if response.status_code == 200:
    soup1 = BeautifulSoup(response.text, "html.parser")

# All Quotes and Their Authors: 
divs = soup1.find_all('div', class_ = 'quote')
quotes = soup1.find_all('span' , class_ = 'text')
authors = soup1.find_all('small', class_ = 'author')
for i in range(len(quotes)):
    print(f"{quotes[i].text} - {authors[i].text}")

# The "Next" Page Link:

linkToNextPage = soup1.find('li', class_ = 'next').find('a')['href']
print(linkToNextPage)


# 

tags = soup1.select('a.tag')
for tag in tags:
    print(tag.text) 

