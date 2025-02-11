import re
from pypdf import PdfReader

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
    reader = PdfReader(pdf_path)
    text = ""
    for page_number in range(min(3, len(reader.pages))):
        text += reader.pages[page_number].extract_text() or ""
    return text

def extract_cin(text: str):
    """
    Extracts Corporate Identification Numbers (CIN) from the given text.

    Args:
        text (str): The input text from which to extract CIN numbers.

    Returns:
        list: A list of strings, each representing a CIN found in the text.
    """
    return re.findall(r'[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}', text)

def extract_emails(text: str):
    """
    Extracts email addresses from the given text.

    Args:
        text (str): The input text from which to extract email addresses.

    Returns:
        list: A list of strings, each representing an email address found in the text.
    """
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

def extract_phone_numbers(text: str):
    """
    Extracts phone numbers from the given text.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        list: A list of strings, each representing a phone number found in the text.
    """
    return re.findall(r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})', text)

def extract_pan_numbers(text: str):
    """
    Extracts Permanent Account Numbers (PAN) from the given text.

    Args:
        text (str): The input text from which to extract PAN numbers.

    Returns:
        list: A list of strings, each representing a PAN found in the text.
    """
    return re.findall(r'[A-Z]{5}\d{4}[A-Z]{1}', text)

def extract_dates(text: str):
    """
    Extracts dates from the given text.

    Args:
        text (str): The input text from which to extract dates.

    Returns:
        list: A list of strings, each representing a date found in the text in the format DD/MM/YYYY.
    """
    return re.findall(r'\b(?:\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2})\b',text)


def extract_websites(text: str):
    """
    Extracts website URLs from the given text.

    Args:
        text (str): The input text from which to extract website URLs.

    Returns:
        list: A list of strings, each representing a website URL found in the text.
    """
    return re.findall(r'\bhttps?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b|\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b',text)
