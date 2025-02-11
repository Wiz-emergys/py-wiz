import re
from utils.config import extracted_dir
from utils.logger import logger
import os

def clean_filename(title):
   
    """
    Clean a filename by replacing non-alphanumeric characters (except hyphen) with an empty string, 
    strip leading/trailing whitespace, and truncate to 50 characters.
    
    Parameters:
        title (str): The title to be cleaned.
    
    Returns:
        str: A cleaned, truncated version of the title suitable for use as a filename.
    """
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title, content, domain):
   
    """
    Save the article content to a markdown file named with the domain and a cleaned title.

    This function attempts to create a markdown file in the `extracted_dir` directory
    using the provided article title, content, and domain. The filename is constructed
    by cleaning the title to remove unwanted characters and truncating it to a suitable
    length. If the operation succeeds, a success message is logged; otherwise, an error
    message is logged.

    Parameters:
        title (str): The title of the article to be saved.
        content (str): The content of the article.
        domain (str): The domain or source of the article.

    Returns:
        bool: True if the article was successfully saved, False otherwise.
    """
    try:
        filename = f"{domain}_{clean_filename(title)}.md"
        filepath = os.path.join(extracted_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{content}")
        logger.info(f"Successfully saved article: {filename}")
        return True
    except Exception as e:
        logger.error(f"Save failed: {str(e)}")
        return False
