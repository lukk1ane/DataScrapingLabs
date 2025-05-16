import scrapy

class BookscraperItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()