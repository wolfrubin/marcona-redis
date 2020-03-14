import asyncio
import constants
import ping
import marcona_cache

async def respond_to_command(command_name: str, args: list, writer: asyncio.StreamWriter):
    if command_name.upper() == constants.PING:
        await ping.ping_response(writer, args)
    elif command_name.upper() == constants.SET:
        await marcona_cache.setval(writer, *args)
    elif command_name.upper() == constants.GET:
        await marcona_cache.getval(writer, *args)
    else:
        print('command not supported')
        writer.write(b'-ERR command not supported')
        await writer.drain()

async def client_connected(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_address = writer.get_extra_info('peername')
    print('client host {} port {} connected callback'.format(*client_address))
    first_byte = await reader.read(1)
    # Parse first bite. If this is not a *, it is an unrecognised command
    if first_byte == b'*':  # array
        n_elements = await get_array_length(reader)
        command_name = None
        command_args = []
        dtype, dlen = await read_dtype_and_len(reader)
        if dtype == b'$':
            # Bulk string
            command_name = await reader.read(int(dlen))
            await reader.read(2)
        for element in range(1, int(n_elements)):
            dtype, dlen = await read_dtype_and_len(reader)
            if dtype == b'$':
                # Bulk string
                command_arg = await reader.read(int(dlen))
                await reader.read(2)
                command_args.append(command_arg)
        print(command_name, command_args)
        await respond_to_command(command_name, command_args, writer)
        writer.close()
    else:
        command = await read_to_next(reader)
        writer.write(b'-ERR Unknown command %b' % command[:-2])
        await writer.drain()
        writer.close()
            
print('Starting server')

event_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()

factory = asyncio.start_server(client_connected, host='localhost', port=6350)
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
