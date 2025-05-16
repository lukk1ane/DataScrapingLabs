# bookscraper/pipelines.py
from itemadapter import ItemAdapter
import re

class BookDataCleanerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 1. Strip extra whitespace from product names
        if adapter.get('name'):
            adapter['name'] = adapter['name'].strip()

        # 2. Remove currency sign from price and convert to float
        if adapter.get('price'):
            price_str = adapter['price']
            # Remove currency symbols (£, $, € etc.) and convert to float
            price_str_cleaned = re.sub(r'[^\d\.]', '', price_str)
            try:
                adapter['price'] = float(price_str_cleaned)
            except ValueError:
                spider.logger.warning(f"Could not convert price to float: {price_str}")
                adapter['price'] = None # Or set to 0.0, or keep original

        # 3. Clean availability (already done well in spider, but can be refined here if needed)
        if adapter.get('availability'):
             adapter['availability'] = adapter['availability'].strip()


        # Note: "sort prices in ascending order"
        # An item pipeline processes items ONE BY ONE. It cannot sort the entire collection
        # of prices from all items. Sorting is typically done AFTER all items are collected,
        # e.g., when processing the final CSV/JSON file, or if you were storing them in a database.
        # The pipeline ensures the 'price' field is a clean float, suitable for later sorting.

        return item
