#!/bin/env python3

from termgraph import CandleStickGraph
from examples import load_data

if __name__ == "__main__":
    example_data = load_data("data.csv")
    g = CandleStickGraph(example_data, 55)
    print(g.draw())