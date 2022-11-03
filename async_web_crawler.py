import asyncio
import logging
import time
from urllib.parse import urlparse
import aiofiles
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(logging.basicConfig(level=logging.INFO))

URL = 'https://youtube.com/'
FILE_PATH = 'links/link'


def clear_repeating_links():
    with open(FILE_PATH, 'r') as f:
        links = f.read().split('\n')
    links_set = set(links)
    with open(FILE_PATH, 'w') as f:
        f.write('\n'.join(list(links_set)))


async def get_data_from_url(url: str) -> str:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(3)) as session:
        async with session.get(url) as response:
            data = await response.text()
    return data


async def get_third_party_links_from_html(data: str) -> list[str]:
    soup = BeautifulSoup(data, 'html.parser')
    links = []
    host_name = urlparse(URL).hostname
    for raw_link in soup.find_all('a'):
        link = raw_link.get('href')
        if link and link.startswith('http') and host_name not in link:
            links.append(link)
    return links


async def get_links_from_file():
    async with aiofiles.open(FILE_PATH, mode='r') as f:
        file_data = await f.read()
        links = file_data.split('\n')
        return links


async def write_links_to_file(links: list[str]):
    links_in_file = await get_links_from_file()
    async with aiofiles.open(FILE_PATH, mode='a') as f:
        for link in links:
            if link not in links_in_file:
                await f.write(link + '\n')


async def get_third_party_links_from_website(url):
    try:
        data = await get_data_from_url(url)
        links = await get_third_party_links_from_html(data)
        await write_links_to_file(links)
        return links
    except Exception as e:
        print(e)
        return [URL]


async def main(iterations: int):
    start = time.time()
    links = await get_third_party_links_from_website(URL)
    for _ in range(iterations - 1):
        tasks = []
        for link in links:
            task = asyncio.create_task(get_third_party_links_from_website(link))
            tasks.append(task)
        links = []
        for test_links in await asyncio.gather(*tasks):
            links.extend(test_links)
    logger.info(time.time() - start)


if __name__ == '__main__':
    asyncio.run(main(3))
    clear_repeating_links()

