# Article Details Extractor

This project is designed to extract news article details from various search engines (Google, Bing, Yahoo) based on specified companies and keywords. The extracted data includes the article's title, link, timestamp, and media name. The results are saved in a CSV file for further analysis.

## Features

- **Search Engine Integration**: Supports Google, Bing, and Yahoo for fetching news articles.
- **Customizable Search**: Allows users to specify companies and keywords to search for.
- **Pagination**: Scrapes multiple pages of search results for comprehensive data collection.
- **Asynchronous Scraping**: Utilizes `aiohttp` and `asyncio` for efficient and concurrent web requests.
- **CSV Output**: Saves the extracted data in a structured CSV format.

## Directory Structure

```
Extract artical details/
├── requirements.txt
├── docs/
│   └── psudocode.txt
└── src/
    ├── config.json
    ├── main.py
    └── utils/
        ├── __init__.py
        ├── config_loader.py
        ├── scraper.py
        ├── utils.py
        ├── __pycache__/
        └── early_refrences/
            ├── Optimized_web_data.py
            └── web_data_extractor.py
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Extract-article-details.git
   cd Extract-article-details
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure the Search**:
   - Modify the `config.json` file to include the companies and keywords you want to search for.
   - Alternatively, run the script and follow the prompts to input companies, keywords, and the number of pages to scrape.

   Example `config.json`:
   ```json
   {
       "companies": [
           "tata",
           "jio",
           "apple"
       ],
       "keywords": [
           "lawsuits",
           "merger",
           "bankruptcy"
       ],
       "pages": 3
   }
   ```

2. **Run the Script**:
   ```bash
   python src/main.py
   ```

3. **Review the Output**:
   - The extracted data will be saved in `src/output/news_results.csv`.

## Configuration

- **config.json**: Contains the list of companies, keywords, and the number of pages to scrape.
- **USER_AGENT**: Defined in `config_loader.py`, used to mimic a browser request.
- **OUTPUT_FILE**: Path to the output CSV file, defined in `config_loader.py`.

## Functions

- **safe_get(element, selector, attribute)**: Safely extracts values from HTML elements.
- **get_search_url(engine, query, page)**: Constructs the search URL for the specified search engine.
- **scrape_results()**: Main function to scrape results from the search engines and save them to a CSV file.
- **fetch(session, url)**: Asynchronously fetches the content of a URL.

## Example Output

The CSV file will have the following columns:

- **Search String**: The combination of company and keyword used in the search.
- **Search Engine**: The search engine used (Google, Bing, Yahoo).
- **Link**: The URL of the news article.
- **Title**: The title of the news article.
- **Time stamp**: The publication time of the article.
- **Media name**: The name of the media outlet.

## Dependencies

- **aiohttp**: For asynchronous HTTP requests.
- **beautifulsoup4**: For parsing HTML content.
- **pandas**: For data manipulation (if needed).
- **requests**: For synchronous HTTP requests (used in early references).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of `aiohttp`, `beautifulsoup4`, and other libraries used in this project.
- Inspired by the need for efficient web scraping tools for news aggregation.

## Contact

For any questions or suggestions, please contact me at  [https://github.com/jain-nikhilkumar].

