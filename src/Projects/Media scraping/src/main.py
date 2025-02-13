import asyncio
import time
from utils.get_user_input import get_user_input
from utils.scraper import main

if __name__ == "__main__":
    """main function to scrape news results from user provided article links."""
    urls = get_user_input()
    start = time.time()
    asyncio.run(main(urls))
    print(f"Execution time: {time.time() - start:.2f} seconds")
  