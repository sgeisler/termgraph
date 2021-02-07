#!/bin/env python3

import os
from termgraph import CandleStickGraph
from utils import load_data


def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(dir, "data.csv")
    example_data = load_data(fname)
    g = CandleStickGraph(example_data, 55)
    print(g.draw())


if __name__ == "__main__":
    main()
