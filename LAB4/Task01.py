import requests
from bs4 import BeautifulSoup

def scrape_books_toscrape():
    """
    Extracts all book titles and prices from the main page of
    https://books.toscrape.com/ using the .parent attribute.
    """
    url = "https://books.toscrape.com/"
    print(f"--- Task 1: Scraping {url} ---")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all h3 tags which contain book titles
    h3_tags = soup.find_all('h3')

    if not h3_tags:
        print("No book titles found on the page.")
        return

    print("\nBook Titles and Prices:")
    for h3_tag in h3_tags:
        # Extract title from the 'a' tag inside h3
        title = h3_tag.find('a')['title'].strip() if h3_tag.find('a') else "Title not found"

        # Navigate to the parent element of the h3 tag
        parent_element = h3_tag.parent

        # Find the price tag within the parent element
        price_tag = parent_element.find('p', class_='price_color') if parent_element else None
        price = price_tag.get_text(strip=True) if price_tag else "Price not found"

        print(f"Title: {title}, Price: {price}")

    print("-" * 20)

if __name__ == "__main__":
    scrape_books_toscrape()
    print("Finished.")
