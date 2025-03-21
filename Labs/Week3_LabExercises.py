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

def extract_title():
    return soup.title.text

def extract_main_heading_and_tagline():
    heading = soup.select_one("#top-header h1").text
    tagline = soup.select_one(".tagline").text
    return heading, tagline

def extract_navigation_items():
    return [li.text for li in soup.select(".nav-menu .menu-item")]

def extract_table_data():
    rows = soup.select("#product-table tr")[1:]
    return [tuple(td.text for td in row.find_all("td")) for row in rows]

def table_data_to_dict():
    rows = extract_table_data()
    return [
        {"Product": product, "Price": price, "Stock": stock}
        for product, price, stock in rows
    ]

def extract_sections_and_descriptions():
    sections = soup.select(".sections h2")
    descriptions = [h2.find_next_sibling("p").text for h2 in sections]
    return [(h2.text, desc) for h2, desc in zip(sections, descriptions)]

def extract_nested_elements():
    container = soup.select_one(".sections")
    headings = [h2.text for h2 in container.find_all("h2")]
    paragraphs = [p.text for p in container.find_all("p")]
    return headings, paragraphs

def extract_by_ids():
    section = soup.select_one("#section-1").text
    nav_item = soup.select_one("#nav-home").text
    return section, nav_item

def extract_specific_paragraphs():
    return [p.text for p in soup.select("p.description")]

def extract_all_visible_text():
    return soup.get_text(strip=True, separator=' ')

def scrape_quotes_page():
    url = 'http://quotes.toscrape.com'
    res = requests.get(url)
    page = BeautifulSoup(res.text, 'html.parser')
    quotes_data = []
    quotes = page.select(".quote")
    for q in quotes:
        text = q.select_one(".text").text
        author = q.select_one(".author").text
        quotes_data.append((text, author))
    next_link = page.select_one("li.next a")
    next_url = url + next_link['href'] if next_link else None
    tags = [tag.text for tag in page.select(".tags .tag")]
    return quotes_data, next_url, tags

