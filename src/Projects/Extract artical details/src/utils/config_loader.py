import json
import os

CONFIG_FILE = "config.json"
OUTPUT_FILE = r"C:\Users\NikhilJain\py-wiz\src\Projects\Extract artical details\src\output\news_results.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def get_user_input():
    """Get user input and save to config file"""
    companies = input("Enter company names (comma-separated): ").split(",")
    keywords = input("Enter keywords (comma-separated): ").split(",")
    pages = int(input("Enter number of pages to scrape: "))
    
    config_data = {
        "companies": [c.strip() for c in companies],
        "keywords": [k.strip() for k in keywords],
        "pages": pages
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}")

def load_config():
    """Load configuration from file"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found")
    with open(CONFIG_FILE) as f:
        return json.load(f)