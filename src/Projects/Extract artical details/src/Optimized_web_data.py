import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
from urllib.parse import quote
import time

# ======== CONFIG ========
CONFIG_FILE = r"C:\Users\NikhilJain\py-wiz\src\Projects\Extract artical details\src\config.json"
OUTPUT_FILE = "news_results.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# ========================

start = time.time()


def safe_get(element, selector, attribute="text"):
    """Safely extract data from HTML element"""
    result = element.select_one(selector)
    if result:
        if attribute == "text":
            return result.get_text(strip=True)
        return result.get(attribute, "")
    return ""


def get_search_url(engine, query, page):
    query = quote(query)
    if engine == "google":
        return f"https://www.google.com/search?q={query}&tbm=nws&start={(page - 1) * 10}"
    elif engine == "bing":
        return f"https://www.bing.com/news/search?q={query}&first={(page - 1) * 10 + 1}"
    elif engine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={query}&b={(page - 1) * 10 + 1}"
    return ""


async def fetch(session, url):
    """Fetch the URL asynchronously"""
    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}, timeout=25) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def scrape_page(session, writer, search_str, engine, page):
    """Scrape a single page asynchronously"""
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
    """Main scraping function"""
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
    asyncio.run(scrape_results())
    print(f"Scraping completed! Results saved to {OUTPUT_FILE}")
    print("Total time:", time.time() - start)
