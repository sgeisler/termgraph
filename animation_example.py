from graph import CandleStickGraph
from example_data import example_data
from time import sleep

for i in range(1, len(example_data)):
    g = CandleStickGraph(example_data[0:i], 55)
    print(g.draw())
    sleep(0.1)