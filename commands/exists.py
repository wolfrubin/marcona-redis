import asyncio
from helpers.functions import integer_response
from cache import MARCONA_CACHE

async def execute(writer: asyncio.StreamWriter, *keys):
    key_count = 0
    for key in keys:
        try:
            MARCONA_CACHE[key]
        except KeyError:
            pass
        else:
            key_count += 1
    writer.write(integer_response(key_count))
    await writer.drain()
