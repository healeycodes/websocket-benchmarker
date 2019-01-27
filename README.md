## :radio: WebSocket Benchmarker :watch:
*Benchmark a WebSocket server's message throughput with Python!*

---

###### 2019.01.26

Now with 100% more bleeding edge :zap: [asyncio](https://docs.python.org/3/library/asyncio.html) goodness.

---

```
python .\bench.py
Benchmarking localhost:3000 with 1000 total clients. 64 clients concurrently. 5 roundtrips per client.
Min: 0.04235544116481793
Mean: 0.16393149133306262
Max: 0.42205915518170034
```

<br>

Message throughput is how fast a WebSocket server can parse and respond to a message. Some people consider this to be a good reference of a framework/library/server's performance. For this benchmark program, an echo server is presumed.

<br>

Design inspiration taken from Cargo Media's unmaintained [websocket-benchmark](https://github.com/cargomedia/websocket-benchmark) (JavaScript). This project aims to improve on the aforementioned by including logging functionality and other features.

<br>

### Usage

| Arg   | Description                            | Default         |
| ----- |:---------------------------------------|:----------------|
| `--h` | Host address of WebSocket server       | `localhost:3000`|
| `--n` | Number of clients to create            | `1000`          |
| `--c` | Number of concurrent clients           | `64`            |
| `--r` | Roundtrips per client                  | `5`             |
| `--s` | Message size in characters             | `30`            |
| `--l` | Path to create or append to a log file | `./log.txt`     |

<br>

### License

MIT (c) healeycodes
