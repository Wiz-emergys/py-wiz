from urllib.parse import urlparse
from utils.config import articles

def get_user_input():
    """
    Gets URLs from user input and validates them against a list of supported websites.
    """
    print("\nSupported Websites for Scraping:")
    for site in articles.keys():
        print(f"- {site}")

    urls = []
    while True:
        url = input("\nEnter an article URL (or type 'done' to finish): ").strip()
        if url.lower() == "done":
            break
        domain = urlparse(url).netloc
        if domain not in articles:
            print(f"❌ {domain} is not supported. Please enter a URL from the supported list.")
        else:
            urls.append(url)
            print(f"✅ URL added: {url}")

    if not urls:
        print("No valid URLs entered. Exiting.")
        exit()

    return urls
