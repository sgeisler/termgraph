#!/bin/env python3

import os
from termgraph import CandleStickGraph
from time import sleep
from examples import load_data


def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(dir, "data.csv")
    example_data = load_data(fname)
    for i in range(1, len(example_data)):
        g = CandleStickGraph(example_data[0:i], 55)
        print(g.draw())
        sleep(0.1)


if __name__ == "__main__":
    main()
