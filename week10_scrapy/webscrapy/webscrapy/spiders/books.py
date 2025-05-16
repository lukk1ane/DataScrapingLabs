import scrapy
from ..items import WebscrapyItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = WebscrapyItem()
            item['name'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('.price_color::text').get()
            yield item

        # Follow pagination link if it exists
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

"""
# Export to CSV
scrapy crawl books -o data/books.csv

# Export to JSON
scrapy crawl books -o data/books.json
"""
