import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    try:
        res = requests.get(url)
        if res.ok:
            return BeautifulSoup(res.text, "html.parser")
        else:
            print(f"Error: {res.status_code}. Please try again.")
            return None
    except requests.exceptions.SSLError as e:
        print(f"Error: invalid SSL request. Please try again.")
        return None


def get_books_data(node):
    data = []
    if node:
        titles = dom.find_all("h3")
        for title in titles:
            parent_container = title.parent
            price_text = parent_container.find("p", class_="price_color").text[1:]
            price = price_text[1:]
            currency = price_text[0]
            data.append({"title": title.text, "price": price, "currency": currency})
        return data
    else:
        return []


def get_article_data(node):
    MAIN_CONTENT_ID = "content"
    MAIN_CONTENT_BODY_ID = "bodyContent"
    LEFT_NAVBAR_ID = "left-navigation"
    BASE_URL = "https://en.wikipedia.org"
    MAIN_TEXT_ID = "mw-content-text"
    if node:
        main = node.find("main", id=MAIN_CONTENT_ID)
        main_text = main.find("div", id=MAIN_CONTENT_BODY_ID).find("div", id=MAIN_TEXT_ID).find("div")
        article_text = ""
        for child in main_text.children:
            if child.name == "p":
                article_text += child.text
        left_nav = node.find("div", id=LEFT_NAVBAR_ID)
        article_url = BASE_URL + left_nav.find("span").parent.get("href")
        title = main.find("header").find("h1").text
        article_refs = []
        refs_list = main.find("ol", class_="references")
        list_items = refs_list.find_all("li")
        for list_item in list_items:
            links = list_item.find("span", class_="reference-text").find_all("a")
            for link in links:
                ref_link = None
                if link.has_attr("class"):
                    if "external" in link.get("class")[0]:
                        ref_link = link.get("href")
                else:
                    ref_link = BASE_URL + link.get("href")
                article_refs.append({"text": link.text, "url": ref_link})
        return {"title": title, "url": article_url, "text": article_text, "refs": article_refs}
    else:
        return {}


# task 1

URL = "https://books.toscrape.com"

dom = get_html_content(URL)
books_data = get_books_data(dom)
for book in books_data:
    print(book)

# task 2

WIKIPEDIA_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

dom = get_html_content(WIKIPEDIA_RANDOM_URL)
article_data = get_article_data(dom)
print(article_data)
