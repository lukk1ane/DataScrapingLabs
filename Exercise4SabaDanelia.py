import requests
from bs4 import BeautifulSoup
from lxml import etree

def html_to_soup(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.content,"html.parser")
    except  requests.exceptions.RequestException as e:
        raise e

def extract_all_books(soup):
    data = soup.find_all('h3')
    names = [d.find_next('a').get_text() for d in data]
    prices = [d.find_parent().select_one("p.price_color").get_text() for d in data]
    data = []
    for j in range(len(names)):
        data.append({"name":names[j],"price":prices[j]})
    print(data)


def html_to_soup(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.content,"html.parser")
    except  requests.exceptions.RequestException as e:
        raise e

def family_tree(soup):

    data = soup.find("article")
    tree = etree.HTML(str(soup))
    dd = tree.xpath("//a")
    for i in dd:
        if i.text is not None:
            print(i.tag,i.text)

def siblings(soup):
    data = soup.find("ol")

    z= data.find_next('li')
    names = []
    while True:
        z = z.find_next_sibling('li')

        if z is None:
            break
        name = z.find_next('a')['href']
        names.append(name)
        # print(name)

    print(names)
    print("_____________")


if __name__ == "__main__":
    print("task1")
    print("_____________")
    url = "https://books.toscrape.com/"
    soup = html_to_soup(url)
    extract_all_books(soup)

    print("task2")
    print("_____________")
    url = "https://books.toscrape.com/"
    soup = html_to_soup(url)
    family_tree(soup)
    print("_____________")
    siblings(soup)