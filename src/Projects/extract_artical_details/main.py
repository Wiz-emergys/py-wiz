# Python Assignment
# Objectives:
# 1. Extract the article details from the news section of the following search engines – Google, Yahoo 
# and Bing.
# Input:
# 1. Input should be a config file in json format with the following contenta. List of company names - e.g: Tata, Jio, Apple, etc.
# b. List of key words to be associated with the company name like Lawsuits, merger, 
# bankruptcy, etc. You can choose any word that will give the output.
# c. The number of pages to be extracted will also be a parameter in the config file.
# d. The number of elements in both the lists will be dynamic.
# e. For the search strings, each company name will be associated with all the keywords 
# from the second list.
# Output format:
# 1. Excel/CSV file.
# 2. Columns – Search string (Tata and lawsuits), Search engine (google/yahoo), Link 
# (article link), Title, Time stamp, Media name.
# Expectations (from higher to lower priority):
# 1. All the functionality is achieved.
# 2. Clean and readable code with appropriate comments.
# 3. Time efficient code.


import json
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import quote

# ======== CONFIG ========
CONFIG_FILE = "config.json"
OUTPUT_FILE = "news_results.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# ========================

def get_search_url(engine, query, page):
    """Create search URL for different engines"""
    query = quote(query)
    
    if engine == "google":
        return f"https://www.google.com/search?q={query}&tbm=nws&start={(page-1)*10}"
    elif engine == "bing":
        return f"https://www.bing.com/news/search?q={query}&first={(page-1)*10 + 1}"
    elif engine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={query}&b={(page-1)*10 + 1}"
    else:
        raise ValueError("Invalid search engine")

def scrape_results():
    # Load configuration
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    
    # Prepare CSV file
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Search String", "Search Engine", "Link", "Title", "Time stamp", "Media name"])

        # Process all combinations
        for company in config["companies"]:
            for keyword in config["keywords"]:
                search_str = f"{company} {keyword}"
                
                for engine in ["google", "bing", "yahoo"]:
                    for page in range(1, config["pages"] + 1):
                        url = get_search_url(engine, search_str, page)
                        
                        try:
                            # Fetch page
                            response = requests.get(
                                url, 
                                headers={"User-Agent": USER_AGENT},
                                timeout=10
                            )
                            response.raise_for_status()
                            
                            # Parse results
                            soup = BeautifulSoup(response.text, "html.parser")
                            
                            if engine == "google":
                                items = soup.find_all("div", class_="SoaBEf")
                                for item in items:
                                    title = item.find("h3").get_text()
                                    link = item.find("a")["href"]
                                    time = item.find("div", class_="OSrXXb").get_text()
                                    media = item.find("div", class_="CEMjEf").get_text()
                                    writer.writerow([search_str, engine, link, title, time, media])
                                    
                            elif engine == "bing":
                                items = soup.find_all("div", class_="news-card")
                                for item in items:
                                    title = item.find("a", class_="title").get_text()
                                    link = item.find("a", class_="title")["href"]
                                    time = item.find("span", class_="time").get_text()
                                    media = item.find("div", class_="source").get_text()
                                    writer.writerow([search_str, engine, link, title, time, media])
                                    
                            elif engine == "yahoo":
                                items = soup.find_all("div", class_="NewsArticle")
                                for item in items:
                                    title = item.find("h4").get_text()
                                    link = item.find("a")["href"]
                                    time = item.find("span", class_="time").get_text()
                                    media = item.find("span", class_="source").get_text()
                                    writer.writerow([search_str, engine, link, title, time, media])
                                    
                        except Exception as e:
                            print(f"Error scraping {engine} page {page}: {str(e)}")
                            continue

if __name__ == "__main__":
    scrape_results()
    print(f"Scraping completed! Results saved to {OUTPUT_FILE}")