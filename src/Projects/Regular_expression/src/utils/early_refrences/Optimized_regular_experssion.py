import asyncio
import time
import aiohttp
import aiofiles
import re
import os
from pypdf import PdfReader

# Set up the download directory relative to this script
project_root = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(project_root, 'download')
os.makedirs(download_dir, exist_ok=True)


# Set up the results directory
results_dir = os.path.join(project_root, 'results')
os.makedirs(results_dir, exist_ok=True)

def write_results_to_file(pdf_path, results):
    """
    Writes extracted data to a formatted text file.
    
    Args:
        pdf_path (str): The path of the processed PDF file.
        results (dict): A dictionary containing extracted CINs, emails, phone numbers, PANs, dates, and websites.
    """
    filename = os.path.basename(pdf_path).replace('.pdf', '_results.txt')
    result_file_path = os.path.join(results_dir, filename)
    
    with open(result_file_path, 'w', encoding='utf-8') as f:
        f.write(f"\n--- Processing file: {pdf_path} ---\n")
        f.write(f"CIN Numbers ({len(results['cin'])} found): {results['cin']}\n")
        f.write(f"Email IDs ({len(results['emails'])} found): {results['emails']}\n")
        f.write(f"Phone Numbers ({len(results['phone_numbers'])} found): {results['phone_numbers']}\n")
        f.write(f"PAN Numbers ({len(results['pan'])} found): {results['pan']}\n")
        f.write(f"Dates ({len(results['dates'])} found): {results['dates']}\n")
        f.write(f"Websites ({len(results['websites'])} found): {results['websites']}\n")
    
    print(f"Results saved to {result_file_path}\n")

# ASYNCHRONOUS PDF DOWNLOAD FUNCTION
async def download_pdf(url: str, filename: str, session: aiohttp.ClientSession) -> str:
    """
    Downloads a PDF from the specified URL and saves it to the local file system.
    
    Args:
        url (str): The URL of the PDF to download.
        filename (str): The name to save the downloaded PDF as.
        session (aiohttp.ClientSession): The aiohttp session to use for the download.
    
    Returns:
        str: The file path of the downloaded PDF if successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL
        async with session.get(url) as response:
            if response.status == 200:
                # Read the content of the PDF from the response
                content = await response.read()
                
                # Construct the file path for saving the PDF
                filepath = os.path.join(download_dir, filename)
                
                # Save the PDF content to the file system
                async with aiofiles.open(filepath, 'wb') as f:
                    await f.write(content)
                
                # Log a success message and return the file path
                print(f"Successfully added URL for '{filename}'. Downloaded {len(content)} bytes.")
                return filepath
            else:
                # Log an error message for unsuccessful download
                print(f"Failed to download {url}. HTTP status: {response.status}")
                return None
    except Exception as e:
        # Log any exceptions that occur during the download process
        print(f"Exception occurred while downloading {url}: {e}")
        return None



# PDF TEXT EXTRACTION AND REGEX FUNCTIONS
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from the first 3 pages of the PDF file.
    
    Reads the PDF file at the specified path and extracts the text from the first 3 pages
    (or fewer if the PDF has fewer pages). The extracted text is returned as a single string.
    
    Args:
        pdf_path (str): The file path of the PDF file to extract text from.
    
    Returns:
        str: The extracted text from the PDF file.
    """
    # Create a PDF reader for the specified PDF file
    reader = PdfReader(pdf_path)
    
    # Initialize an empty string to store the extracted text
    text = ""
    
    # Iterate over the first 3 pages (or fewer if the PDF has fewer pages)
    for page_number in range(min(3, len(reader.pages))):
        # Get the current page from the PDF reader
        page = reader.pages[page_number]
        
        # Extract the text from the page (or an empty string if none is found)
        page_text = page.extract_text() or ""
        
        # Append the extracted page text to the overall text string
        text += page_text
    
    # Return the extracted text
    return text

def extract_cin(text: str):
    """
    Extracts Corporate Identification Numbers (CIN) from the given text.

    Args:
        text (str): The input text from which to extract CIN numbers.
    
    Returns:
        list: A list of strings, each representing a CIN found in the text.
    """
    cin_pattern = r'[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}'
    return re.findall(cin_pattern, text)

def extract_emails(text: str):
    
    """
    Extracts email addresses from the given text.

    Args:
        text (str): The input text from which to extract email addresses.

    Returns:
        list: A list of strings, each representing an email address found in the text.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str):
    """
    Extracts phone numbers from the given text.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        list: A list of strings, each representing a phone number found in the text.
    """
    phone_pattern = r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})'
    return re.findall(phone_pattern, text)

def extract_pan_numbers(text: str):
    """
    Extracts Permanent Account Numbers (PAN) from the given text.

    Args:
        text (str): The input text from which to extract PAN numbers.

    Returns:
        list: A list of strings, each representing a PAN found in the text.
    """

    pan_pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'
    return re.findall(pan_pattern, text)

def extract_dates(text: str):
    """
    Extracts dates from the given text.

    Args:
        text (str): The input text from which to extract dates.

    Returns:
        list: A list of strings, each representing a date found in the text in the format DD/MM/YYYY.
    """
    
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    return re.findall(date_pattern, text)

def extract_websites(text: str):
    """
    Extracts websites from the given text.

    Args:
        text (str): The input text from which to extract websites.

    Returns:
        list: A list of strings, each representing a website found in the text.
    """

    website_pattern = r'https?://(?:www\.){3,}?[a-zA-Z0-9-]{5}+\.[a-zA-Z]{5,6}|\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{3,6}\b'
    return re.findall(website_pattern, text)


# ASYNCHRONOUS PDF PROCESSING FUNCTION
async def process_pdf(pdf_path: str):
    
    """
    Asynchronous function to process a PDF file.

    Args:
        pdf_path (str): The path to the PDF file to process.

    Returns:
        None
    """
    text = await asyncio.to_thread(extract_text_from_pdf, pdf_path)
    
    results = {
        "cin": extract_cin(text),
        "emails": extract_emails(text),
        "phone_numbers": extract_phone_numbers(text),
        "pan": extract_pan_numbers(text),
        "dates": extract_dates(text),
        "websites": extract_websites(text)
    }
    
    write_results_to_file(pdf_path, results)


# MAIN ASYNCHRONOUS WORKFLOWa
async def main_async():
    # Build a dynamic list of PDFs based on user input.
    """
    Asynchronous main function.

    This function builds a dynamic list of PDFs based on user input, downloads them concurrently using aiohttp,
    filters out any failed downloads, and processes each downloaded PDF concurrently using asyncio.

    The function will exit if no PDF URLs are provided or if no PDFs are downloaded successfully.

    Args:
        None

    Returns:
        None
    """
    pdf_list = []
    print("Enter the PDF URLs one by one.")

    while True:
        url = input("Enter PDF URL or done to finish : ").strip()
        if url.lower() == "done":
            break
        filename = input("Enter desired filename for this PDF (with .pdf extension): ").strip()
        pdf_list.append((filename, url))
        print(f" ✅ Successfully added UR L for '{filename}'.\n")
    
    if not pdf_list:
        print(" ❌ No PDF URLs were provided. Exiting.")
        return

    # Download PDFs concurrently using aiohttp.
    async with aiohttp.ClientSession() as session:
        download_tasks = [download_pdf(url, filename, session) for filename, url in pdf_list]
        file_paths = await asyncio.gather(*download_tasks)

    # Filter out any failed downloads.
    file_paths = [path for path in file_paths if path is not None]
    
    if not file_paths:
        print("No PDFs were downloaded successfully. Exiting.")
        return

    # Process each downloaded PDF concurrently.
    process_tasks = [process_pdf(path) for path in file_paths]
    await asyncio.gather(*process_tasks)

if __name__ == '__main__':
    start=time.time()
    asyncio.run(main_async())
    print(f"The total time required is : {time.time()-start}")
