import aiohttp
from io import BytesIO


async def download_widget(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        return BytesIO(await resp.read())
