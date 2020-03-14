import asyncio
import constants

async def ping_response(writer: asyncio.StreamWriter, arg_list):
    if not arg_list:
        writer.write(b'+PONG%b' % constants.CRLF)
    else:
        if len(arg_list) > 1:
            writer.write(b'-ERR wrong number of arguments for command PING%b' % constants.CRLF)
        else:
            writer.write(b'+%b%b' % (arg_list[0], constants.CRLF))
    await writer.drain()
