import asyncio

async def my_coroutine():
    while True:
        print('co routine')
        await asyncio.sleep(1)

event_loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(my_coroutine())
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print('Closing')
    event_loop.close()
