
import logging
import re
import aiohttp
from bs4 import BeautifulSoup
import html2text
import os
from aiohttp import ClientSession
from urllib.parse import urlparse
import asyncio
import time

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
    'indianexpress.com': ('h1[itemprop="headline"]', 'div.story_details', 'span.custom-caption img'),
    'www.thehindu.com': ('div.storyline h1.title', 'div.storyline div.articlebodycontent[itemprop="articleBody"]', 'div.picture.verticle picture source'),
    'www.bbc.com': ('h1.sc-518485e5-0.bWszMR', 'p.sc-eb7bd5f6-0.fYAfXe', "div[data-testid='hero-image'] img:not(.hide-when-no-script)")
}   

def clean_filename(title):

    """Clean a filename by replacing non-alphanumeric characters (except hyphen) with empty string, strip leading/trailing whitespace, and truncate to 50 characters. Useful for converting article titles to filenames."""
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title, content, domain):
    """
    Save article content to file with proper structure and logging.

    Parameters:
        title (str): Title of article.
        content (str): Content of article.
        domain (str): Domain of article.

    Returns:
        bool: True if saving is successful, False otherwise.
    """
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
    
    """
    Scrape article from given URL using given title and content selectors.

    Parameters:
        session (aiohttp.ClientSession): Client session to use for HTTP request.
        url (str): URL of article.

    Returns:
        bool: True if scraping is successful, False otherwise.

    Raises:
        requests.exceptions.RequestException: If request to URL fails.
        ValueError: If title or content element not found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        domain = urlparse(url).netloc
        selectors = articales.get(domain)
        
        if not selectors:
            logging.error(f"No selected configured for domain {domain}")
            return False

        title_selector, content_selector ,image_selector = selectors

        async with session.get(url, headers=headers, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

        soup = BeautifulSoup(html, 'lxml')
        
        # Extract title
        title_element = soup.select_one(title_selector)
        if not title_element:
            raise ValueError("Title element not found")
        title = title_element.get_text().strip()
        
        # Extract image URL
        image_element = soup.select_one(image_selector)
        image_url = None
        if image_element:
            image_url = image_element.get("img") or image_element.get("src") or image_element.get("data-src") or image_element.get("srcset")
            if image_url and image_url.startswith("//"):    # Handle protocol-relative URLs
                image_url = "https:" + image_url
        
        #Extract content based on website
        content_element = soup.select(content_selector) if domain == "www.bbc.com" else soup.select_one(content_selector)
        if not content_element:
            raise ValueError("Content element not found")    
                
        # Clean unnecessary elemensts
        # for elem in content_element.select('.also-read, .ad-container, script, style'):
        #     elem.decompose()
            
        # Convert to markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True

        md_content = ""

        if isinstance (content_element,list):
            for content in content_element:    
                md_content += converter.handle(str(content))
                md_content= md_content.replace('_', "")
        
        else:
            md_content = converter.handle(str(content_element))
            md_content= md_content.replace('_', "")
    
        if image_url:
            md_content = f"![Image]({image_url})\n\n" + f"\n {md_content}"

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
    
    """
    Asynchronous main function.

    This function takes a list of URLs and runs them all through the scrape_article
    function asynchronously using aiohttp. It then logs any errors and results.

    Parameters:
        urls (list): List of URLs to scrape.

    Returns:
        None
    """
    
    async with aiohttp.ClientSession() as session:
        tasks=[scrape_article(session,url) for url in urls]
        results=await asyncio.gather(*tasks,return_exceptions=True)

    for result,url in zip(results,urls):
        if isinstance(result,Exception):
            logging.error(f"Task failed for url : {url} and result : {result}")    
        elif not result:
            logging.error(f"Task failed for url {url}..")


def get_user_input():
    
    """
    Gets URLs from user input and validates them against a list of supported websites.

    Prints a list of supported websites, then prompts the user to enter article URLs one by one.
    Checks each entered URL against the list of supported websites and domain names.
    If a URL is valid, adds it to the list of URLs to scrape.
    If a URL is invalid, prints an error message and continues to the next URL.
    If no valid URLs are entered, prints a message and exits the program.

    Returns a list of validated URLs to scrape.
    """
    print("\nSupported Websites for Scraping:")
    for site in articales.keys():
        print(f"- {site}")

    urls = []
    while True:
        url = input("\nEnter an article URL (or type 'done' to finish): ").strip()
        if url.lower() == "done":
            break
        domain = urlparse(url).netloc
        if domain not in articales:
            print(f"❌ {domain} is not supported. Please enter a URL from the supported list.")
        else:
            urls.append(url)
            print(f"✅ URL added: {url}")

    if not urls:
            print("No valid URLs entered. Exiting.")
            exit()

    return urls

if __name__ == "__main__":
    urls=get_user_input()
    start=time.time()
    asyncio.run(main(urls))
    print(time.time()-start)
 