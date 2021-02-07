#!/bin/env python3

from termgraph import CandleStickGraph
from time import sleep
from examples import load_data

if __name__ == "__main__":
    example_data = load_data("data.csv")
    for i in range(1, len(example_data)):
        g = CandleStickGraph(example_data[0:i], 55)
        print(g.draw())
        sleep(0.1)