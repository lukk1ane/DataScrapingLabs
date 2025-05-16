# bookscraper/spiders/books.py
import scrapy
from bookscraper.items import BookscraperItem # Import the item

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"] # Start from page 1

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")

        # Select all book containers on the page
        books = response.css('article.product_pod')

        for book in books:
            item = BookscraperItem() # Create an item instance

            # Extract book name
            item['name'] = book.css('h3 a::attr(title)').get()
            if not item['name']: # Fallback if title attribute is missing
                item['name'] = book.css('h3 a::text').get()

            # Extract price
            item['price'] = book.css('div.product_price p.price_color::text').get()

            # Extract availability
            # The availability text has leading/trailing whitespace and newlines
            availability_text = book.css('div.product_price p.instock.availability::text').getall()
            # Join and strip whitespace if multiple text nodes exist (though usually just one for availability)
            item['availability'] = " ".join(text.strip() for text in availability_text if text.strip())


            # Extract rating (e.g., "star-rating Three")
            rating_class = book.css('p.star-rating::attr(class)').get()
            if rating_class:
                # Split the class string (e.g., "star-rating Three") and take the last part
                item['rating'] = rating_class.split()[-1]
            else:
                item['rating'] = None

            # Extract book URL (relative, so join with base URL)
            relative_url = book.css('h3 a::attr(href)').get()
            item['url'] = response.urljoin(relative_url)

            yield item

        # Handle pagination
        next_page_relative = response.css('li.next a::attr(href)').get()
        if next_page_relative:
            next_page_url = response.urljoin(next_page_relative)
            self.logger.info(f"Found next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("No more pages to parse.")