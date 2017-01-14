from graph import CandleStickGraph
from example_data import example_data
from time import sleep

g = CandleStickGraph(55)
for i in range(1, len(example_data)):
    print(g.draw(example_data[0:i]))
    sleep(0.1)