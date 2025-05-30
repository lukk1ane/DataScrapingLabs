# LAB9: Web Scraping Performance Comparison and Asynchronous Scraping

This lab contains two tasks that demonstrate different approaches to web scraping, comparing performance and implementing asynchronous techniques.

## Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Task 1: Sequential vs Threaded vs Multiprocessing Scraping

**File:** `task1.py`

**Description:** Compares three different approaches to scrape the first 10 pages of quotes from http://quotes.toscrape.com:
- Sequential scraping (one request at a time)
- Threaded scraping using ThreadPoolExecutor with 5 threads
- Multiprocessing scraping using multiprocessing.Pool with 5 processes

**Features:**
- Measures and prints total execution time for each approach
- Calculates average time per request (page)
- Extracts quote text, author, and tags for each quote
- Provides detailed performance comparison and speedup analysis
- Robust error handling for network issues

**Usage:**
```bash
cd LAB9
python task1.py
```

**Expected Output:**
- Progress updates for each scraping method
- Performance metrics for each approach
- Speedup comparison between methods
- Total quotes scraped from all pages

## Task 2: Asynchronous Book Scraping with Rate Limiting

**File:** `task2.py`

**Description:** Creates an asynchronous script that scrapes book information from https://books.toscrape.com/ using asyncio and aiohttp. The script:
- Scrapes all books from all pages of the website
- Implements proper rate limiting (max 5 requests per second)
- Extracts title, price, and product page URL for each book
- Saves results to a JSON file
- Prints task duration and performance metrics

**Features:**
- Asynchronous HTTP requests using aiohttp
- Custom rate limiter class to respect server limits
- Automatic pagination handling
- JSON output with proper UTF-8 encoding
- Comprehensive error handling and logging
- Performance metrics and sample results display

**Usage:**
```bash
cd LAB9
python task2.py
```

**Output Files:**
- `books_data.json`: Contains all scraped book information

**Expected Output:**
- Real-time progress updates for each page
- Total pages scraped and books found
- Performance metrics (duration, books per second)
- Sample of first 5 books found
- Confirmation of JSON file creation

## Key Learning Objectives

1. **Performance Comparison**: Understanding the performance differences between:
   - Sequential processing
   - Thread-based concurrency (I/O bound tasks)
   - Process-based parallelism

2. **Asynchronous Programming**: 
   - Using asyncio and aiohttp for efficient concurrent HTTP requests
   - Implementing custom rate limiting
   - Proper async resource management with context managers

3. **Web Scraping Best Practices**:
   - Respectful scraping with rate limiting
   - Robust error handling
   - Efficient data extraction with BeautifulSoup
   - Proper URL handling and navigation

4. **Data Management**:
   - Structured data extraction
   - JSON serialization
   - Performance monitoring and metrics

## Performance Expectations

**Task 1:** You should see significant speedup with threaded and multiprocessing approaches compared to sequential scraping, especially for I/O-bound web scraping tasks.

**Task 2:** The asynchronous approach should efficiently handle the rate limiting while maintaining good performance, typically scraping all books in a reasonable time while respecting the 5 requests/second limit.

## Notes

- Both scripts include comprehensive error handling for network issues
- The rate limiter in Task 2 ensures respectful scraping practices
- All timing measurements account for both request time and processing time
- The scripts are designed to be educational and demonstrate best practices in web scraping 