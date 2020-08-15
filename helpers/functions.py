import asyncio
import helpers.constants as const

async def read_to_next(reader: asyncio.StreamReader):
    next_bytes = await reader.readuntil(const.CRLF)
    return next_bytes[:-2]

async def read_dtype_and_len(reader: asyncio.StreamReader):
    dtype = await reader.read(1)
    command_len = await read_to_next(reader)
    return dtype, command_len

def bulk_string_response(byte_string):
    return b'$%u%b%b%b' % (len(byte_string), const.CRLF, byte_string, const.CRLF)

def simple_string_response(byte_string):
    return b'+%b%b' % (byte_string, const.CRLF)

def integer_response(byte_string):
    return b':%i%b' % (byte_string, const.CRLF)

def error_response(byte_string):
    return b'-%b%b' % (byte_string, const.CRLF)