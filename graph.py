from math import ceil, floor
from colorama import Fore, Style

class Candle:
    UP_MOVE = 1
    DOWN_MOVE = -1

    def __init__(self, min_value: float, max_value: float, begin_value: float, end_value: float):
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

    def __init__(self, height: int):
        self._height = height

    def draw(self, data: [Candle]) -> str:
        global_min_value = min([c.bottom_stick for c in data])
        global_max_value = max([c.top_stick for c in data])

        def to_height_units(x: float) -> float:
            return (x - global_min_value) / (global_max_value - global_min_value) * self._height

        def candle_color(candle: Candle) -> str:
            if candle.price_move == Candle.UP_MOVE:
                return self.COLOR_POSITIVE
            else:
                return self.COLOR_NEGATIVE

        def render_candle_at(candle: Candle, height_unit: int) -> str:
            height_unit = float(height_unit)

            ts = to_height_units(candle.top_stick)
            tc = to_height_units(candle.top_candle)

            bs = to_height_units(candle.bottom_stick)
            bc = to_height_units(candle.bottom_candle)

            if height_unit <= ceil(ts) and height_unit >= floor(tc):
                if (tc - height_unit > 0.75):
                    return candle_color(candle) + self.SYMBOL_CANDLE
                elif (tc - height_unit) > 0.25:
                    if (ts - height_unit > 0.75):
                        return candle_color(candle) + self.SYMBOL_HALF_TOP
                    else:
                        return candle_color(candle) + self.SYMBOL_HALF_CANDLE_TOP
                else:
                    if (ts - height_unit) > 0.75:
                        return self.COLOR_NEUTRAL + self.SYMBOL_STICK
                    elif (ts - height_unit) > 0.25:
                        return self.COLOR_NEUTRAL + self.SYMBOL_HALF_STICK_TOP
                    else:
                        return self.SYMBOL_NOTHING
            elif height_unit <= ceil(tc) and height_unit >= floor(bc):
                return candle_color(candle) + self.SYMBOL_CANDLE
            elif height_unit <= ceil(bc) and height_unit >= floor(bs):
                if (bc - height_unit) < 0.25:
                    return candle_color(candle) + self.SYMBOL_CANDLE
                elif (bc - height_unit) < 0.75:
                    if (bs - height_unit) < 0.25:
                        return candle_color(candle) + self.SYMBOL_HALF_BOTTOM
                    else:
                        return candle_color(candle) + self.SYMBOL_HALF_CANDLE_BOTTOM
                else:
                    if (bs - height_unit) < 0.25:
                        return self.COLOR_NEUTRAL + self.SYMBOL_STICK
                    elif (bs - height_unit) < 0.75:
                        return self.COLOR_NEUTRAL + self.SYMBOL_HALF_STICK_BOTTOM
                    else:
                        return self.SYMBOL_NOTHING
            else:
                return self.SYMBOL_NOTHING

        output_str = "\n"
        for y in reversed(range(0, self._height)):
            if y % 4 == 0:
                output_str += Style.RESET_ALL + "{:8.2f} ".format(global_min_value + (y * (global_max_value - global_min_value) / self._height))
            else:
                output_str += "         "
            for c in data:
                output_str += render_candle_at(c, y)
            output_str += "\n" + Style.RESET_ALL
        return output_str
