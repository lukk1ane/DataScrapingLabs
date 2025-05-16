import csv, json

class CleanSortPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        item['title'] = item['title'].strip()
        price = item['price'].replace('£', '')
        item['price'] = float(price)
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        self.items.sort(key=lambda x: x['price'])

        with open('data/books_sorted.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title','price'])
            writer.writeheader()
            writer.writerows(self.items)

        with open('data/books_sorted.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False)
