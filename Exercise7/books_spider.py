import scrapy
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from scrapy import signals
import csv
import json


class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # For sorting prices
    items = []

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            item = {
                'title': book.css('h3 a::attr(title)').get().strip(),
                'price': float(book.css('div.product_price p.price_color::text').get().replace('£', '')),
                'rating': book.css('p.star-rating::attr(class)').get().split()[-1],
                'availability': book.css('div.product_price p.instock.availability::text').getall()[1].strip()
            }
            self.items.append(item)
            yield item

        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            if 'catalogue/' not in next_page:
                next_page = 'catalogue/' + next_page
            yield response.follow(next_page, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BookSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        # Sort items by price in ascending order
        sorted_items = sorted(self.items, key=lambda x: x['price'])

        # Save to JSON
        with open('books_sorted.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_items, f, indent=4, ensure_ascii=False)

        # Save to CSV
        with open('books_sorted.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating', 'availability'])
            writer.writeheader()
            writer.writerows(sorted_items)