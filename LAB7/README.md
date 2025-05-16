# Books to Scrape - Scrapy Project

This Scrapy project crawls [books.toscrape.com](https://books.toscrape.com/) to extract book information including title, price, image URL, availability, and rating.

## Features

- Crawls all pages of the website using pagination
- Extracts detailed information for each book
- Processes and cleans data through item pipelines:
  - Strips whitespace from product names
  - Removes currency signs from prices
  - Sorts books by price in ascending order
- Outputs data in both CSV and JSON formats

## How to Run

1. Navigate to the Scrapy project's root directory (containing scrapy.cfg):
   ```
   cd DataScrapingLabs/LAB7
   ```

2. Run the spider:
   ```
   scrapy crawl books
   ```

   Note: The command must be run from the directory containing the scrapy.cfg file.

3. The output will be saved in two files in the same directory:
   - `books.csv` - CSV format
   - `books.json` - JSON format with pretty formatting

## Troubleshooting

If you see an error like "The crawl command is not available from this location", make sure you're running the command from the correct directory (LAB7, which contains scrapy.cfg).

## Item Pipeline

The project includes two pipelines:
- `BooksPipeline`: Cleans the data by stripping whitespace and removing currency symbols
- `PriceSortPipeline`: Sorts all items by price in ascending order

## Data Structure

Each book item contains:
- `title`: Book title
- `price`: Book price (without currency symbol)
- `image_url`: URL to the book cover image
- `category`: Book category
- `availability`: Availability status
- `rating`: Star rating (1-5) 