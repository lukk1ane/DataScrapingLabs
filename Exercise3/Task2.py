import requests
from bs4 import BeautifulSoup


def scrape_quotes_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"Scraping data from: {url}")

    # task 1
    print("\n1. All Quotes and Their Authors:")
    print("-" * 50)
    quotes_divs = soup.find_all('div', class_='quote')

    for i, quote_div in enumerate(quotes_divs, 1):
        quote_text = quote_div.find('span', class_='text').text

        author = quote_div.find('small', class_='author').text

        print(f"Quote #{i}:")
        print(f"Text: {quote_text}")
        print(f"Author: {author}")
        print("-" * 30)

    # task 2
    print("\n2. The 'Next' Page Link:")
    print("-" * 50)
    next_button = soup.find('li', class_='next')

    if next_button:
        next_link = next_button.find('a')['href']
        next_page_url = url.rstrip('/') + next_link if next_link.startswith('/') else next_link
        print(f"Next page URL: {next_page_url}")
    else:
        print("No 'Next' page link found. This must be the last page.")

    # task 3
    print("\n3. Tags for Each Quote:")
    print("-" * 50)

    for i, quote_div in enumerate(quotes_divs, 1):
        print(f"Tags for Quote #{i}:")
        tags_div = quote_div.find('div', class_='tags')
        tags = tags_div.find_all('a', class_='tag')

        if tags:
            for tag in tags:
                print(f"- {tag.text}")
        else:
            print("No tags found for this quote.")
        print()


# Main execution
if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com'
    scrape_quotes_page(base_url)

    # Uncomment this for multiple page requests
    """
    current_url = base_url
    page_num = 1
    max_pages = 5

    while page_num <= max_pages:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        next_button = soup.find('li', class_='next')
        if next_button:
            next_link = next_button.find('a')['href']
            current_url = base_url + next_link if next_link.startswith('/') else next_link
            scrape_quotes_page(current_url)
            page_num += 1
        else:
            print("Reached the last page.")
            break
    """