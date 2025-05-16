import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# Middleware to handle Selenium requests
class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)  # Allow JavaScript to render
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def close(self):
        self.driver.quit()


# Item definition
class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()


# Spider implementation
class BooksSpider(scrapy.Spider):
    name = "books"
    custom_settings = {
        'FEEDS': {
            'books.json': {'format': 'json', 'indent': 4},
            'books.csv': {'format': 'csv'}
        }
    }

    def start_requests(self):
        yield scrapy.Request("https://books.toscrape.com/")

    def parse(self, response):
        for book in response.css('article.product_pod'):
            yield BookItem(
                title=book.css('h3 a::attr(title)').get().strip(),
                price=float(book.css('p.price_color::text').get().replace('£', ''))
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


# Pipeline for sorting
class PriceSorterPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        self.items.sort(key=lambda x: x['price'])


# Run the spider
process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {'__main__.PriceSorterPipeline': 100},
    'DOWNLOADER_MIDDLEWARES': {'__main__.SeleniumMiddleware': 543},
    'ROBOTSTXT_OBEY': True
})
process.crawl(BooksSpider)
process.start()