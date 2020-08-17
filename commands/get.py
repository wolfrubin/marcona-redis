import asyncio
from helpers.functions import bulk_string_response, error_response
from cache import MARCONA_CACHE

async def execute(writer: asyncio.StreamWriter, key):
    try:
        writer.write(bulk_string_response(MARCONA_CACHE[key]))
    except KeyError:
        writer.write(error_response(b'Key "%b" not found in cache' % key))
