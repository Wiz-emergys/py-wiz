import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import PyPDF2
from pypdf import PdfReader
import re
import requests



project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
download_dir=os.path.join(project_root, 'download')
os.makedirs(download_dir, exist_ok=True)

def download_pdf():
    """
    Downloads two PDF files from the given URLs using headless Chrome and 
    stores them in the 'download' directory in the project root.

    Args:
        None

    Returns:
        None
    """
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs",{
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True

    })

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    
    driver.get(r"https://assets.airtel.in/teams/simplycms/web/docs/Draft-Annual-Return-FY-2021-22.pdf")
    time.sleep(20)
    driver.get(r"https://www.tatamotors.com/wp-content/uploads/2023/10/Form-MGT-7.pdf")
    time.sleep(20)
    driver.quit()


def find_path(name,download_dir):
    """
    Finds a file in the specified directory that starts with the given name.

    Args:
        name (str): The name to search for.
        download_dir (str): The directory to search in.

    Returns:
        str: The full path to the file if it is found, None otherwise.
    """
    for file in os.listdir(download_dir):
        if file.startswith(name):
            return os.path.join(download_dir,file)
    return None



def extract_text_from_pdf(pdf_path):
    """
    Extracts text from the first 3 pages of the PDF file.

    Reads the PDF file at the specified path and extracts the text from the first 3 pages
    (or fewer if the PDF has fewer pages). The extracted text is returned as a single string.

    Args:
        pdf_path (str): The file path of the PDF file to extract text from.

    Returns:
        str: The extracted text from the PDF file.
    """

    reader = PdfReader(pdf_path)
    text = ""
    # Extract text from the first 3 pages (or fewer if the document is shorter)
    for page_number in range(min(3, len(reader.pages))):
        page = reader.pages[page_number]
        page_text = page.extract_text() or ""
        text += page_text
    return text

def extract_cin(text):
    """
    Extracts Corporate Identification Numbers (CIN) from the given text.

    Args:
        text (str): The input text from which to extract CIN numbers.
    
    Returns:
        list: A list of strings, each representing a CIN found in the text.
    """

    cin_pattern = r'[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}'  
    return re.findall(cin_pattern, text)

def extract_emails(text):

    """
    Extracts email addresses from the given text.

    Args:
        text (str): The input text from which to extract email addresses.

    Returns:
        list: A list of strings, each representing an email address found in the text.
    """
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text):
    
    """
    Extracts phone numbers from the given text.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        list: A list of strings, each representing a phone number found in the text.
    """
    phone_pattern = r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})'  
    return re.findall(phone_pattern, text)

def extract_pan_numbers(text):
    """
    Extracts Permanent Account Numbers (PAN) from the given text.

    Args:
        text (str): The input text from which to extract PAN numbers.

    Returns:
        list: A list of strings, each representing a PAN found in the text.
    """
    
    pan_pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'  
    return re.findall(pan_pattern, text)

def extract_dates(text):
    """
    Extracts dates from the given text.

    Args:
        text (str): The input text from which to extract dates.

    Returns:
        list: A list of strings, each representing a date found in the text in the format DD/MM/YYYY.
    """
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    return re.findall(date_pattern, text)

def extract_websites(text):

    """
    Extracts URLs from the given text.

    Args:
        text (str): The input text from which to extract URLs.

    Returns:
        list: A list of strings, each representing a URL found in the text.
    """

    website_pattern = r'https?://(?:www\.){3,}?[a-zA-Z0-9-]{5}+\.[a-zA-Z]{5,6}|\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{3,6}\b'

    return re.findall(website_pattern, text)

def main(pdf_path):
    # Extract text from the PDF
    """
    Processes a PDF file to extract and print various entities.

    This function extracts text from a PDF file specified by the given path
    and identifies different types of information from the text, including:
    Corporate Identification Numbers (CIN), email addresses, phone numbers,
    Permanent Account Numbers (PAN), dates, and website URLs. It counts and
    prints the number of occurrences of each type of entity found.

    Args:
        pdf_path (str): The file path of the PDF to process.

    Returns:
        None
    """

    text = extract_text_from_pdf(pdf_path)
    
    # Extract CIN numbers
    cin_numbers = extract_cin(text)
    print(f"CIN Numbers: {len(cin_numbers)} found")
    print(cin_numbers)
    
    # Extract Email IDs
    emails = extract_emails(text)
    print(f"Email IDs: {len(emails)} found")
    print(emails)
    
    # Extract Phone Numbers
    phone_numbers = extract_phone_numbers(text)
    print(f"Phone Numbers: {len(phone_numbers)} found")
    print(phone_numbers)
    
    # Extract PAN numbers
    pan_numbers = extract_pan_numbers(text)
    print(f"PAN Numbers: {len(pan_numbers)} found")
    print(pan_numbers)
    
    # Extract Dates
    dates = extract_dates(text)
    print(f"Dates: {len(dates)} found")
    print(dates)
    
    # Extract Websites
    websites = extract_websites(text)
    print(f"Websites: {len(websites)} found")
    print(websites)
    



# Download the PDF
# download_pdf()

pdf_path =find_path("Draft-Annual-Return-FY-2021-22.pdf",download_dir)
pdf_path = find_path("Draft-Annual-Return-FY-2021-22.pdf", download_dir)
if pdf_path:
    print(f"Found file: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print("PDF not found!")

main(pdf_path)
pdf_path = find_path("Form-MGT-7.pdf",download_dir)
if pdf_path:
    print(f"Found file: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print("PDF not found!")
main(pdf_path)

        