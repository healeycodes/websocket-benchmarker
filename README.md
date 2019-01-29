## :radio: WebSocket Benchmarker :watch:

*Message throughput* is how fast a WebSocket server can parse and respond to a message. Some people consider this to be a good reference of a framework/library/server's performance.

<br>

![](https://github.com/healeycodes/websocket-benchmarker/blob/master/images/header.png)

<br>

---

###### 2019.01.26

Now with 100% more bleeding edge :zap: [asyncio](https://docs.python.org/3/library/asyncio.html) goodness.

---

<br>

### Installation

Python 3.6.5+.

`pip install -r requirements.txt`

<br>

### Usage

This program expects the host to be an echo server and measures the time between sending a message and recieving the same message back from the host.

`python bench.py` will launch the benchmark and print statistics to stdout. If the log file path is to a non-file then one will be created otherwise results will be appended to the existing file.

The raw results are in CSV format with each line representing a client's roundtrip times.

E.g., `0.1, 0.1, 0.1` for one client performing three roundtrips.

<br>

| Arg   | Description                            | Default         |
| ----- |:---------------------------------------|:----------------|
| `--h` | Host address of WebSocket server       | `localhost:3000`|
| `--n` | Number of clients to create            | `1000`          |
| `--c` | Number of concurrent clients           | `64`            |
| `--r` | Roundtrips per client                  | `5`             |
| `--s` | Message size in characters             | `30`            |
| `--l` | Path to create or append to a log file | `./log.txt`     |

<br>

### Tests

Full end-to-end testing via unittest.

```
python -m unittest
...
----------------------------------------------------------------------
Ran 3 tests in 8.371s

OK
```

<br>

### License

MIT (c) 2019 healeycodes.

Inspiration taken from the unmaintained JavaScript project [websocket-benchmark](https://github.com/cargomedia/websocket-benchmark).
