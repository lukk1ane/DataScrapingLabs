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


#task1
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.find('title'))

#task2
# print(soup.find('div', id='top-header').h1)
# print(soup.find('p', class_='tagline'))


#task3
nav_menu = soup.find('ul', class_='nav-menu') 
menu_items = [li.text for li in nav_menu.find_all('li', class_='menu-item')]  

# print("nav menu lists:", menu_items)

#task4 and 5
prod_table = soup.find('table', id = 'product-table')
products = []
rows = prod_table.find_all('tr')[1:]
for row in rows:
    cols = row.find_all('td')  # Extract all <td> elements
    product_name = cols[0].text
    price = cols[1].text
    stock = cols[2].text
    products.append({"product": product_name, "price": price, "stock": stock})
# print(products)

#task6
sections_div = soup.find('div', class_='sections')  
sections = sections_div.find_all('h2') 

section_desc = sections_div.find_all('p')
# print("all h2 elements:", sections)
# print("all p elements after h2", section_desc)

#task7
headings_texts = [h2.text for h2 in sections_div.find_all('h2')]
paragraphs_texts = [p.text for p in sections_div.find_all('p')]

# print("headings:", headings_texts)
# print("paragraphs:", paragraphs_texts)

#task8
h2_text = sections_div.find('h2', id='section-1').text
nav_home = soup.find('li', id='nav-home')

# print("li home navigation item:", nav_home.text)
# print(h2_text)

#task9
desc_p = soup.find_all('p', class_='description')
texts = [p.text for p in desc_p]
# print(texts)

# all visible text in html document
visible_text = soup.get_text(separator='\n', strip=True)
# print(visible_text)


# second part of exercise 3
response = requests.get("http://quotes.toscrape.com")
soup = BeautifulSoup(response.content, "lxml")

# extracting All Quotes and Their Authors:
divs = soup.find_all("div", class_ = "quote")
quotes = []
for div in divs: 
    txt = div.find("span", class_="text").text
    author = div.find("small", class_ = "author").text
    quotes.append({"quote": txt, "author": author})

# for q in quotes:
#     print(q)


#The "Next" Page Link:
next_button = soup.find("li", class_="next")
url = next_button.find("a")["href"]
# print(url)



# Extract all tags associated with the quotes

#tags associated with quotes: 
tags_of_quotes = []
divs = soup.select('div.tags a.tag')  

for tag in divs:
    tags_of_quotes.append(tag)  

#top 10 tags

top_10_tags = []
tag_spans = soup.select('span.tag-item a.tag')

for tag in tag_spans:
    top_10_tags.append(tag)  

# print("tags of quotes:")
# for tag in tags_of_quotes:
#     print("tag: ", tag, "tag text: ", tag.text)

# print("top 10 tags:")
# for tag in top_10_tags:
#     print("tag: ", tag, "tag text: ", tag.text)

