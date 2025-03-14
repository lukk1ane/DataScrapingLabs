import requests
from bs4 import BeautifulSoup


# task1
URL = "https://books.toscrape.com/"
response = requests.get(URL)

for key, value in response.headers.items():
    print(f"{key}: {value}")


# task2
import requests
from bs4 import BeautifulSoup

def book_titles():
    url = "http://books.toscrape.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        book_titles = [book.a['title'] for book in soup.find_all('h3')]

        print("titles on homepage:")
        for title in book_titles:
            print(title)
    else:
        print(f"failed to retrieve page")


#task 3

def fetch_books_from_pages(pages):
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    
    for page in range(1, pages + 1):
        url = base_url.format(page)
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_titles = [book.a['title'] for book in soup.find_all('h3')]
            
            print(f"Book Titles on Page {page}:")
            for title in book_titles:
                print(title)
            print("-" * 50)
        else:
            print(f"Failed to retrieve page {page}. Status Code: {response.status_code}")

# fetch_books_from_pages(2)


#task 4

def get():
    print("GET request:")
    response = requests.get(URL)
    print(f"status Code: {response.status_code}")
    print("\n")

def post():
    response = requests.post(URL)


def head():
    print("HEAD request:")
    response = requests.head(URL)
    print(f"status code: {response.status_code}")
    print(f"response headers: {response.headers}")

get()
post()
head()

