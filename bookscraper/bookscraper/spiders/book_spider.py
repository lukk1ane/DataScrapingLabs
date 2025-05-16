import scrapy
from ..items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BookItem()
            item['title'] = book.css("h3 a::attr(title)").get()
            item['price'] = book.css(".price_color::text").get()
            yield item

        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
