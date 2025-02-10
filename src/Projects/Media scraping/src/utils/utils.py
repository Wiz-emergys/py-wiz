import re
from utils.config import extracted_dir
from utils.logger import logger
import os

def clean_filename(title):
    """
    Clean a filename by replacing non-alphanumeric characters (except hyphen) with an empty string.
    Strip leading/trailing whitespace, and truncate to 50 characters.
    """
    return re.sub(r'[^\w\s-]', '', title).strip()[:50]

def save_article(title, content, domain):
    """
    Save article content to a markdown file.

    Returns:
        bool: True if successful, False otherwise.
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
