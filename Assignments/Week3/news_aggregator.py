from bs4 import BeautifulSoup
import requests

def fetch_html(url):
    """
    Fetches the HTML content of a given URL.
    :param url: The URL to fetch content from.
    :return: The HTML content as a string.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    return response.text

def parse_html(html_content):
    """
    Converts HTML content into a BeautifulSoup object.
    :param html_content: The HTML content as a string.
    :return: A BeautifulSoup object for easy navigation.
    """
    return BeautifulSoup(html_content, 'html.parser')

def test_connection():
    """
    Tests the setup by connecting to a news website and retrieving its content.
    """
    test_url = "https://www.bbc.com/news"
    try:
        html_content = fetch_html(test_url)
        soup = parse_html(html_content)
        print("Connection successful. Page title:", soup.title.string)
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()

