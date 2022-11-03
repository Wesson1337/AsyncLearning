import asyncio
import logging
import time
from urllib.parse import urlparse
import aiofiles
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(logging.basicConfig(level=logging.INFO))

URL = 'https://okcalc.com/ru/'
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


async def get_third_party_links_from_html(data: str, url: str) -> list[str]:
    soup = BeautifulSoup(data, 'html.parser')
    links = set()
    host_name = urlparse(url).hostname
    scheme = urlparse(url).scheme
    for raw_link in soup.find_all('a'):
        link = raw_link.get('href')
        if link:
            if link.startswith('/'):
                link = f'{scheme}://{host_name}{link}'
            elif not link.startswith('http'):
                link = URL
            links.add(link)
    return list(links)


async def write_links_to_file(links: list[str]):
    async with aiofiles.open(FILE_PATH, mode='a') as f:
        for link in links:
            await f.write(link + '\n')


async def get_third_party_links_from_website(url):
    try:
        data = await get_data_from_url(url)
        links = await get_third_party_links_from_html(data, url)
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
        result = await asyncio.gather(*tasks)
        links = set()
        for test_links in result:
            for link in test_links:
                links.add(link)
    logger.info(time.time() - start)


if __name__ == '__main__':
    asyncio.run(main(4))
    clear_repeating_links()
