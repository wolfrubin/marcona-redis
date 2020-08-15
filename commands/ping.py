import asyncio
import helpers.constants as const

async def execute(writer: asyncio.StreamWriter, *args):
    if not args:
        writer.write(b'+PONG%b' % const.CRLF)
    else:
        if len(args) > 1:
            writer.write(b'-ERR wrong number of arguments for command PING%b' % const.CRLF)
        else:
            writer.write(b'+%b%b' % (args[0], const.CRLF))
    await writer.drain()
