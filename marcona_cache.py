import asyncio
import helpers

MARCONA_CACHE = {}

async def set_val(writer: asyncio.StreamWriter, key, value):
    MARCONA_CACHE[key] = value
    writer.write(b'+key set')
    await writer.drain()


async def get_val(writer: asyncio.StreamWriter, key):
    writer.write(helpers.bulk_string_response(MARCONA_CACHE[key]))
    await writer.drain()


async def key_count(writer: asyncio.StreamWriter, *keys):
    key_count = 0
    for key in keys:
        try:
            MARCONA_CACHE[key]
        except KeyError:
            pass
        else:
            key_count += 1
    writer.write(helpers.integer_response(key_count))
    await writer.drain()
