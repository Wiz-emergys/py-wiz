# Media Scraping Project

This project is designed to scrape news articles from various media websites (BBC, The Hindu, Indian Express) and save the extracted content in markdown format. The project uses asynchronous web scraping techniques to efficiently fetch and process multiple articles concurrently.

## Features

- **Asynchronous Scraping**: Utilizes `aiohttp` and `asyncio` for efficient and concurrent web requests.
- **Markdown Output**: Saves the extracted article content in markdown format for easy readability and further processing.
- **Customizable Selectors**: Supports multiple websites with customizable CSS selectors for title, content, and images.
- **Logging**: Logs all scraping activities and errors for debugging and monitoring.
- **User Input Validation**: Validates user-provided URLs against a list of supported websites.

## Directory Structure

```
Media scraping/
├── extracted_content/
│   ├── bbc_Prevent closed Southport killer case prematurely.md
│   ├── indianexpress_Panama president to US stop lies and falsehoods ab.md
│   └── thehindu_Rupee falls 3 paise to 8665 against US dollar in e.md
├── logs/
└── src/
    ├── main.py
    ├── Docs/
    │   └── Pseudocode.txt
    ├── early_refrences/
    │   ├── Optimized_media_Scraping.py
    │   └── main.py
    ├── extracted_content/
    │   ├── bbc_Ed Sheeran stopped from busking in Bengaluru by In.md
    │   ├── bbc_Why more young men in Germany are turning to the f.md
    │   ├── indianexpress_Explained How mice learn to suppress fear implicat.md
    │   └── thehindu_Complaint filed against Ranveer Allahbadia others .md
    ├── logs/
    └── utils/
        ├── config.py
        ├── get_user_input.py
        ├── logger.py
        ├── scraper.py
        ├── utils.py
        └── __pycache__/
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Media-scraping.git
   cd Media-scraping
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Script**:
   ```bash
   python src/main.py
   ```

2. **Enter URLs**:
   - The script will prompt you to enter URLs of articles from supported websites (BBC, The Hindu, Indian Express).
   - Type 'done' when you have finished entering URLs.

3. **Review the Output**:
   - The extracted articles will be saved in the `extracted_content/` directory as markdown files.
   - Logs will be saved in the `logs/` directory.

## Configuration

- **config.py**: Contains the list of supported websites and their corresponding CSS selectors for title, content, and images.
- **logger.py**: Configures logging to save runtime logs in the `logs/` directory.
- **get_user_input.py**: Handles user input and validates URLs against the list of supported websites.

## Functions

- **clean_filename(title)**: Cleans the article title to create a valid filename.
- **save_article(title, content, domain)**: Saves the extracted article content to a markdown file.
- **scrape_article(session, url)**: Scrapes an article from the given URL using the corresponding selectors.
- **main(urls)**: Asynchronously scrapes multiple articles concurrently.

## Example Output

The markdown files will have the following structure:

```markdown
# Article Title

![Image](image_url)

Article content...
```

## Dependencies

- **aiohttp**: For asynchronous HTTP requests.
- **beautifulsoup4**: For parsing HTML content.
- **html2text**: For converting HTML to markdown.
- **logging**: For logging scraping activities and errors.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of `aiohttp`, `beautifulsoup4`, and other libraries used in this project.
- Inspired by the need for efficient web scraping tools for news aggregation.

## Contact

For any questions or suggestions, please contact me at  [https://github.com/jain-nikhilkumar].

