from math import ceil, floor
from colorama import Fore, Style
from typing import List

__version__ = '0.1.0'


class Candle:
    UP_MOVE = 1
    DOWN_MOVE = -1

    def __init__(self, begin_value: float, max_value: float, min_value: float, end_value: float):
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.begin_value = float(begin_value)
        self.end_value = float(end_value)

    @property
    def top_stick(self):
        return self.max_value

    @property
    def bottom_stick(self):
        return self.min_value

    @property
    def top_candle(self):
        return max(self.begin_value, self.end_value)

    @property
    def bottom_candle(self):
        return min(self.begin_value, self.end_value)

    @property
    def price_move(self):
        if self.begin_value > self.end_value:
            return self.DOWN_MOVE
        else:
            return self.UP_MOVE


class CandleStickGraph:
    SYMBOL_STICK = "│"
    SYMBOL_CANDLE = "┃"
    SYMBOL_HALF_TOP = "╽"
    SYMBOL_HALF_BOTTOM = "╿"
    SYMBOL_HALF_CANDLE_TOP = "╻"
    SYMBOL_HALF_CANDLE_BOTTOM = "╹"
    SYMBOL_HALF_STICK_TOP = "╷"
    SYMBOL_HALF_STICK_BOTTOM = "╵"
    SYMBOL_NOTHING = " "

    COLOR_NEUTRAL = Style.RESET_ALL
    COLOR_POSITIVE = Style.BRIGHT + Fore.GREEN
    COLOR_NEGATIVE = Style.BRIGHT + Fore.RED

    def __init__(self, data: List[Candle], height: int):
        self._height = height
        self._data = data

        self._global_min_value = min([c.bottom_stick for c in data])
        self._global_max_value = max([c.top_stick for c in data])

    def _to_height_units(self, x: float) -> float:
        return (x - self._global_min_value) / (self._global_max_value - self._global_min_value) * self._height

    def _candle_color(self, candle: Candle) -> str:
        if candle.price_move == Candle.UP_MOVE:
            return self.COLOR_POSITIVE
        else:
            return self.COLOR_NEGATIVE

    def _render_candle_at(self, candle: Candle, height_unit: int, colorize: bool) -> str:
        height_unit = float(height_unit)

        ts = self._to_height_units(candle.top_stick)
        tc = self._to_height_units(candle.top_candle)

        bs = self._to_height_units(candle.bottom_stick)
        bc = self._to_height_units(candle.bottom_candle)

        if ceil(ts) >= height_unit >= floor(tc):
            if tc - height_unit > 0.75:
                return (self._candle_color(candle) if colorize else "") + self.SYMBOL_CANDLE
            elif (tc - height_unit) > 0.25:
                if (ts - height_unit) > 0.75:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_TOP
                else:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_CANDLE_TOP
            else:
                if (ts - height_unit) > 0.75:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_STICK
                elif (ts - height_unit) > 0.25:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_STICK_TOP
                else:
                    return self.SYMBOL_NOTHING
        elif floor(tc) >= height_unit >= ceil(bc):
            return (self._candle_color(candle) if colorize else "") + self.SYMBOL_CANDLE
        elif ceil(bc) >= height_unit >= floor(bs):
            if (bc - height_unit) < 0.25:
                return (self._candle_color(candle) if colorize else "") + self.SYMBOL_CANDLE
            elif (bc - height_unit) < 0.75:
                if (bs - height_unit) < 0.25:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_BOTTOM
                else:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_CANDLE_BOTTOM
            else:
                if (bs - height_unit) < 0.25:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_STICK
                elif (bs - height_unit) < 0.75:
                    return (self._candle_color(candle) if colorize else "") + self.SYMBOL_HALF_STICK_BOTTOM
                else:
                    return self.SYMBOL_NOTHING
        else:
            return self.SYMBOL_NOTHING

    def draw(self, colorize: bool = True) -> str:
        output_str = "\n"
        for y in reversed(range(0, self._height)):
            if y % 4 == 0:
                output_str += (Style.RESET_ALL if colorize else "") + "{:8.2f} ".format(
                    self._global_min_value + (y * (self._global_max_value - self._global_min_value) / self._height))
            else:
                output_str += "         "
            for c in self._data:
                output_str += self._render_candle_at(c, y, colorize)
            output_str += "\n" + (Style.RESET_ALL if colorize else "")
        return output_str
