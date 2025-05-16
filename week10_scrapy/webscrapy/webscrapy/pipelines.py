# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd



class WebscrapyPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        item['name'] = item['name'].strip()

        # Remove currency symbol and convert to float
        item['price'] = float(item['price'].replace('£', '').strip())

        # Store cleaned item for later sorting
        self.items.append(item)
        return item

    def close_spider(self, spider):
        # Sort items by price and convert to list of dicts
        self.items.sort(key=lambda x: x['price'])
        items_as_dicts = [dict(item) for item in self.items]

        with open('data/books_sorted.json', 'w', encoding='utf-8') as f:
            json.dump(items_as_dicts, f, ensure_ascii=False, indent=2)

        df = pd.DataFrame(items_as_dicts)
        df.to_csv('data/books_sorted.csv', index=False, encoding='utf-8')
