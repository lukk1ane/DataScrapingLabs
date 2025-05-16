# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class Lab7Pipeline:
    def process_item(self, item, spider):
        return item

class BooksPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Strip whitespace from product name
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()
        
        # Remove currency sign and convert to float for sorting
        if adapter.get('price'):
            adapter['price'] = float(re.sub(r'[^\d.]', '', adapter['price']))
            
        return item

class PriceSortPipeline:
    items = []
    
    def process_item(self, item, spider):
        self.items.append(item)
        return item
    
    def close_spider(self, spider):
        # Sort items by price in ascending order
        self.items.sort(key=lambda x: x['price'])
        
        # You can use the sorted items here if needed
        # For example, write to a special sorted file
        for item in self.items:
            spider.logger.info(f"Sorted item: {item['title']} - {item['price']}")
