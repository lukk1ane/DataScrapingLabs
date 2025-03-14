"""
Books to Scrape - Web Scraping Toolkit

A comprehensive collection of utilities for interacting with the
Books to Scrape demo website (http://books.toscrape.com/).

Author: Nugo
"""

import argparse
import json
import logging
import socket
import ssl
import sys
import time
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, SSLError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("books_scraper")

# Constants
BASE_URL = "http://books.toscrape.com/"
SECURE_URL = "https://books.toscrape.com/"
DEFAULT_TIMEOUT = 10
USER_AGENT = "BooksScraper/1.0 (Educational Purposes)"


class RequestsClient:
    """HTTP client with session management."""
    
    def __init__(
        self, 
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        verify_ssl: bool = True,
    ):
        """Initialize the HTTP client."""
        self.base_url = base_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
    
    def close(self):
        """Close the underlying session."""
        self.session.close()
    
    def request(self, method: str, url: str, **kwargs):
        """Send an HTTP request with built-in error handling."""
        full_url = urljoin(self.base_url, url)
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify_ssl)
        
        try:
            logger.debug(f"Sending {method} request to {full_url}")
            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get(self, url: str, **kwargs):
        """Send a GET request."""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs):
        """Send a POST request."""
        return self.request("POST", url, **kwargs)
    
    def head(self, url: str, **kwargs):
        """Send a HEAD request."""
        return self.request("HEAD", url, **kwargs)


class BooksToScrape:
    """Primary interface for interacting with the Books to Scrape website."""
    
    def __init__(
        self, 
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        verify_ssl: bool = True
    ):
        """Initialize the scraper."""
        self.base_url = base_url
        self.client = RequestsClient(
            base_url=base_url,
            timeout=timeout,
            verify_ssl=verify_ssl
        )
    
    def close(self):
        """Close the client connection."""
        self.client.close()
    
    def get_status_and_headers(self):
        """Get the status code and response headers from the homepage."""
        response = self.client.get("/")
        return response.status_code, dict(response.headers)
    
    def extract_book_titles(self):
        """Extract all book titles from the homepage."""
        response = self.client.get("/")
        soup = BeautifulSoup(response.text, "html.parser")
        
        titles = []
        article_elements = soup.select("article.product_pod")
        
        for article in article_elements:
            title_element = article.select_one("h3 > a")
            if title_element and title_element.get("title"):
                titles.append(title_element["title"])
        
        logger.info(f"Extracted {len(titles)} book titles from homepage")
        return titles
    
    def scrape_catalog(self, max_pages: Optional[int] = None):
        """Scrape the book catalog with pagination."""
        # Get the first page
        response = self.client.get("/")
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract books from first page
        books = []
        for article in soup.select("article.product_pod"):
            title_element = article.select_one("h3 > a")
            if title_element and title_element.get("title"):
                books.append({
                    "title": title_element["title"],
                    "url": urljoin(self.base_url, title_element["href"])
                })
        
        # Check if there are more pages
        pages_processed = 1
        next_button = soup.select_one("li.next > a")
        
        while next_button and (max_pages is None or pages_processed < max_pages):
            next_url = urljoin(self.base_url, next_button["href"])
            response = self.client.get(next_url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract books from this page
            for article in soup.select("article.product_pod"):
                title_element = article.select_one("h3 > a")
                if title_element and title_element.get("title"):
                    books.append({
                        "title": title_element["title"],
                        "url": urljoin(self.base_url, title_element["href"])
                    })
            
            # Move to next page
            next_button = soup.select_one("li.next > a")
            pages_processed += 1
        
        logger.info(f"Scraped {len(books)} books from {pages_processed} pages")
        return books
    
    def test_http_methods(self):
        """Test different HTTP methods (GET, POST, HEAD) and their responses."""
        results = {}
        
        # GET request
        try:
            response = self.client.get("/")
            results["GET"] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_length": len(response.content),
            }
        except RequestException as e:
            results["GET"] = {"error": str(e)}
        
        # HEAD request
        try:
            response = self.client.head("/")
            results["HEAD"] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
            }
        except RequestException as e:
            results["HEAD"] = {"error": str(e)}
        
        # POST request (may not be supported by the website)
        try:
            response = self.client.post("/", data={"dummy": "data"})
            results["POST"] = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_length": len(response.content),
            }
        except RequestException as e:
            results["POST"] = {"error": str(e)}
        
        return results


def verify_ssl(url: str):
    """
    Verify a website's SSL certificate and return status and information.
    
    Args:
        url: URL to verify (must be HTTPS)
    """
    result = {
        "url": url,
        "verified": False,
        "error": None,
        "certificate": None,
    }
    
    # Ensure URL is HTTPS
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        result["error"] = "URL must use HTTPS protocol for SSL verification"
        return result
    
    try:
        # Try with SSL verification
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        result["verified"] = True
        result["status_code"] = response.status_code
        
        # Get certificate info using ssl module
        hostname = parsed_url.netloc
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                cert = ssl_sock.getpeercert()
                
                # Extract relevant certificate information
                if cert:
                    result["certificate"] = {
                        "subject": dict(x[0] for x in cert["subject"]),
                        "issuer": dict(x[0] for x in cert["issuer"]),
                        "version": cert["version"],
                        "not_before": cert["notBefore"],
                        "not_after": cert["notAfter"],
                    }
    
    except SSLError as e:
        result["error"] = f"SSL Certificate Verification Failed: {str(e)}"
    except Exception as e:
        result["error"] = f"Error during verification: {str(e)}"
    
    # Try with SSL verification disabled
    try:
        response_no_verify = requests.get(url, verify=False, timeout=DEFAULT_TIMEOUT)
        result["unverified_status_code"] = response_no_verify.status_code
        result["verification_disabled_works"] = True
    except Exception as e:
        result["verification_disabled_works"] = False
        result["unverified_error"] = str(e)
    
    return result


def task1_get_status_and_headers():
    """Task 1: Get and display status code and response headers."""
    logger.info("Task 1: Sending GET request and displaying status and headers")
    
    try:
        scraper = BooksToScrape()
        status_code, headers = scraper.get_status_and_headers()
        scraper.close()
        
        print(f"\nStatus Code: {status_code}")
        print("\nResponse Headers:")
        for key, value in headers.items():
            print(f"{key}: {value}")
    
    except Exception as e:
        logger.error(f"Error in Task 1: {e}")
        sys.exit(1)


def task2_extract_book_titles():
    """Task 2: Extract all book titles from the homepage."""
    logger.info("Task 2: Extracting book titles from homepage")
    
    try:
        scraper = BooksToScrape()
        titles = scraper.extract_book_titles()
        scraper.close()
        
        print(f"\nFound {len(titles)} books:")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
    
    except Exception as e:
        logger.error(f"Error in Task 2: {e}")
        sys.exit(1)


def task3_scrape_catalog(max_pages: int = 2):
    """
    Task 3: Scrape books from catalog pages.
    
    Args:
        max_pages: Maximum number of pages to scrape
    """
    logger.info(f"Task 3: Scraping catalog (max {max_pages} pages)")
    
    try:
        scraper = BooksToScrape()
        books = scraper.scrape_catalog(max_pages=max_pages)
        scraper.close()
        
        print(f"\nScraped {len(books)} books:")
        for i, book in enumerate(books[:10], 1):  # Show first 10 books
            print(f"{i}. {book['title']}")
        
        if len(books) > 10:
            print(f"... and {len(books) - 10} more")
        
        # Save results to JSON file
        with open("books_catalog.json", "w", encoding="utf-8") as f:
            json.dump(books, f, indent=2)
        
        print(f"\nScraped {len(books)} books and saved to books_catalog.json")
    
    except Exception as e:
        logger.error(f"Error in Task 3: {e}")
        sys.exit(1)


def task4_test_http_methods():
    """Task 4: Test different HTTP methods and their responses."""
    logger.info("Task 4: Testing HTTP methods")
    
    try:
        scraper = BooksToScrape()
        results = scraper.test_http_methods()
        scraper.close()
        
        for method, data in results.items():
            print(f"\n{method} Request:")
            if "error" in data:
                print(f"  Error: {data['error']}")
            else:
                print(f"  Status Code: {data['status_code']}")
                print("  Headers:")
                for key, value in data["headers"].items():
                    print(f"    {key}: {value}")
                if "content_length" in data:
                    print(f"  Content Length: {data['content_length']} bytes")
    
    except Exception as e:
        logger.error(f"Error in Task 4: {e}")
        sys.exit(1)


def task5_verify_ssl():
    """Task 5: Verify SSL certificate and display information."""
    logger.info("Task 5: Verifying SSL certificate")
    
    try:
        # Use a secure URL that should have SSL
        url = SECURE_URL
        if not url.startswith("https://"):
            url = url.replace("http://", "https://")
        
        result = verify_ssl(url)
        
        print(f"\nSSL Verification for {result['url']}:")
        print(f"Verification Successful: {result['verified']}")
        
        if result.get("error"):
            print(f"Error: {result['error']}")
        
        if result.get("certificate"):
            cert = result["certificate"]
            print("\nCertificate Information:")
            print(f"  Subject: {cert['subject']}")
            print(f"  Issuer: {cert['issuer']}")
            print(f"  Valid From: {cert['not_before']}")
            print(f"  Valid Until: {cert['not_after']}")
        
        print("\nTesting with SSL Verification Disabled:")
        if result.get("verification_disabled_works"):
            print(f"  Status Code: {result.get('unverified_status_code')}")
            print("  Request succeeded with verification disabled")
        else:
            print(f"  Error: {result.get('unverified_error')}")
    
    except Exception as e:
        logger.error(f"Error in Task 5: {e}")
        sys.exit(1)


def main():
    """Main entry point for the command-line application."""
    parser = argparse.ArgumentParser(description="Books to Scrape - Web Scraping Toolkit")
    
    parser.add_argument(
        "task",
        type=int,
        choices=range(1, 6),
        help="Task to run (1-5)"
    )
    
    parser.add_argument(
        "--max-pages",
        type=int,
        default=2,
        help="Maximum number of pages to scrape for Task 3 (default: 2)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level based on verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Execute the selected task
    task_map = {
        1: task1_get_status_and_headers,
        2: task2_extract_book_titles,
        3: lambda: task3_scrape_catalog(args.max_pages),
        4: task4_test_http_methods,
        5: task5_verify_ssl,
    }
    
    task_map[args.task]()


if __name__ == "__main__":
    main()