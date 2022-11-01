import asyncio
from pathlib import Path

import aiofiles
import aiohttp

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 20
OUT_PATH = (Path(__file__).parent / 'cats').absolute()


async def get_cat(client, id):
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await write_to_disk(result, id)


async def write_to_disk(content, id):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)


async def get_all_cats():

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, id) for id in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    res = asyncio.run(get_all_cats())
    print(len(res))

