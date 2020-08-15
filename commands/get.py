import asyncio
from helpers.functions import bulk_string_response
from cache import MARCONA_CACHE

async def execute(writer: asyncio.StreamWriter, key):
    writer.write(bulk_string_response(MARCONA_CACHE[key]))
    await writer.drain()
