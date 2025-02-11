from urllib.parse import urlparse
from utils.config import articles

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
    for site in articles.keys():
        print(f"- {site}")

    urls = []
    while True:
        url = input("\nEnter an article URL (or type 'done' to finish): ").strip()
        if url.lower() == "done":
            break
        domain = urlparse(url).netloc
        print(domain)
        if domain not in articles:
            print(f"❌ {domain} is not supported. Please enter a URL from the supported list.")
        else:
            urls.append(url)
            print(f"✅ URL added: {url}")

    if not urls:
        print("No valid URLs entered. Exiting.")
        exit()

    return urls
