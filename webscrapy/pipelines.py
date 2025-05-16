# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapyPipeline:

    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        item['title'] = item['title'].strip()

        item['price'] = float(item['price'].replace('£', '').strip())

        self.items.append(item)
        return item

    def close_spider(self, spider):
        sorted_items = sorted(self.items, key=lambda x: x['price'])

        import json
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump([dict(item) for item in sorted_items], f, indent=2)

        import csv
        with open('books.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'price'])
            writer.writeheader()
            writer.writerows(sorted_items)
