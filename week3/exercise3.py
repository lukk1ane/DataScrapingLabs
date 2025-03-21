from bs4 import BeautifulSoup
import requests
import pandas as pd



def task1():
    title = soup.find("title")
    print("Title:", title.get_text(), "\n")

def task2():
    top_header_div = soup.find("body").find("div", id="top-header")
    print("Top header h1:", top_header_div.find("h1").get_text())
    print("P_tagline:", top_header_div.find("p", class_="tagline").get_text(), "\n")

def task3():
    navigation_div = soup.find("body").find("div", id="navigation")
    menu_item_list = navigation_div.find('ul', class_="nav-menu").find_all('li', class_="menu-item")
    print("Menu items:", [item.get_text() for item in menu_item_list], "\n")

def task4_5():
    product_table = soup.find("div", class_="content").find("table", id="product-table")

    product_table_headers = [th.text.strip() for th in product_table.find("tr").find_all("th")]

    product_table_data = []
    for row in product_table.find_all("tr")[1:]:
        row_data = [td.text.strip() for td in row.find_all("td")]
        product_table_data.append(dict(zip(product_table_headers, row_data)))

    print("Product Table Data (Dictionary Format):")
    print(product_table_data, "\n")

def task6_7():
    content_div_sections = soup.find("div", class_="content").find("div", class_='sections')
    print("h2 sections:", [item for item in content_div_sections.find_all('h2')])
    print("p sections:", [item for item in content_div_sections.find_all('p')])

    print("h2 sections text:", [item.get_text() for item in content_div_sections.find_all('h2')])
    print("p sections text:", [item.get_text() for item in content_div_sections.find_all('p')])

def task8():
    content_div_sections = soup.find("div", class_="content").find("div", class_='sections')
    navigation_li_nav_home = soup.find("div", id="navigation").find("ul", class_="nav-menu")

    h2_section_1 = content_div_sections.find("h2", id="section-1")
    li_nav_home = navigation_li_nav_home.find("li", id="nav-home")

    print("H2 Section 1:", h2_section_1.get_text())
    print("LI Nav Home:", li_nav_home.get_text(), "\n")

def task9():
    p_descriptions = soup.find_all("p", class_="description")
    print("All paragraphs p with class Description:")
    for p in p_descriptions:
        print(p.get_text())
    print()

def task10():
    for element in soup(["script", "style"]):
        element.extract()

    visible_text = soup.get_text(separator="\n", strip=True)
    print(visible_text)

def all_quotes_and_authors():
    quotes_and_authors = (soup_quotes.find_all("div", class_="quote"))

    for qao in quotes_and_authors:
        spans = qao.find_all("span")
        quote = spans[0]
        author = spans[1].find("small")
        print({"quote": quote.get_text(), "author": author.get_text()})

def extract_next_page_link():
    next_page_link = soup_quotes.find("li", class_="next").find("a").get("href")
    full_url = url.rstrip("/") + next_page_link
    print("Next Page Link:", full_url, "\n")

def extract_tags():
    quotes_and_authors = (soup_quotes.find_all("div", class_="quote"))
    for qao in quotes_and_authors:
        tags = qao.find_all("a", class_="tag")
        print([tag.get_text() for tag in tags])



if __name__ == '__main__':
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
    soup = BeautifulSoup(html_doc, "html.parser")

    task1()
    task2()
    task3()
    task4_5()
    task6_7()
    task8()
    task9()
    task10()

    url = "http://quotes.toscrape.com/"
    response = requests.get(url)
    soup_quotes = BeautifulSoup(response.text, "html.parser")

    all_quotes_and_authors()
    extract_next_page_link()
    extract_tags()
