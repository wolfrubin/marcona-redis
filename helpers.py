import asyncio
import constants

async def read_to_next(reader: asyncio.StreamReader):
    next_bytes = await reader.readuntil(constants.CRLF)
    return next_bytes[:-2]

async def read_dtype_and_len(reader: asyncio.StreamReader):
    dtype = await reader.read(1)
    command_len = await read_to_next(reader)
    return dtype, command_len

async def get_array_length(reader: asyncio.StreamReader):
    """Gets the array length from the stream reader"""
    arr_len = await read_to_next(reader)
    return arr_len

def bulk_string_response(byte_string):
    length = len(byte_string)
    return b'$%u%b%b%b' % (length, constants.CRLF, byte_string, constants.CRLF)

def simple_string_response(byte_string):
    return b'+%b%b' % (byte_string, constants.CRLF)

def integer_response(byte_string):
    return b':%i%b' % (byte_string, constants.CRLF)
