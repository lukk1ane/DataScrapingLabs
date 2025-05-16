import scrapy
from LAB7.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    
    def parse(self, response):
        """
        Parse the main page and extract book information.
        Follow pagination links to next pages.
        """
        # Extract books from current page
        books = response.css('article.product_pod')
        for book in books:
            book_url = book.css('h3 a::attr(href)').get()
            if book_url is not None:
                # Fix URL construction to avoid duplicate catalogue/ path
                book_url = response.urljoin(book_url)
                yield scrapy.Request(book_url, callback=self.parse_book)
        
        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
    
    def parse_book(self, response):
        """
        Parse individual book page to extract detailed information.
        """
        book_item = BookItem()
        
        # Extract book data
        book_item['title'] = response.css('div.product_main h1::text').get()
        book_item['price'] = response.css('p.price_color::text').get()
        book_item['image_url'] = response.urljoin(response.css('div.item.active img::attr(src)').get())
        book_item['availability'] = response.css('p.availability::text').getall()[-1].strip()
        
        # Extract rating (convert text rating to numerical)
        rating_class = response.css('p.star-rating::attr(class)').get()
        if rating_class:
            rating_text = rating_class.split()[-1]
            ratings_map = {
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
            }
            book_item['rating'] = ratings_map.get(rating_text, 0)
        
        # Extract category from breadcrumbs
        category = response.css('ul.breadcrumb li:nth-child(3) a::text').get()
        book_item['category'] = category.strip() if category else 'Unknown'
        
        yield book_item 