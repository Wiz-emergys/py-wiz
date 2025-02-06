
import logging
import re
import aiohttp
from bs4 import BeautifulSoup
import html2text
import os
from aiohttp import ClientSession
from urllib.parse import urlparse
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)

extracted_dir = os.path.join(project_root, "extracted_content")
os.makedirs(extracted_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(logs_dir, 'runtime.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

articales={
    'indianexpress.com':('h1[itemprop="headline"]' ,'div.full-details'),
    'www.thehindu.com':('div.storyline h1.title','div.storyline div.articlebodycontent[itemprop="articleBody"]'),
    'www.bbc.com': ('h1.sc-518485e5-0.bWszMR', 'p.sc-eb7bd5f6-0.fYAfXe')

}


def clean_filename(title):
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title, content, domain):
    """Save content to markwn file with proper structure"""
    try:
        filename = f"{domain}_{clean_filename(title)}.md"
        filepath = os.path.join(extracted_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{content}")
        logging.info(f"Successfully saved article: {filename}")
        return True
    except Exception as e:
        logging.error(f"Save failed: {str(e)}")
        return False
    
async def scrape_article(session: aiohttp.ClientSession, url: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        domain = urlparse(url).netloc
        selectors = articales.get(domain)
        
        if not selectors:
            logging.error(f"No selected configured for domain {domain}")
            return False

        title_selector,content_selector=selectors

        async with session.get(url, headers=headers, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

        soup = BeautifulSoup(html, 'lxml')
        
        # Extract title
        title_element = soup.select_one(title_selector)
        if not title_element:
            raise ValueError("Title element not found")
        title = title_element.get_text().strip()
        
        if domain == "www.bbc.com":
            content_element = soup.select(content_selector)
            if not content_element:
                raise ValueError("Content element not found")
            # Convert to markdown
            
            filename = f"{clean_filename(title)}.md"
            filepath = os.path.join(extracted_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(f"# {title}\n\n")
                for content in content_element:
                    converter = html2text.HTML2Text()
                    converter.ignore_links = True
                    converter.ignore_images = False
                    md_content = converter.handle(str(content))
                    md_content= md_content.replace('_', "") 
                    file.write(f"{md_content}")
                logging.info(f"Successfully scraped article from: {url}")
        else:
            # Extract content
            content_element = soup.select_one(content_selector)
            if not content_element:
                raise ValueError("Content element not found")
                
            # Clean unnecessary elements
            for elem in content_element.select('.also-read, .ad-container, script, style'):
                elem.decompose()
                
            # Convert to markdown
            converter = html2text.HTML2Text()
            converter.ignore_links = True
            converter.ignore_images = False
            md_content = converter.handle(str(content_element))
            md_content= md_content.replace('_', "")
            
            # Get domain name
            domain_name = domain.split('.')[-2]
            
            # Save article
            if save_article(title, md_content, domain_name):
                logging.info(f"Successfully scraped article from: {url}")
                return True
            return False
        
    except Exception as e:
        logging.error(f"Error scraping {url}: {str(e)}")
        return False
    
async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks=[scrape_article(session,url) for url in urls]
        results=await asyncio.gather(*tasks,return_exceptions=True)

    for result,url in zip(results,urls):
        if isinstance(result,Exception):
            logging.error(f"Task failed for url : {url} and result : {result}")    
        elif not result:
            logging.error(f"Task failed for url {url}..")


if __name__ == "__main__":
    urls=[
        "https://indianexpress.com/article/technology/tech-news-technology/china-announces-measures-against-google-other-us-firms-as-trade-tensions-escalate-9816925/?ref=shrt_article_readfull",
        "https://www.thehindu.com/sport/football/premier-league-arsenal-hammer-man-city-5-1-to-stay-in-title-hunt/article69173901.ece" ,
        "https://www.bbc.com/news/articles/c0rqxpg2ryvo",
    ]
    asyncio.run(main(urls))

 