import json
import os

CONFIG_FILE = "config.json"
OUTPUT_FILE = r"C:\Users\NikhilJain\py-wiz\src\Projects\Extract artical details\src\output\news_results.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def get_user_input():
    
    """
    Get user input for companies, keywords, and number of pages to scrape and save to config.json.

    Asks user for input and saves it to the configuration file (config.json) in the same directory as
    this script. The configuration file is a JSON file with the following structure:

    {
        "companies": [
            "company1",
            "company2",
            ...
        ],
        "keywords": [
            "keyword1",
            "keyword2",
            ...
        ],
        "pages": <number of pages to scrape>
    }
    """
    
    companies = input("Enter company names (comma-separated): ").split(",")
    keywords = input("Enter keywords (comma-separated): ").split(",")
    pages = int(input("Enter number of pages to scrape: "))
    
    config_data = {
        "companies": [c.strip() for c in companies],
        "keywords": [k.strip() for k in keywords],
        "pages": pages
    }
    
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}")

def load_config():
    """
    Load the configuration from the file specified by CONFIG_FILE.

    Returns the loaded configuration as a dictionary with the following keys:

        - companies: List of company names
        - keywords: List of keywords
        - pages: Number of pages to scrape

    If the file does not exist, raises FileNotFoundError.
    """

    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found")
    with open(CONFIG_FILE) as f:
        return json.load(f)