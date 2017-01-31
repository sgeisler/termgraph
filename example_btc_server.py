#!/usr/bin/python3

import json
import requests
from typing import List, Tuple, Dict
from itertools import groupby
from time import time
from graph import Candle, CandleStickGraph

BITSTAMP_TX_API = "https://www.bitstamp.net/api/v2/transactions/btcusd/?time={}"
DAYS_SECONDS = 24 * 60 * 60

class Range:
    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    def __contains__(self, item):
        return self.min <= item <= self.max


def get_bitstamp_transactions(timespan: str = "day") -> List[Tuple[int, float]]:
    raw_transactions = list(json.loads(requests.get(BITSTAMP_TX_API.format(timespan)).text))
    return [(int(entry['date']), float(entry['price'])) for entry in raw_transactions]


def group_transactions_by_timestamp(
        transactions: List[Tuple[int, str]],
        start_time: int,
        end_time: int,
        intervals: int) -> List[List[Tuple[int, float]]]:
    grouped = groupby(transactions, lambda tx: int((tx[0] - start_time) / (end_time - start_time) * intervals))
    return [list(group[1]) for group in grouped]


def transactions_to_candles(transactions: List[Tuple[int, float]]):
    start = transactions[0][1]
    end = transactions[-1][1]
    min_val = min(transactions, key=lambda tx: tx[1])[1]
    max_val = max(transactions, key=lambda tx: tx[1])[1]
    return Candle(min_val, max_val, start, end)


if __name__ == "__main__":
    now = int(time())
    data = get_bitstamp_transactions()
    p = group_transactions_by_timestamp(data, now - DAYS_SECONDS, now, 100)
    c = [transactions_to_candles(tx_set) for tx_set in reversed(p)]
    g = CandleStickGraph(c, 40)
    print(g.draw())
