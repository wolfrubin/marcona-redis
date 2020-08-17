import asyncio
from cache import MARCONA_CACHE
from helpers.functions import simple_string_response

async def execute(writer: asyncio.StreamWriter, key, value):
    MARCONA_CACHE[key] = value
    writer.write(simple_string_response(b'OCK'))
