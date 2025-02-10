import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page_number in range(min(3, len(reader.pages))):
        text += reader.pages[page_number].extract_text() or ""
    return text

def extract_cin(text: str):
    return re.findall(r'[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}', text)

def extract_emails(text: str):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

def extract_phone_numbers(text: str):
    return re.findall(r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})', text)

def extract_pan_numbers(text: str):
    return re.findall(r'[A-Z]{5}\d{4}[A-Z]{1}', text)

def extract_dates(text: str):
    return re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)

def extract_websites(text: str):
    return re.findall(r'\bhttps?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b|\bwww\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b',text)
    