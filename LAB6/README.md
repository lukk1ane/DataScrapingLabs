# LAB6 - Web Scraping with Selenium

## Requirements

- Python 3.x
- Selenium
- Chrome browser (already installed)
- Pillow (optional, for image processing in task4)
- pandas (for data handling in task2)

## Installation

Since you're using Arch Linux and already have Selenium installed, you only need to install the additional dependencies:

```bash
pip install pandas pillow
```

## Scripts Overview

1. **task1_login.py**: Opens swoop.ge and interacts with the login form (with proper Georgian language support)
2. **task2_scrape_data.py**: Navigates through multiple pages and scrapes product data
3. **task3_apply_filters.py**: Applies category filters and waits for results to reload
4. **task4_check_images.py**: Checks if product images are loaded and saves screenshots
5. **bonus_pagination.py**: Handles dynamic pagination and detects when new products load

## Running the Scripts

To run any of the scripts, use:

```bash
python LAB6/script_name.py
```

For example:

```bash
python LAB6/task1_login.py
```
## Notes

- The scripts use a robust approach to handle different HTML structures on the site
- Screenshots from task4 will be saved in the LAB6/screenshots directory
- The scripts include proper waits and error handling to manage dynamic content loading
- I didn't include the Selenium WebDriver installation in the script since it's already installed on Linux; you may need to adjust the setup for Windows.
## Task Description

These scripts fulfill the requirements specified in `task.md`:

1. Opening the homepage, navigating to login section, and filling username/password fields
2. Navigating through multiple pages and scraping product data
3. Applying category filters and using explicit waits
4. Checking if images are loaded and saving screenshots
5. Handling dynamic pagination (bonus task) 