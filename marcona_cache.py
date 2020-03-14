import asyncio
import helpers

MARCONA_CACHE = {}

async def setval(writer: asyncio.StreamWriter, key, value):
    MARCONA_CACHE[key] = value
    writer.write(b'+key set')
    await writer.drain()

async def getval(writer: asyncio.StreamWriter, key):
    writer.write(helpers.bulk_string_response(MARCONA_CACHE[key]))
    await writer.drain()