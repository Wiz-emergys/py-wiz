import logging
import re
import requests
from bs4 import BeautifulSoup
import html2text
import os
from urllib.parse import urlparse
import asyncio
from aiohttp import clientSession


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

def clean_filename(title):
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]


def save_article(title, content, domain):
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

def scrape_article(url, title_selector, content_selector):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract title\=
        title_element = soup.select_one(title_selector)
        if not title_element:
            raise ValueError("Title element not found")
        title = title_element.get_text().strip()
        
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
        converter.ignore_images = True
        md_content = converter.handle(str(content_element))
        md_content= md_content.replace('_', "")
        
        # Get domain name
        domain = urlparse(url).netloc.split('.')[-2]
        
        # Save article
        if save_article(title, md_content, domain):
            logging.info(f"Successfully scraped article from: {url}")
            return True
        return False
        
    except Exception as e:
        logging.error(f"Error scraping {url}: {str(e)}")
        return False
def scrape_indian_express(url):
    return scrape_article(
        url,
        title_selector='h1[itemprop="headline"]',
        content_selector='div.full-details'
    )
def scrape_the_hindu(url):
    return scrape_article(
        url,
        title_selector='div.storyline h1.title',
        content_selector='div.storyline div.articlebodycontent[itemprop="articleBody"]'
    )
if __name__ == "__main__":
    # Example usage
    ie_url = "https://indianexpress.com/article/technology/tech-news-technology/china-announces-measures-against-google-other-us-firms-as-trade-tensions-escalate-9816925/?ref=shrt_article_readfull"
    hindu_url = "https://www.thehindu.com/sport/football/premier-league-arsenal-hammer-man-city-5-1-to-stay-in-title-hunt/article69173901.ece"
    
    scrape_indian_express(ie_url)
    scrape_the_hindu(hindu_url)
 
 