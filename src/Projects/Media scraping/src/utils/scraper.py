import aiohttp
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urlparse
from utils.config import articles
from utils.utils import save_article
from utils.logger import logger
import asyncio

async def scrape_article(session: aiohttp.ClientSession, url: str):
    
    """
    Scrape an article from the given URL using the corresponding selectors.

    Parameters:
        session (aiohttp.ClientSession): Client session to use for HTTP request.
        url (str): URL of article.

    Returns:
        bool: True if the article is successfully scraped and saved, False otherwise.

    Raises:
        requests.exceptions.RequestException: If request to URL fails.
        ValueError: If title or content element not found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        domain = urlparse(url).netloc
        selectors = articles.get(domain)

        if not selectors:
            logger.error(f"No selectors configured for domain {domain}")
            return False

        title_selector, content_selector, image_selector = selectors

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
            if image_url and image_url.startswith("//"):  
                image_url = "https:" + image_url

        # Extract content
        content_element = soup.select(content_selector) if domain == "www.bbc.com" else soup.select_one(content_selector)
        if not content_element:
            raise ValueError("Content element not found")    

        # Convert to markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True

        md_content = ""

        if isinstance(content_element, list):
            for content in content_element:    
                md_content += converter.handle(str(content))
                md_content = md_content.replace('_', "")
        else:
            md_content = converter.handle(str(content_element))
            md_content = md_content.replace('_', "")

        if image_url:
            md_content = f"![Image]({image_url})\n\n" + md_content

        # Get domain name
        domain_name = domain.split('.')[-2]

        # Save article
        if save_article(title, md_content, domain_name):
            logger.info(f"Successfully scraped article from: {url}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
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
        tasks = [scrape_article(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for result, url in zip(results, urls):
        if isinstance(result, Exception):
            logger.error(f"Task failed for URL: {url} | Error: {result}")    
        elif not result:
            logger.error(f"Task failed for URL: {url}")
