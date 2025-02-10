import aiohttp
import asyncio
import csv
from urllib.parse import quote
from bs4 import BeautifulSoup
from utils.config_loader import USER_AGENT, OUTPUT_FILE, load_config
from utils.utils import safe_get

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch URL content"""
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
        return f"https://www.google.com/search?q={query}&tbm=nws&start={(page-1)*10}"
    elif engine == "bing":
        return f"https://www.bing.com/news/search?q={query}&first={(page-1)*10+1}"
    elif engine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={query}&b={(page-1)*10+1}"
    return ""

async def scrape_page(session: aiohttp.ClientSession, writer: csv.writer, 
                     search_str: str, engine: str, page: int):
    """Scrape a single page of results"""
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
            writer.writerow([search_str, engine, link, title, time, media])
    
    elif engine == "bing":
        items = soup.select("div.news-card")
        for item in items:
            title = safe_get(item, "div.snippet", "title")
            link = safe_get(item, "a", "href")
            time = safe_get(item, 'div.source span[tabindex="0"]')
            media = safe_get(item, "div.source.set_top")
            writer.writerow([search_str, engine, link, title, time, media])
    
    elif engine == "yahoo":
        items = soup.select("div.NewsArticle")
        for item in items:
            title = safe_get(item, "h4.s-title a")
            link = safe_get(item, "a", "href")
            time = safe_get(item, "span.s-time, span.time, time")
            media = safe_get(item, "span.s-source")
            writer.writerow([search_str, engine, link, title, time, media])

async def scrape_results():
    """Main scraping function"""
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