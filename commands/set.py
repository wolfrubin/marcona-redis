import asyncio
from cache import MARCONA_CACHE

async def execute(writer: asyncio.StreamWriter, key, value):
    MARCONA_CACHE[key] = value
    writer.write(b'+key set')
    await writer.drain()