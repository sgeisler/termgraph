from unittest import TestCase
from termgraph import CandleStickGraph, Candle

class BloomfilterTest(TestCase):
    def test_candle_int_4(self):
        c = Candle(1, 4, 0, 3)
        g = CandleStickGraph([c], 4)
        drawn_string = g.draw(False)

        lines = drawn_string.split("\n")
        first_candle = [line[9] for line in lines[1:-1]]

        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[0])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[1])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[2])
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[3])

    def test_candle_frac_8(self):
        c = Candle(1.5, 4, 0, 3.5)
        g = CandleStickGraph([c], 8)
        drawn_string = g.draw(False)

        lines = drawn_string.split("\n")
        first_candle = [line[9] for line in lines[1:-1]]
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[0])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[1])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[2])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[3])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[4])
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[5])
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[6])
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[7])

    def test_candle_half_1(self):
        c = Candle(1.5, 4, 0, 3.5)
        g = CandleStickGraph([c], 4)
        drawn_string = g.draw(False)

        lines = drawn_string.split("\n")
        first_candle = [line[9] for line in lines[1:-1]]
        self.assertEquals(CandleStickGraph.SYMBOL_HALF_TOP, first_candle[0])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[1])
        self.assertEquals(CandleStickGraph.SYMBOL_HALF_BOTTOM, first_candle[2])
        self.assertEquals(CandleStickGraph.SYMBOL_STICK, first_candle[3])

    def test_candle_half_2(self):
        c = Candle(1.5, 4, 1.3, 3.7)
        c_fake = Candle(0, 4, 0, 0)
        g = CandleStickGraph([c, c_fake], 4)
        drawn_string = g.draw(False)

        lines = drawn_string.split("\n")
        first_candle = [line[9] for line in lines[1:-1]]
        self.assertEquals(CandleStickGraph.SYMBOL_HALF_TOP, first_candle[0])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[1])
        self.assertEquals(CandleStickGraph.SYMBOL_HALF_CANDLE_BOTTOM, first_candle[2])
        self.assertEquals(CandleStickGraph.SYMBOL_NOTHING, first_candle[3])

    def test_candle_half_3(self):
        c = Candle(1.5, 4, 1.2, 3.8)
        c_fake = Candle(0, 4, 0, 0)
        g = CandleStickGraph([c, c_fake], 4)
        drawn_string = g.draw(False)

        lines = drawn_string.split("\n")
        first_candle = [line[9] for line in lines[1:-1]]
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[0])
        self.assertEquals(CandleStickGraph.SYMBOL_CANDLE, first_candle[1])
        self.assertEquals(CandleStickGraph.SYMBOL_HALF_BOTTOM, first_candle[2])
        self.assertEquals(CandleStickGraph.SYMBOL_NOTHING, first_candle[3])
