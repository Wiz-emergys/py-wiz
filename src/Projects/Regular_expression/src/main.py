import re
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pdfplumber
import re




download_dir=os.path.join(os.getcwd(), 'download')
os.makedirs(download_dir, exist_ok=True)

def download_pdf():
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
    for file in os.listdir(download_dir):
        if file.startswith(name):
            return os.path.join(download_dir,file)
    return None



def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page_number in range(min(3, len(pdf.pages))):  # Extract text from the first 3 pages
            page = pdf.pages[page_number]
            text += page.extract_text()
    return text

def extract_cin(text):
    cin_pattern = r'[A-Z]{1}\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}'  
    return re.findall(cin_pattern, text)

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text):
    phone_pattern = r'(\+?\d{1,4}[\s-]?)?(\(?\d{1,4}\)?[\s-]?)?(\d{10})'  
    return re.findall(phone_pattern, text)

def extract_pan_numbers(text):
    pan_pattern = r'[A-Z]{5}\d{4}[A-Z]{1}'  
    return re.findall(pan_pattern, text)

def extract_dates(text):
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    return re.findall(date_pattern, text)

def extract_websites(text):
    website_pattern = r'https?://(?:www\.){3,}?[a-zA-Z0-9-]{5}+\.[a-zA-Z]{5,6}|\b(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{3,6}\b'

    return re.findall(website_pattern, text)

def main(pdf_path):
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Extract CIN numbers
    cin_numbers = extract_cin(text)
    print(cin_numbers)
    print(f"CIN Numbers: {len(cin_numbers)} found")
    
    # Extract Email IDs
    emails = extract_emails(text)
    print(emails)
    print(f"Email IDs: {len(emails)} found")
    
    # Extract Phone Numbers
    phone_numbers = extract_phone_numbers(text)
    print(phone_numbers)
    print(f"Phone Numbers: {len(phone_numbers)} found")
    
    # Extract PAN numbers
    pan_numbers = extract_pan_numbers(text)
    print(pan_numbers)
    print(f"PAN Numbers: {len(pan_numbers)} found")
    
    # Extract Dates
    dates = extract_dates(text)
    print(dates)
    print(f"Dates: {len(dates)} found")
    
    # Extract Websites
    websites = extract_websites(text)
    print(websites)

    print(f"Websites: {len(websites)} found")
    

    import requests


# Download the PDF
# download_pdf()

pdf_path =find_path("Draft-Annual-Return-FY-2021-22.pdf",download_dir)
main(pdf_path)

pdf_path = find_path("Form-MGT-7.pdf",download_dir)
main(pdf_path)

        