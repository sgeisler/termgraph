import csv
from termgraph import Candle


def load_data(file: str) -> [Candle]:
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # skip first row
        return [Candle(float(o), float(h), float(l), float(c)) for o, h, l, c in reader]