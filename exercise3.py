from bs4 import BeautifulSoup
import requests
with open("main.html", "r", encoding="utf-8") as file:
    html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# task 1
title = soup.title.text
# task 2
main_heading = soup.find('h1').text
tagline = soup.find('p', class_='tagline').text
# task3
nav_items = [li.text for li in soup.select('.nav-menu .menu-item')]

# task 4
table = soup.find('table', id='product-table')
rows = table.find_all('tr')[1:]
products = [{
    'Product': row.find_all('td')[0].text,
    'Price': row.find_all('td')[1].text,
    'Stock': row.find_all('td')[2].text
} for row in rows]

# task 5
sections = [{
    'Title': h2.text,
    'Description': h2.find_next_sibling('p').text
} for h2 in soup.select('.sections h2')]

# task 6
section_1_text = soup.find('h2', id='section-1').text
nav_home_text = soup.find('li', id='nav-home').text


descriptions = [p.text for p in soup.select('p.description')]

all_text = ' '.join(soup.stripped_strings)


url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

quotes = [{
    'Quote': quote.find('span', class_='text').text,
    'Author': quote.find('small', class_='author').text
} for quote in soup.select('div.quote')]

next_page = soup.select_one('li.next > a')
next_page_url = url + next_page['href'] if next_page else None


tags = [tag.text for tag in soup.select('.tag')]


print(f'Title: {title}')
print(f'Main Heading: {main_heading}, Tagline: {tagline}')
print(f'Navigation Items: {nav_items}')
print(f'Products: {products}')
print(f'Sections: {sections}')
print(f'Section 1: {section_1_text}, Home Nav: {nav_home_text}')
print(f'Descriptions: {descriptions}')
print(f'All Text: {all_text}')
print(f'Quotes: {quotes}')
print(f'Next Page URL: {next_page_url}')
print(f'Tags: {tags}')
