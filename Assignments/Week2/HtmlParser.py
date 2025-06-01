import requests
from bs4 import BeautifulSoup
from lxml import etree

class HtmlParser:
    def __init__(self, url, user_agent="Google"):
        self.url = url
        self.headers = {"User-Agent": user_agent}
        self.html_content = self.fetch_html()
        self.soup = BeautifulSoup(self.html_content, "html.parser") #using BeautifulSoup to parse HTML structure
        self.tree = etree.HTML(self.html_content)

    def fetch_html(self):
        try:
            # fetching data using request library again
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return ""

    def extract_element_by_css(self, selector):
        return [element.get_text(strip=True) for element in self.soup.select(selector)]

    def extract_element_by_xpath(self, xpath):
        return [element.text.strip() for element in self.tree.xpath(xpath) if element.text]

    def text_cleaner(self, text):
        return " ".join(text.split())

    def navigate_HTML_tree(self):
        return [tag.name for tag in self.soup.find_all(True)]

# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    parser = HtmlParser(url, user_agent="Google")
    print("Extracted elements by CSS:", parser.extract_element_by_css("p"))
    print("Extracted elements by XPath:", parser.extract_element_by_xpath("//p"))
    print("Cleaned text:", parser.text_cleaner("   Example   text   with spaces  "))
    print("HTML tree structure:", parser.navigate_HTML_tree())
