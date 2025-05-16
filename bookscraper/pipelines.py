from itemadapter import ItemAdapter

class BookPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Remove currency sign and convert to float
        price = adapter.get('price').replace('£', '').strip()
        adapter['price'] = float(price)
        # Strip extra whitespace from title
        adapter['title'] = adapter['title'].strip()
        return item
