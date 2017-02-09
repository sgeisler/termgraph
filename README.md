# TermGraph

[![Build Status](https://travis-ci.org/sgeisler/termgraph.svg?branch=master)](https://travis-ci.org/sgeisler/termgraph)

TermGraph is a highly experimental and untested python library to draw candle stick graphs on a terminal. The graph is drawn using [unicode box drawing characters](https://en.wikipedia.org/wiki/Box-drawing_character). Colorama is used for coloring.

![example output](/example.png)

## Server example

I've built a hacky example application that pulls bitcoin market data from Bitstamp and displays a 24h graph (`example_btc_server.py`). It accepts tcp connections and you may send one line of configuration:
```
[<width=80>[ <height=43>[ <colors_on=True>]]⏎
```

An example server is running on `gnet.me:8170`. You may use `netcat` to get the current graph:
```
$ echo "80 24" | nc gnet.me 8170⏎
```