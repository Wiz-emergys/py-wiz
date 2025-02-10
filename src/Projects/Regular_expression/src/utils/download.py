import aiohttp
import aiofiles
import os

async def download_pdf(url: str, filename: str, session: aiohttp.ClientSession, download_dir: str) -> str:
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
