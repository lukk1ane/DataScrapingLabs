from bs4 import BeautifulSoup
import requests

html_content = """
<html>
<head><title>Sample Page</title></head>
<body>
    <div id='header' class='header'>
        <h1>Primary Heading</h1>
        <p class='subtext'>This is a sample webpage.</p>
    </div>
    <div id='menu'>
        <ul class='nav-list'>
            <li id='menu-home' class='menu-option'>Home</li>
            <li id='menu-about' class='menu-option'>About</li>
            <li id='menu-contact' class='menu-option'>Contact</li>
        </ul>
    </div>
    <div class='main-content'>
        <table id='items-table'>
            <tr><th>Item</th><th>Cost</th><th>Availability</th></tr>
            <tr><td>Notebook</td><td>$12</td><td>Available</td></tr>
            <tr><td>Pen</td><td>$5</td><td>Sold Out</td></tr>
        </table>
        <div class='details'>
            <h2 id='topic-1'>Topic 1</h2>
            <p class='info'>Information about topic 1.</p>
            <h2 id='topic-2'>Topic 2</h2>
            <p class='info'>Information about topic 2.</p>
        </div>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html_content, 'html.parser')

"""Task 1"""
page_title = soup.title.text
print("Page Title:", page_title)

"""Task 2"""
primary_heading = soup.find('h1').text
subtext = soup.find('p', class_='subtext').text
print("Primary Heading:", primary_heading)
print("Subtext:", subtext)

"""Task 3"""
navigation_options = [li.text for li in soup.select('.nav-list .menu-option')]
print("Navigation Options:", navigation_options)

"""Task 4 & 5"""
items = []
table_rows = soup.select('#items-table tr')[1:]
for row in table_rows:
    columns = row.find_all('td')
    items.append({
        'Item': columns[0].text,
        'Cost': columns[1].text,
        'Availability': columns[2].text
    })
print("Item Table Data:", items)

"""Task 6 & 7"""
topics = {h2.text: h2.find_next_sibling('p').text for h2 in soup.select('.details h2')}
print("Topics:", topics)

"""Task 8"""
topic_1_text = soup.find(id='topic-1').text
menu_home_text = soup.find(id='menu-home').text
print("Topic 1 Text:", topic_1_text)
print("Menu Home Text:", menu_home_text)

"""Task 9"""
info_texts = [p.text for p in soup.select('p.info')]
print("Information Texts:", info_texts)

"""Task 10"""
all_text = ' '.join(soup.stripped_strings)
print("All Visible Text:", all_text)

"""Task 11"""
url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

"""Task 12"""
quotes_list = [{
    'Quote': quote.find('span', class_='text').text,
    'Author': quote.find('small', class_='author').text
} for quote in soup.select('.quote')]
print("Quotes List:", quotes_list)

"""Task 13"""
next_link = soup.select_one('.next > a')
next_link_url = url + next_link['href'] if next_link else "No Next Page"
print("Next Page URL:", next_link_url)

"""Task 14"""
quote_tags = [tag.text for tag in soup.select('.tag')]
print("Quote Tags:", quote_tags)