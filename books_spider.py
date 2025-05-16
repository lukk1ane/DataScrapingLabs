import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import json

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()

class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    start_urls = ['https://books.toscrape.com/']
    collected_items = []

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            title = book.css('h3 a::attr(title)').get().strip()
            price = book.css('.price_color::text').get().replace('£', '').strip()
            price = float(price)
            self.collected_items.append({'title': title, 'price': price})
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        sorted_items = sorted(self.collected_items, key=lambda x: x['price'])
        with open('books_sorted.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'price'])
            writer.writeheader()
            writer.writerows(sorted_items)
        with open('books_sorted.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_items, f, indent=4)

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
        "USER_AGENT": "Mozilla/5.0",
    })
    process.crawl(BooksSpider)
    process.start()
