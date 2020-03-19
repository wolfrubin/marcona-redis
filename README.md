# Introduction

- Simple realization of a redis server done in pure python3 using asyncio
- Uses an asyncio event loop to handle connections concurrently
- Implements the PING, GET, SET and EXISTS commands (so far)

# To run

`python marcona_server.py` (make sure this is python 3). This will run the server locally on port 6350.

Then use the `redis-cli` like so `redis-cli -p 6350` to connect once it is up and running. Then you can PING, SET and GET all you like.

# To Do

1. More commands
2. Tests
3. Performance benchmarking
4. Logging
5. Try memory map for the cache interface to make it persistent (see how this would impact performance)

Personal project to learn more about python, asyncio, the redis protocol, memory maps.

# Thoughts

Each command has a common set of stages
read args (reader)
do work
write response (writer)

Currently do work and write response are tied together into one function
This should be split

Will each redis COMMAND have it's own well defined response type or will they change based on the input?
