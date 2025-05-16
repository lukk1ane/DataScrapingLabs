BOT_NAME = 'bookscraper'

SPIDER_MODULES = ['bookscraper.spiders']
NEWSPIDER_MODULE = 'bookscraper.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'bookscraper.pipelines.BookPipeline': 300,
}

SPIDER_MIDDLEWARES = {
    'bookscraper.middlewares.BookscraperSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'bookscraper.middlewares.BookscraperDownloaderMiddleware': 543,
}

FEEDS = {
    'output/books.json': {'format': 'json', 'encoding': 'utf8', 'indent': 4},
    'output/books.csv': {'format': 'csv'},
}
