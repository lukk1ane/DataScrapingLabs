from scrapy.exporters import CsvItemExporter, JsonItemExporter

class BooksScraperPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'].strip()
        item['price'] = float(item['price'].replace('£', '').strip())
        return item

class SortAndExportPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        sorted_items = sorted(self.items, key=lambda x: x['price'])

        # Export to CSV
        with open('books_sorted.csv', 'wb') as f:
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            for item in sorted_items:
                exporter.export_item(item)
            exporter.finish_exporting()

        # Export to JSON
        with open('books_sorted.json', 'wb') as f:
            exporter = JsonItemExporter(f, encoding='utf-8', ensure_ascii=False)
            exporter.start_exporting()
            for item in sorted_items:
                exporter.export_item(item)
            exporter.finish_exporting()
