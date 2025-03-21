import bs4

from doc import html_doc

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'lxml')


# Task 1
# print(soup.find('title'))


# Task 2
# print(soup.find('div',attrs={'id': 'top-header'})
#       .find('h1'))
# print(soup.find('p',attrs={'class':'tagline'}))


# Task 3
# print(soup.find('ul',attrs={'class': 'nav-menu'})
#       .find_all('li',attrs={'class':'menu-item'}))


# Task 4-5
# table = soup.find('table', attrs={'id': 'product-table'})
#
# def extract_product(product: bs4.element.Tag):
#     td = product.find_all('td')
#     try:
#         return {
#             'product': td[0],
#             'price': td[1],
#             'stock': td[2]
#         }
#     except IndexError:
#         return {}
#
# products = list(filter(lambda x: x != {}, map(extract_product, table.find_all('tr'))))
# print(products)


# Task6
# sections = soup.find('div', attrs={'class': 'sections'})
# sections = list(
#     map(lambda x: {'section': x[0].get_text(), 'description': x[1].get_text()},
#         zip(sections.find_all('h2'), sections.find_all('p'))))
# print(sections)


# Task 7
# sections = soup.find('div', attrs={'class': 'sections'})
# texts = list(map(lambda x: x.get_text(), sections.find_all('p')))
# print(texts)


# Task 8
# print(soup.find('h2', attrs={'id': 'section-1'}).get_text())
# print(soup.find('li', attrs={'id': 'nav-home'}).get_text())


# Task 9
# print(list(map(lambda x: x.get_text(), soup.find_all('p', attrs={'class': 'description'}))))


#####################
def get_all_text(element):
    if isinstance(element, bs4.element.NavigableString):
        return [element.get_text()]
    return sum((get_all_text(child) for child in element.children), [])


texts = list(filter(lambda x: x != '\n', get_all_text(soup.find('html'))))

print(texts)
