import asyncio
import time
import aiohttp 
import os
from utils.download import download_pdf
from utils.extract import extract_text_from_pdf, extract_cin, extract_emails, extract_phone_numbers, extract_pan_numbers, extract_dates, extract_websites
from utils.file_operations import write_results_to_file

# Set up directories
project_root = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(project_root, 'download')
os.makedirs(download_dir, exist_ok=True)



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

# MAIN ASYNCHRONOUS WORKFLOW
async def main_async():
    
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
        url = input("Enter PDF URL or done to finish: ").strip()
        if url.lower() == "done":
            break
        filename = input("Enter desired filename for this PDF (with .pdf extension): ").strip()
        pdf_list.append((filename, url))
        print(f" ✅ Successfully added URL for '{filename}'.\n")
    
    if not pdf_list:
        print(" ❌ No PDF URLs were provided. Exiting.")
        return

    async with aiohttp.ClientSession() as session:
        download_tasks = [download_pdf(url, filename, session, download_dir) for filename, url in pdf_list]
        file_paths = await asyncio.gather(*download_tasks)

    file_paths = [path for path in file_paths if path is not None]
    
    if not file_paths:
        print("No PDFs were downloaded successfully. Exiting.")
        return
    start=time.time()
    process_tasks = [process_pdf(path) for path in file_paths]
    await asyncio.gather(*process_tasks)
    print(f"The total time required is: {time.time() - start}")


if __name__ == '__main__':
    asyncio.run(main_async())
   