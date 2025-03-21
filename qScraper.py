import requests
from bs4 import BeautifulSoup

def scrape_quotes_website():
    url = 'http://quotes.toscrape.com'
    
    try:
        
        response = requests.get(url)
        
       
        if response.status_code == 200:
           
            soup = BeautifulSoup(response.text, 'html.parser')
            
           
            print("All Quotes and Their Authors:")
            quote_divs = soup.find_all('div', class_='quote')
            for quote in quote_divs:
                quote_text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                print(f"Quote: {quote_text}")
                print(f"Author: {author}")
                print("---")
            
            next_button = soup.find('li', class_='next')
            if next_button:
                next_link = next_button.find('a')['href']
                next_page_url = url + next_link
                print(f"\nNext Page URL: {next_page_url}")
            else:
                print("\nNo Next Page Found")
            
         
            print("\nTags Associated with Quotes:")
            all_tags = soup.select('.tag')
            unique_tags = set()
            for tag in all_tags:
                unique_tags.add(tag.text)
            for tag in unique_tags:
                print(f"- {tag}")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request to website: {e}")


if __name__ == "__main__":
    scrape_quotes_website()