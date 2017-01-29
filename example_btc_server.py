#!/usr/bin/python3

import json
import requests
from typing import List, Tuple

BITSTAMP_TX_API = "https://www.bitstamp.net/api/v2/transactions/btcusd/?time={}"


class Range:
    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    def __contains__(self, item):
        return min <= item <= max


def get_bitstamp_transactions(timespan: str = "day") -> List[Tuple[str, str]]:
    raw_transactions = json.loads(requests.get(BITSTAMP_TX_API.format(timespan)).text)
    return [(entry['date'], entry['price']) for entry in raw_transactions.values()]


def group_transactions_by_timestamp(start_time: int, end_time: int, intervals: int):
    pass


if __name__ == "__main__":
    get_bitstamp_transactions()
