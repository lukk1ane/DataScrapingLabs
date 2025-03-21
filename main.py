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

print('task_1')
# ● Find and extract the <title> tag inside the <head> section.
selector_1 = "head title"
task_1 = soup.select_one(selector_1)
print(task_1.text)
print('-----')
print()
# ● Retrieve the <h1> element inside the <div> with id='top-header'.
print('task_2')
selector_2_1 = "div#top-header h1"
task_2_1 = soup.select_one(selector_2_1)
print(task_2_1.text)
# ● Extract the <p> element with class='tagline'
selector_2_2 = 'p.tagline'
task_2_2 = soup.select_one(selector_2_2)
print(task_2_2.text)
print('-----')
print()
#  Locate the <ul> with class='nav-menu' and extract the text inside all <li> elements
# with class='menu-item'.
print('task_3')
selector_3 = "div#navigation > ul.nav-menu li"
task_3 = soup.select(selector_3)
for t in task_3:
    print(t.text)
print('-----')
print()
# ● Find the <table> with id='product-table'.
# ● Extract product names, prices, and stock availability from the table rows.
print('task_4')
print('-----')
print('-----')
print()
table = soup.select_one('table#product-table')
headers = [h.text.strip() for h in table.select('tr th')]

print(headers)
for row in table.select('tr'):
    cells = [c.text.strip() for c in row.select('td')]
    if cells:
        print(cells)
print('-----')
print('-----')
print()
# Convert extracted table data into a list of dictionaries with keys: Product, Price, and
# Stock.
print('task_5')
table = soup.select_one('table#product-table')
headers = [h.text.strip() for h in table.select('tr th')]

print(headers)
for row in table.select('tr'):
    cells = [c.text.strip() for c in row.select('td')]
    if cells:
        print(dict(zip(headers, cells)))
print('-----')
print()
print('task_6')
# Retrieve all <h2> elements inside the <div> with class='sections'.
# ● Extract the <p> element (description) immediately following each <h2>.
selector_6 = "div.sections h2 + p"
task_6 = soup.select(selector_6)
for p in task_6:
    print(p.text)
print('-----')
print()

print('task_7')
# Locate headings inside the <div> with class='sections' and extract their text.
# ● Extract all paragraph texts inside the same <div>.
selector_7 = "div.sections * "
task_7 = soup.select(selector_7)
for p in task_7:
    print(p.text)
print('-----')
print()

print('task_8')

# ● Find the <h2> with id='section-1' and extract its text.
# ● Find the <li> with id='nav-home' and extract its text.

selector_8_1 = "h2#section-1"
task_8_1 = soup.select_one(selector_8_1)
selector_8_2 = "li#nav-home"
task_8_2 = soup.select_one(selector_8_2)
print(task_8_1.text)
print(task_8_2.text)
print('-----')
print()

print('task_9')

selector_9 = "p.description"
task_9 = soup.select(selector_9)
for t in task_9:
    print(t.text)
print('-----')
print()

print('--Part_2--')

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print('All Quotes and Their Authors:')


def all_quotes_and_their_authors():
    quotes = soup.select('span.text')
    authors = soup.select('small.author')

    return {k.text: v.text for k, v in zip(quotes, authors)}


for k, v in all_quotes_and_their_authors().items():
    print(f'{k} : {v}')
print('-----')
print()

print('The "Next" Page Link:')


def next_page():
    next_link = soup.select_one('li.next a')
    return next_link['href']


print('-----')
print()

print(url + next_page())

print('Extract Tags with a Specific Class Using CSS Selectors:')


def all_tags_with_a():
    tags = soup.select('a.tag')
    for t in tags:
        print(t.text)


all_tags_with_a()
print()
print('-----')
