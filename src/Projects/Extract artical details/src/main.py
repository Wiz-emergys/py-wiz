import os
import time
import asyncio
from utils.config_loader import CONFIG_FILE, get_user_input, OUTPUT_FILE
from utils.scraper import scrape_results

def main():
    """Main entry point"""
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