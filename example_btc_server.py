#!/usr/bin/python3

import json
from threading import Thread

import requests
from typing import List, Tuple, Dict
from itertools import groupby
from time import time
from graph import Candle, CandleStickGraph
import socketserver

BITSTAMP_TX_API = "https://www.bitstamp.net/api/v2/transactions/btcusd/?time={}"
DAYS_SECONDS = 24 * 60 * 60

bitstamp_data = None
last_fetch = 0

def get_bitstamp_transactions(timespan: str = "day") -> List[Tuple[int, float]]:
    raw_transactions = list(json.loads(requests.get(BITSTAMP_TX_API.format(timespan)).text))
    return [(int(entry['date']), float(entry['price'])) for entry in reversed(raw_transactions)]


def group_transactions_by_timestamp(
        transactions: List[Tuple[int, str]],
        start_time: int,
        end_time: int,
        intervals: int) -> List[List[Tuple[int, float]]]:
    grouped = groupby(transactions, lambda tx: int((tx[0] - start_time) / (end_time - start_time) * intervals))
    return [list(group[1]) for group in grouped]


def transactions_to_candles(transactions: List[Tuple[int, float]]) -> Candle:
    start = transactions[0][1]
    end = transactions[-1][1]
    min_val = min(transactions, key=lambda tx: tx[1])[1]
    max_val = max(transactions, key=lambda tx: tx[1])[1]
    return Candle(min_val, max_val, start, end)

def update_cache() -> None:
    global bitstamp_data
    global last_fetch
    def fetch_updates():
        global bitstamp_data
        global last_fetch
        bitstamp_data = get_bitstamp_transactions()
        last_fetch = int(time())
        print("updated cache")

    if bitstamp_data is None:
        fetch_updates()
    elif last_fetch < (time() - 10):
        Thread(target=fetch_updates).start()

def render_graph(width: int, height: int, colored: bool) -> str:
    update_cache()
    now = int(time())
    p = group_transactions_by_timestamp(bitstamp_data, now - DAYS_SECONDS, now, width - 9)
    c = [transactions_to_candles(tx_set) for tx_set in p]

    prev_end = c[0].end_value
    for index, candle in enumerate(c[1:]):
        c[index+1].begin_value = prev_end
        prev_end = candle.end_value

    g = CandleStickGraph(c, height - 3)

    min_val = min([candle.min_value for candle in c])
    max_val = max([candle.max_value for candle in c])
    last = c[-1].end_value
    diff = last - c[0].begin_value

    out = g.draw(colored)
    out += "\n"

    legend = "24h | min = {:.2f} | max = {:.2f} | curr = {:.2f} | diff = {:+.2f}".format(min_val, max_val, last, diff)
    out +=  " " * int((width - len(legend)) / 2)
    out += legend + "\n"
    return out

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

class ChartRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):

        #print("got request from {}".format(self.request.))

        width = 80
        height = 43
        color = True

        args = self.request.recv(128).decode('ascii', 'ignore').split(" ")

        if len(args) >= 1:
            try:
                width_inp = int(args[0])
                if 10 <= width_inp <= 1024:
                    width = width_inp
            except Exception: pass

        if len(args) >= 2:
            try:
                height_inp = int(args[1])
                if 10 <= height_inp <= 1024:
                    height = height_inp
            except Exception: pass

        if len(args) >= 3:
            try:
                color = str2bool(args[2])
            except Exception: pass

        self.request.sendall(render_graph(width, height, color).encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1234

    server = socketserver.TCPServer((HOST, PORT), ChartRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
