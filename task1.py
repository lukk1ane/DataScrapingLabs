import requests

def fetch_books_to_scrape():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    fetch_books_to_scrape()
