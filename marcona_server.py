import asyncio
import commands
import helpers
from command_error import execute as error
from watchdog.events import FileSystemEventHandler


async def respond_to_command(command_name: bytes, args: list, writer: asyncio.StreamWriter):
    """The pattern here is that the commands module imports the function that executes the command
    from the module with the same name in the commands module. 
    
    I.e. commands/ping.py has a function execute in it
        this is imported in commands/__init__.py as ping
        The getattr here gets that ping function as it is the name of the issued command.

    This means that all commands need to follow the same interface of (writer, *args).

    This is fine for the uses we have so far.

    This could be changed at a later date such that the execute function in ping.py would
    take a simpler interface with just the arg list and not be responsible for writing to
    the stream. Just return the bytes that need to be written back to the stream.
    """
    try:
        func = getattr(commands, command_name.decode("utf-8").lower())
    except AttributeError:
        print('error no command, writing error response')
        func = error
        args = [command_name, *args]
    finally:
        await func(writer, *args)

async def client_connected(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_address = writer.get_extra_info('peername')
    print('client host {} port {} connected callback'.format(*client_address))
    first_byte = await reader.read(1)
    # Parse first bite. If this is not a *, it is an unrecognised command
    if first_byte == b'*':  # array
        n_elements = await helpers.read_to_next(reader)
        command_name = None
        command_args = []
        dtype, dlen = await helpers.read_dtype_and_len(reader)
        if dtype == b'$':
            # Bulk string
            command_name = await reader.read(int(dlen))
            await reader.read(2)
        for element in range(1, int(n_elements)):
            dtype, dlen = await helpers.read_dtype_and_len(reader)
            if dtype == b'$':
                # Bulk string
                command_arg = await reader.read(int(dlen))
                await reader.read(2)
                command_args.append(command_arg)
        print(command_name, command_args)
        await respond_to_command(command_name, command_args, writer)
    else:
        command = await read_to_next(reader)
        error(writer, [command])
    
    await writer.drain()
    writer.close()

print('Starting server')

event_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()

factory = asyncio.start_server(client_connected, host='localhost', port=6351)
server = event_loop.run_until_complete(factory)

try:
    print('running server')
    event_loop.run_forever()
except Exception:
    pass
finally:
    print('closing server')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    print('shutdown complete')
