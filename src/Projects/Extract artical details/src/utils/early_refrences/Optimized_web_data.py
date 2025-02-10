import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
from urllib.parse import quote
import time
import os

# ======== CONFIG ========
CONFIG_FILE = r"C:\Users\NikhilJain\py-wiz\src\Projects\Extract artical details\src\config.json"
OUTPUT_FILE = "news_results.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# ========================


def get_user_input():
    """
    Get user input for companies, keywords, and number of pages to scrape and save to config.json.

    Asks user for input and saves it to the configuration file (config.json) in the same directory as
    this script. The configuration file is a JSON file with the following structure:

    {
        "companies": [
            "company1",
            "company2",
            ...
        ],
        "keywords": [
            "keyword1",
            "keyword2",
            ...
        ],
        "pages": <number of pages to scrape>
    }
    """
    
    companies = input("Enter company names (comma-separated): ").split(",")
    keywords = input("Enter keywords (comma-separated): ").split(",")
    pages = int(input("Enter the number of pages to scrape: "))

    # Trim spaces and format properly
    companies = [company.strip() for company in companies]
    keywords = [keyword.strip() for keyword in keywords]

    # Create dictionary
    config_data = {
        "companies": companies,
        "keywords": keywords,
        "pages": pages
    }

    # Save to config.json
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    
    print(f"Configuration saved to {CONFIG_FILE}")

def safe_get(element, selector, attribute="text"):
    """
    Safely extract a value from an HTML element.

    Parameters:
        element (bs4.element.Tag): The element to extract from.
        selector (str): The CSS selector to use to extract the element.
        attribute (str): The attribute to extract from the element. Defaults to "text".

    Returns:
        str: The extracted value, or empty string if the element or attribute is not found.
    """
    result = element.select_one(selector)
    if result:
        if attribute == "text":
            return result.get_text(strip=True)
        return result.get(attribute, "")
    return ""


def get_search_url(engine, query, page):
    """
    Construct a search URL for the specified search engine.

    Parameters:
        engine (str): Name of the search engine (one of "google", "bing", or "yahoo").
        query (str): The search query string.
        page (int): Page number to get results for.

    Returns:
        str: The constructed search URL.
    """
    
    query = quote(query)
    if engine == "google":
        return f"https://www.google.com/search?q={query}&tbm=nws&start={(page - 1) * 10}"
    elif engine == "bing":
        return f"https://www.bing.com/news/search?q={query}&first={(page - 1) * 10 + 1}"
    elif engine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={query}&b={(page - 1) * 10 + 1}"
    return ""


async def fetch(session, url):
    """
    Fetches the content of a URL asynchronously.

    Parameters:
        session (aiohttp.ClientSession): The client session to use for the request.
        url (str): The URL to fetch content from.

    Returns:
        str: The response text from the URL if successful, None if an error occurs.

    Raises:
        Exception: If an error occurs during the fetch operation, it is caught and printed.
    """

    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}, timeout=25) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def scrape_page(session, writer, search_str, engine, page):
    """
    Scrape and extract news article details from a search engine results page.

    Parameters:
        session (aiohttp.ClientSession): The client session to use for making HTTP requests.
        writer (csv.writer): CSV writer object to write the extracted data to a CSV file.
        search_str (str): The search string used to query the search engine.
        engine (str): The name of the search engine ("google", "bing", or "yahoo").
        page (int): The page number to scrape results from.

    Returns:
        None

    This function uses the specified search engine and page number to construct a search URL,
    fetches the page content, and parses the HTML using BeautifulSoup. It extracts article
    details such as title, link, time, and media name, and writes them to a CSV file.
    """

    url = get_search_url(engine, search_str, page)
    if not url:
        return
    
    html = await fetch(session, url)
    if not html:
        return
    
    soup = BeautifulSoup(html, "html.parser")
    
    if engine == "google":
        items = soup.select("div.SoaBEf")
        for item in items:
            title = safe_get(item, "div.MBeuO, h3, h4, a.title")
            link = safe_get(item, "a", attribute="href")
            time = safe_get(item, "div.OSrXXb span")
            media = safe_get(item, "div.MgUUmf span")
            writer.writerow([search_str, engine, link, title, time, media])
    elif engine == "bing":
        items = soup.select("div.news-card")
        for item in items:
            title = safe_get(item, "div.snippet", attribute="title")
            link = safe_get(item, "a", attribute="href")
            time = safe_get(item, 'div.source span[tabindex="0"]', attribute="text")
            media = safe_get(item, "div.source.set_top", attribute="text")
            writer.writerow([search_str, engine, link, title, time, media])
    elif engine == "yahoo":
        items = soup.select("div.NewsArticle")
        for item in items:
            title = safe_get(item, 'h4.s-title a', attribute="text")
            link = safe_get(item, "a", attribute="href")
            time = safe_get(item, "span.s-time,span.time,time")
            media = safe_get(item, "span.s-source", attribute="text")
            writer.writerow([search_str, engine, link, title, time, media])


async def scrape_results():
    """
    Asynchronously scrape news results from specified search engines for all companies and keywords in the config file.

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

    with open(CONFIG_FILE) as f:
        config = json.load(f)
    
    async with aiohttp.ClientSession() as session:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Search String", "Search Engine", "Link", "Title", "Time stamp", "Media name"])
            
            tasks = []
            for company in config["companies"]:
                for keyword in config["keywords"]:
                    search_str = f"{company} {keyword}"
                    for engine in ["google", "bing", "yahoo"]:
                        for page in range(1, config["pages"] + 1):
                            tasks.append(scrape_page(session, writer, search_str, engine, page))
            
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        get_user_input()

    # Ask user if they want to update the config
    update_choice = input("Do you want to update the config file? (yes/no): ").strip().lower()
    if update_choice == "yes":
        get_user_input()

    
    start = time.time()
    asyncio.run(scrape_results())
    print(f"Scraping completed! Results saved to {OUTPUT_FILE}")
    print("Total time:", time.time() - start)
