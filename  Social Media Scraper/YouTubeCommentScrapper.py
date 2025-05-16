import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


class YouTubeCommentScraper:
    """A class to scrape comments from YouTube videos."""

    def __init__(self, url, max_comments=10):
        """Initialize the YouTube comment scraper.

        Args:
            url (str): The URL of the YouTube video.
            max_comments (int): Maximum number of comments to scrape.
        """
        self.url = url
        self.max_comments = max_comments
        self.comments_data = []
        self.driver = None

    def configure_driver(self):
        """Configure and initialize the Firefox WebDriver."""
        try:
            # Configure Firefox options
            firefox_options = Options()

            # Set user agent to avoid detection
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
            firefox_options.set_preference("general.useragent.override", user_agent)

            # Create Firefox driver instance
            self.driver = webdriver.Firefox(options=firefox_options)

            print("Firefox WebDriver configured successfully")
            return True
        except Exception as e:
            print(f"Error configuring WebDriver: {str(e)}")
            return False

    def navigate_to_page(self):
        """Navigate to the target YouTube video page."""
        try:
            # Load the YouTube video page
            self.driver.get(self.url)

            # Wait for page to fully load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print(f"Successfully navigated to {self.url}")
            return True
        except Exception as e:
            print(f"Error navigating to page: {str(e)}")
            return False

    def scroll_to_comments(self):
        """Scroll down to the comments section."""
        try:
            # Initial scroll to make comments visible
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(3)  # Wait for scroll to complete

            # Wait for comments section to become available
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "comments"))
            )
            print("Comments section loaded successfully")
            return True
        except TimeoutException:
            print("Timeout waiting for comments section to load")
            return False
        except Exception as e:
            print(f"Error scrolling to comments: {str(e)}")
            return False

    def _extract_author(self, comment_element):
        """Extract author name from comment element using multiple fallback methods."""
        try:
            # Method 1: Using header-author ID
            author_element = comment_element.find_element(By.CSS_SELECTOR, "#header-author")
            return author_element.text.split('\n')[0]
        except NoSuchElementException:
            try:
                # Method 2: Using author-text or author-comment-badge
                author_element = comment_element.find_element(
                    By.CSS_SELECTOR, "#author-text, span[id='author-comment-badge']"
                )
                return author_element.text
            except NoSuchElementException:
                try:
                    # Method 3: Using channel name selectors
                    author_element = comment_element.find_element(
                        By.CSS_SELECTOR, "#channel-name, span[id='name'], .yt-channel-name"
                    )
                    return author_element.text
                except NoSuchElementException:
                    return "Unknown Author"

    def _extract_comment_text(self, comment_element):
        """Extract comment text using multiple fallback methods."""
        try:
            # Method 1: Using formatted string selector
            comment_text_element = comment_element.find_element(
                By.CSS_SELECTOR, "#text.yt-formatted-string, .yt-formatted-string[id='text']"
            )
            return comment_text_element.text
        except NoSuchElementException:
            try:
                # Method 2: Using content-text selector
                comment_text_element = comment_element.find_element(
                    By.CSS_SELECTOR, "#content-text, .yt-attributed-string[id='content-text']"
                )
                return comment_text_element.text
            except NoSuchElementException:
                try:
                    # Method 3: Using core attributed string classes
                    comment_text_element = comment_element.find_element(
                        By.CSS_SELECTOR,
                        ".yt-core-attributed-string, .yt-core-attributed-string--white-space-pre-wrap"
                    )
                    return comment_text_element.text
                except NoSuchElementException:
                    return "Comment text not found"

    def _extract_like_count(self, comment_element):
        """Extract like count from comment element."""
        try:
            like_element = comment_element.find_element(
                By.CSS_SELECTOR, "#vote-count-middle, .comment-vote-count"
            )
            like_count = like_element.text.strip()
            return like_count if like_count else "0"
        except NoSuchElementException:
            return "0"

    def extract_comments(self):
        """Extract comments from the YouTube video page."""
        try:
            # Wait for comment threads to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-thread-renderer"))
            )

            comments_collected = 0

            # Continue scrolling and collecting until we reach max_comments
            while comments_collected < self.max_comments:
                # Get all comment elements currently loaded
                comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")

                # Process only the new comments we haven't collected yet
                for comment_element in comment_elements[comments_collected:]:
                    if comments_collected >= self.max_comments:
                        break

                    try:
                        # Extract comment data using helper methods
                        author = self._extract_author(comment_element)
                        comment_text = self._extract_comment_text(comment_element)
                        like_count = self._extract_like_count(comment_element)

                        # Add the data to our collection
                        self.comments_data.append({
                            "author": author,
                            "text": comment_text,
                            "likes": like_count
                        })

                        comments_collected += 1
                        print(f"Collected comment {comments_collected}/{self.max_comments}")

                    except StaleElementReferenceException:
                        # Handle stale elements (DOM changes during processing)
                        print("Stale element encountered, skipping and continuing")
                        continue
                    except Exception as e:
                        print(f"Error extracting comment data: {str(e)}")
                        continue

                # If we need more comments, scroll down to load more
                if comments_collected < self.max_comments:
                    # Scroll down to trigger loading of more comments
                    self.driver.execute_script("window.scrollBy(0, 1000);")
                    # Add random delay to avoid detection
                    time.sleep(random.uniform(2, 4))

            print(f"Successfully collected {len(self.comments_data)} comments")
            return True
        except Exception as e:
            print(f"Error extracting comments: {str(e)}")
            return False

    def save_to_csv(self, filename="youtube_comments.csv"):
        """Save the collected comments data to a CSV file."""
        try:
            # Verify we have data to save
            if not self.comments_data:
                print("No comment data available to save")
                return False

            # Define CSV headers
            headers = ["author", "text", "likes"]

            # Write data to CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for comment in self.comments_data:
                    writer.writerow(comment)

            print(f"Data successfully saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving data to CSV: {str(e)}")
            return False

    def cleanup(self):
        """Close the browser and cleanup resources."""
        try:
            if self.driver:
                self.driver.quit()
                print("WebDriver closed successfully")
        except Exception as e:
            print(f"Error closing WebDriver: {str(e)}")

    def run(self):
        """Run the complete scraping process."""
        try:
            # Step 1: Configure and initialize WebDriver
            if not self.configure_driver():
                return False

            # Step 2: Navigate to the YouTube video page
            if not self.navigate_to_page():
                self.cleanup()
                return False

            # Step 3: Wait for page to load completely
            time.sleep(random.uniform(3, 5))

            # Step 4: Scroll to comments section
            if not self.scroll_to_comments():
                self.cleanup()
                return False

            # Step 5: Extract comments
            if not self.extract_comments():
                self.cleanup()
                return False

            # Step 6: Save data to CSV
            if not self.save_to_csv():
                self.cleanup()
                return False

            # Step 7: Cleanup resources
            self.cleanup()
            return True

        except Exception as e:
            print(f"An error occurred during the scraping process: {str(e)}")
            self.cleanup()
            return False


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=fx2Z5ZD_Rbo&ab_channel=SpritePix"
    max_comments = 20

    # Create and run the scraper
    scraper = YouTubeCommentScraper(video_url, max_comments)
    success = scraper.run()

    if success:
        print("YouTube comment scraping completed successfully.")
    else:
        print("YouTube comment scraping encountered errors.")