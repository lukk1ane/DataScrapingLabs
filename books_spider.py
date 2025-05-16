import scrapy
from websrcapy.items import BookItem 

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BookItem()
            item['name'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()
            item['availability'] = book.css(
                'p.instock.availability::text').getall()[-1].strip()
            yield item
            # yield {
            #     'name': book.css('h3 a::attr(title)').get(),
            #     'price': book.css('p.price_color::text').get(),
            #     'availability': book.css('p.instock.availability::text').getall()[-1].strip(),
            # }
        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse) 