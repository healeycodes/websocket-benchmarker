#!/usr/bin/env python

import os
import time
import asyncio
import websockets
import argparse

parser = argparse.ArgumentParser(description='Benchmark a WebSocket server')
parser.add_argument('--h', dest='host',
                    help='Host address of WebSocket server',
                    default='localhost:3000')
parser.add_argument('--n', dest='clients',
                    help='Number of clients to create',
                    default=1000, type=int)
parser.add_argument('--c', dest='concurrency',
                    help='Number of concurrent clients',
                    default=64, type=int)
parser.add_argument('--r', dest='roundtrips',
                    help='Roundtrips per client',
                    default=5, type=int)
parser.add_argument('--s', dest='msg_size',
                    help='Message size in characters',
                    default=30, type=int)
parser.add_argument('--l', dest='log_path',
                    help='Path to create or append to a log file',
                    default=os.path.join('.', 'log.txt'))
args = parser.parse_args()

# get benchmark parameters
host = args.host
clients = args.clients
concurrency = args.concurrency
roundtrips = args.roundtrips
message = 'a' * args.msg_size

# open log file
log_file = open(args.log_path, 'a')
log_memory = list()

print(f'Benchmarking {host} with {clients} total clients. ' +
      f'{concurrency} clients concurrently. {roundtrips} roundtrips per client.\n')


async def client(state):
    '''A WebSocket client, which sends a message and expects an echo `roundtrip` number of times.
    This client will spawn a copy of itself afterwards, so that the requested concurrency is continuous.

    Parameters
    ----------
    state : Dictionary
        A Dictionary-like object with the key `clients` -- the number of clients spawned thus far.

    Returns
    -------
    string
        A statement when the max number of clients have been spawned.'''
    if state['clients'] >= clients:
        return 'Reached max clients.'
    state['clients'] += 1
    timings = list()
    start = time.perf_counter()
    async with websockets.connect(f'ws://{host}') as websocket:
        for i in range(roundtrips):
            await websocket.send(message)
            response = await websocket.recv()
            if response != message:
                raise 'Message recieved differs from message sent'
            timings.append(time.perf_counter() - start)
    log_file.write(','.join([str(t) for t in timings]) + '\n')
    log_memory.append(timings)
    await asyncio.ensure_future(client(state))


# create an amount of client coroutine functions to satisfy args.concurrency
con_clients = [client] * concurrency

# pass them all a 'link' to the same state Dictionary
state = dict({'clients': 0})

# run them concurrently
main = asyncio.gather(*[i(state) for i in con_clients])
loop = asyncio.get_event_loop()
loop.run_until_complete(main)


def stats(timings):
    '''Prints stats based off raw benchmark data.

    Parameters
    ----------
    timings : List(List(Float))
        A List of Lists containing message timings.

    Returns
    -------
    Dictionary
        Stats from the provided timings. Keys: `min`, `mean`, and `max`. '''
    timings_flat = [t for client_timings in timings for t in client_timings]
    min_timing = min(timings_flat) * 1000
    mean_timing = sum(timings_flat) / len(timings_flat) * 1000
    max_timing = max(timings_flat) * 1000
    print(f'Min: {min_timing:.2f}ms')
    print(f'Mean: {mean_timing:.2f}ms')
    print(f'Max: {max_timing:.2f}ms')
    return dict({'min': min_timing, 'mean': mean_timing, 'max': max_timing})


# the benchmark is finished, build stats by passing an in-memory copy of the log
stats(log_memory)

print(f'\nRaw results sent to {log_file.name}')
