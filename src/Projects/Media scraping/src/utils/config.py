import os

# Project Directories
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_dir = os.path.join(project_root, "logs")
extracted_dir = os.path.join(project_root, "extracted_content")

os.makedirs(logs_dir, exist_ok=True)
os.makedirs(extracted_dir, exist_ok=True)

# Supported Websites and Selectors
articles = {
    'indianexpress.com': ('h1[itemprop="headline"]', 'div.story_details', 'span.custom-caption img'),
    'www.thehindu.com': ('div.storyline h1.title', 'div.storyline div.articlebodycontent[itemprop="articleBody"]', 'div.picture.verticle picture source'),
    'www.bbc.com': ('h1.sc-518485e5-0.bWszMR', 'p.sc-eb7bd5f6-0.fYAfXe', "div[data-testid='hero-image'] img:not(.hide-when-no-script)")
}
