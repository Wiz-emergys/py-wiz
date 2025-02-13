import aiohttp
import asyncio
import csv
from urllib.parse import quote
from bs4 import BeautifulSoup
from utils.config_loader import USER_AGENT, OUTPUT_FILE, load_config
from utils.utils import safe_get
import dateparser

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
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

def get_search_url(engine: str, query: str, page: int) -> str:
    """Generate search URL for different engines"""
    query = quote(query)
    if engine == "google":
        # print(f"https://www.google.com/search?q={query}&tbm=nws&start={(page-1)*10}")
        return f"https://www.google.com/search?q={query}&tbm=nws&start={(page-1)*10}"
    
    elif engine == "bing":
        # print(f"https://www.bing.com/news/search?q={query}&first={(page-1)*10+1}")
        return f"https://www.bing.com/news/search?q={query}&first={(page-1)*10+1}"
    elif engine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={query}&b={(page-1)*10+1}"
    return ""

async def scrape_page(session: aiohttp.ClientSession, writer: csv.writer, 
                     search_str: str, engine: str, page: int):
    """
    Scrape news article details from a search engine results page.

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
    
    # Scraping logic for different search engines
    if engine == "google":
        items = soup.select("div.SoaBEf")
        for item in items:
            title = safe_get(item, "div.MBeuO, h3, h4, a.title")
            link = safe_get(item, "a", "href")
            time = safe_get(item, "div.OSrXXb span")
            media = safe_get(item, "div.MgUUmf span")
            parsed_time=dateparser.parse(time)
            time_stamo=parsed_time.isoformat() if parsed_time else "No found"
            writer.writerow([search_str, engine, link, title, time_stamo, media])
    elif engine == "bing":
        items = soup.select("div.news-card")
        for item in items:
            title = safe_get(item, "a.title",attribute="text")
            link = safe_get(item, "a", "href")
            time = safe_get(item, 'div.source span[tabindex="0"]')  
            media = safe_get(item, "div.source.set_top")
            parsed_time=dateparser.parse(time)
            time_stamo=parsed_time.isoformat() if parsed_time else "No found"
            writer.writerow([search_str, engine, link, title, time_stamo, media])
    elif engine == "yahoo":
        items = soup.select("div.NewsArticle")
        for item in items:
            title = safe_get(item, "h4.s-title a")
            link = safe_get(item, "a", "href")
            time = safe_get(item, "span.s-time, span.time, time")
            media = safe_get(item, "span.s-source")
            parsed_time=dateparser.parse(time)
            time_stamo=parsed_time.isoformat() if parsed_time else "No found"
            writer.writerow([search_str, engine, link, title, time_stamo, media])

async def scrape_results():
    
    """
    Scrape news results from specified search engines for all companies and keywords in the config file.

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
    config = load_config()
    async with aiohttp.ClientSession() as session:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Search String", "Search Engine", "Link", "Title", "Time", "Media"])
            
            tasks = []
            for company in config["companies"]:
                for keyword in config["keywords"]:
                    search_str = f"{company} {keyword}"
                    for engine in ["google", "bing", "yahoo"]:
                        for page in range(1, config["pages"] + 1):
                            tasks.append(
                                scrape_page(session, writer, search_str, engine, page)
                            )
            await asyncio.gather(*tasks)