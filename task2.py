import requests
from bs4 import BeautifulSoup

def main():
    
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    
   
    if response.status_code == 200:
     
        soup = BeautifulSoup(response.content, 'html.parser')
        
       
        book_titles = soup.select("article.product_pod h3 a")
       
        print(f"Found {len(book_titles)} books on the homepage:")
        for i, title in enumerate(book_titles, 1):
           
            book_title = title.get('title')
            print(f"{i}. {book_title}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    main()