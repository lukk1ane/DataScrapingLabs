# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WebsrcapyPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Clean product name
        if 'name' in adapter:
            adapter['name'] = adapter['name'].strip()
        # Remove currency sign and convert price to float
        if 'price' in adapter:
            price = adapter['price'].replace('£', '').strip()
            try:
                adapter['price'] = float(price)
            except ValueError:
                adapter['price'] = price
        self.items.append(dict(adapter))
        return item  # Don't yield yet, will yield in close_spider

    def close_spider(self, spider):
        # Sort items by price
        sorted_items = sorted(self.items, key=lambda x: x.get('price', float('inf')))
        for item in sorted_items:
            spider.crawler.engine.scraper._itemproc_scraped(item, spider)
