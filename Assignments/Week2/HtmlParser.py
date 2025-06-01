from bs4 import BeautifulSoup
from lxml import html
import requests


def fetch_html(url):
    """Fetch HTML content from a URL."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


def parse_with_soup(html_content):
    """Parse HTML using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')


def extract_elements_soup(soup, selector):
    """Extract elements using CSS selectors."""
    return soup.select(selector)


def parse_with_lxml(html_content):
    """Parse HTML using lxml for XPath queries."""
    return html.fromstring(html_content)


def extract_elements_xpath(tree, xpath_query):
    """Extract elements using XPath queries."""
    return tree.xpath(xpath_query)


def clean_text(text):
    """Clean extracted text content."""
    return ' '.join(text.split()).strip()


def navigate_html_tree(soup):
    """Example function to navigate HTML tree structures."""
    return [tag.name for tag in soup.find_all(True)]


# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    html_content = fetch_html(url)

    # Using BeautifulSoup
    soup = parse_with_soup(html_content)
    elements = extract_elements_soup(soup, "p")  # Extracting <p> elements
    cleaned_texts = [clean_text(el.get_text()) for el in elements]

    # Using lxml for XPath
    tree = parse_with_lxml(html_content)
    xpath_elements = extract_elements_xpath(tree, "//p/text()")

    print("Extracted Paragraphs (CSS Selector):", cleaned_texts)
    print("Extracted Paragraphs (XPath):", xpath_elements)
    print("HTML Tags in Tree:", navigate_html_tree(soup))
