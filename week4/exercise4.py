import requests
from bs4 import BeautifulSoup
from lxml import html



def task1():
    book_titles = soup.find_all('h3')
    for book_title in book_titles:
        parent = book_title.parent
        p_tag_price_color = parent.find('p', class_='price_color')
        print(f"Title: {book_title.find("a").get("title")}, Price: {p_tag_price_color.text}")

def task2():
    tree = html.fromstring(response.text)
    book_titles = soup.find("section").find_all('a')

    rating_nodes = tree.xpath('//article[@class="product_pod"]/p[contains(@class, "star-rating")]/@class')
    availability_nodes = tree.xpath(
        '//article[@class="product_pod"]/div[@class="product_price"]/p[contains(@class, "instock")]/text()')
    rating_index = 0

    for book_title in book_titles:
        if book_title and book_title.parent:
            parent_h3 = book_title.parent
            h3_next_sibling_price = parent_h3.find_next_sibling("div", class_="product_price")
            h3_previous_sibling_image = parent_h3.find_previous_sibling("div", class_="image_container")

            if h3_next_sibling_price and h3_previous_sibling_image:
                p_tag_price_color = h3_next_sibling_price.find('p', class_='price_color')
                book_image = h3_previous_sibling_image.find('img')['src']

                if rating_index < len(rating_nodes):
                    rating = rating_nodes[rating_index].split()[-1]
                else:
                    rating = "N/A"

                availability_raw = availability_nodes[rating_index * 2:rating_index * 2 + 2]
                availability = ''.join([a.strip() for a in availability_raw]).strip()

                if book_title.get("title"):
                    print(f"Title: {book_title.get('title')}")
                    print(f"Price: {p_tag_price_color.text}")
                    print(f"Rating: {rating}")
                    print(f"Availability: {availability}")
                    print(f"Image: {url + book_image.replace('../', '')}")
                    print("-" * 50)

                rating_index += 1



if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml") if response.status_code == 200 else None
    task2()
