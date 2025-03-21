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
soup =  BeautifulSoup(html_doc,features='lxml')
task1 = soup.find("head").find_next()
print(task1)
print("______________________________________")

task2_1 = soup.find("div",id = "top-header").find("h1")
task2_2 = soup.find("p",class_="tagline")
print(task2_1)
print(task2_2)
print("______________________________________")

task3 = list(soup.find("ul",class_='nav-menu').find_all('li'))
task3 = [x.get_text() for x in task3]
print(task3)
print("______________________________________")

task4 = list(soup.find('table',id = 'product-table').find_all("tr"))
task4 = [x.find_all('td') for x in task4 ]
task4 = [x  for x in task4 if x != []]
task4_1 = []
for i in task4:
    temp = []
    for j in i:
        temp.append(j.get_text())
    task4_1.append(temp)
print(task4_1)
print("______________________________________")

task5l = list(soup.find('table',id = 'product-table').find_all("th"))
task5l = [x.get_text() for x in task5l]
task5 = []
for j in task4_1:
    dictionary = {}
    for i in range(len(task5l)):
        dictionary[task5l[i]] = j[i]
    task5.append(dictionary)
print(task5)
print("______________________________________")

task6_1 = list(soup.find('div',class_="sections").find_all("h2"))
task6_2 = [x.find_next_sibling('p',class_="description") for x in task6_1]
print(task6_1)
print(task6_2)
print("______________________________________")


task7 = []
for h in range(1,4):
    task7+=soup.find('div',class_='sections').find_all(f'h{h}')
task7_1 = [x.get_text() for x in task7]
task7_2 =soup.find_all('div')
task7_2 = [x.find_all('p') for x in task7_2]
task7 = [x for x in task7_2 if x != []]
task7_2 = []
for x in task7:
    for j in x:
        task7_2.append(j.get_text())

print(task7_1)
print(task7_2)
print("______________________________________")

task8_1 = soup.find('h2',id='section-1').get_text()
task8_2 = soup.find('li',id ='nav-home').get_text()
print(task8_1)
print(task8_2)
print("______________________________________")

task9 = soup.find_all('p',class_='description')
task9 = [x.get_text() for x in task9]
print(task9)

print("______________________________________")

task10 = soup.get_text()
lines = (line.strip() for line in task10.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
task10 = '\n'.join(chunk for chunk in chunks if chunk)

print(task10)

print("______________________________________")


def extractAllQuotes(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')

    # get all divs
    divs = soup.find_all("div",class_='quote')
    # from each div find quote,author and tags via selector, store them in same list and print them together
    quotes = [[x.find('span',class_='text'),x.find('small',class_='author'),x.select('a.tag')]for x in divs]
    # quotes = [[x.find('span',class_='text'),x.find('small',class_='author'),x.find_all('a',class_='tag')]for x in divs]

    for q in quotes:
        print(f"Quote: {q[0].get_text()} -- By: {q[1].get_text()}")
        tags = []
        for tag in q[2]:
            tags.append(tag.get_text())
        print(f"tags: {tags}")
def extractNextUrl(url,main = ""):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    next = soup.find('li',class_='next').find('a').get('href')
    return main + next if main != "" else url+next

extractAllQuotes("https://quotes.toscrape.com/")
nextUrl = extractNextUrl("https://quotes.toscrape.com/")
print(nextUrl)