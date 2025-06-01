import argparse
from typing import Optional
import sys
from loguru import logger

from amazon_scraper import AmazonScraper
from data_manager import DataManager
from config import MIN_PRODUCTS, MIN_PAGES

def setup_logging():
    """Configure logging settings."""
    logger.remove()  # Remove default handler
    logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    logger.add("../logs/scraper.log", rotation="500 MB")

def scrape_products(search_term: str, min_products: Optional[int] = MIN_PRODUCTS, min_pages: Optional[int] = MIN_PAGES):
    """Main function to scrape products."""
    data_manager = DataManager()
    
    with AmazonScraper(search_term) as scraper:
        logger.info(f"Starting scraping for search term: {search_term}")
        scraper.start_scraping()
        
        page_count = 0
        product_count = 0
        
        while True:
            page_count += 1
            logger.info(f"Scraping page {page_count}")
            
            # Get all product elements on the current page
            product_elements = scraper.get_product_elements()
            
            # Process each product
            for element in product_elements:
                product = scraper.extract_product_info(element)
                if product:
                    data_manager.add_product(product)
                    product_count += 1
                    logger.info(f"Scraped product {product_count}: {product.name}")
            
            # Check if we've collected enough products and pages
            if product_count >= min_products and page_count >= min_pages:
                logger.info("Reached minimum products and pages requirement")
                break
                
            # Try to go to next page
            if not scraper.navigate_to_next_page():
                logger.info("No more pages available")
                break
    
    # Save the collected data
    logger.info("Saving collected data...")
    data_manager.save_to_csv()
    data_manager.save_to_json()
    
    # Generate and save analysis
    logger.info("Generating analysis...")
    analysis = data_manager.generate_analysis()
    data_manager.save_analysis(analysis)
    
    logger.info(f"Scraping completed. Total products collected: {product_count}")
    return product_count

def main():
    """Entry point of the script."""
    parser = argparse.ArgumentParser(description="Product catalog scraper")
    parser.add_argument("search_term", help="Search term for products")
    parser.add_argument("--min-products", type=int, default=MIN_PRODUCTS,
                      help=f"Minimum number of products to collect (default: {MIN_PRODUCTS})")
    parser.add_argument("--min-pages", type=int, default=MIN_PAGES,
                      help=f"Minimum number of pages to scrape (default: {MIN_PAGES})")
    
    args = parser.parse_args()
    
    setup_logging()
    try:
        scrape_products(args.search_term, args.min_products, args.min_pages)
    except KeyboardInterrupt:
        logger.warning("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 