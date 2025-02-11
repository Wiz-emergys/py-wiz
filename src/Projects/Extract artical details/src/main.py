import os
import time
import asyncio
from utils.config_loader import CONFIG_FILE, get_user_input, OUTPUT_FILE
from utils.scraper import scrape_results

def main():
    
    """
    Main function to scrape news results from specified search engines for all companies and keywords in the config file.

    Opens the configuration file to retrieve the list of companies, keywords, and number of pages to scrape. For each
    company and keyword combination, constructs a search string and iterates over the specified search engines and pages.
    Initiates asynchronous tasks to scrape each page using the `scrape_page` function.

    Writes the scraped results to a CSV file with the following columns:
        - Search String
        - Search Engine
        - Link
        - Title
        - Time stamp
        - Media name

    Utilizes asyncio for concurrent execution to improve efficiency.

    Raises:
        IOError: If there is an issue opening or writing to the output CSV file.
    """
    if not os.path.exists(CONFIG_FILE):
        get_user_input()
    
    update = input("Update config? (yes/no): ").strip().lower()
    if update == "yes":
        get_user_input()
    
    start = time.time()
    asyncio.run(scrape_results())
    print(f"Scraping completed! Results saved to {OUTPUT_FILE}")
    print(f"Total time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()