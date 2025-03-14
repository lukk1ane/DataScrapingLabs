import requests

def main():
    
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    
   
    print(f"Status Code: {response.status_code}")
    
    
    print("\nResponse Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

if __name__ == "__main__":
    main()