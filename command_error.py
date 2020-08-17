import asyncio
import helpers.constants as const
from helpers.functions import error_response

async def execute(writer: asyncio.StreamWriter, *args):
    command_name = args[0]
    writer.write(error_response(b'Command: "%b" not known or supported' % (command_name)))
