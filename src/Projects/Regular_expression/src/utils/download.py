import aiohttp
import aiofiles
import os

async def download_pdf(url: str, filename: str, session: aiohttp.ClientSession, download_dir: str) -> str:
    """
    Downloads a PDF from the specified URL and saves it to the local file system.

    Args:
        url (str): The URL of the PDF to download.
        filename (str): The name to save the downloaded PDF as.
        session (aiohttp.ClientSession): The aiohttp session to use for the download.
        download_dir (str): The directory to save the downloaded PDF in.

    Returns:
        str: The file path of the downloaded PDF if successful, None otherwise.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                filepath = os.path.join(download_dir, filename)
                async with aiofiles.open(filepath, 'wb') as f:
                    await f.write(content)
                print(f"Successfully downloaded '{filename}'.")
                return filepath
            else:
                print(f"Failed to download {url}. HTTP status: {response.status}")
                return None
    except Exception as e:
        print(f"Exception while downloading {url}: {e}")
        return None
