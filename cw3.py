class Color:
    """Класс Color, который выводит ● в заданном цвете RGB"""
    END = "\033[0"
    START = "\033[1;38;2"
    MOD = "m"

    def __init__(self, r, g, b):
        self.red_level = r
        self.green_level = g
        self.blue_level = b

    def __repr__(self):
        return f"{self.START};{self.red_level};{self.green_level};{self.blue_level}{self.MOD}●{self.END}{self.MOD}"

    @staticmethod
    def _is_correct_ch(channel):
        if not isinstance(channel, int):
            raise ValueError(f"{type(channel)} != int")

        if not 0 <= channel <= 255:
            raise ValueError("Channel > 255 or Channel < 0")

    @property
    def red_level(self):
        return self.red_level_

    @property
    def green_level(self):
        return self.green_level_

    @property
    def blue_level(self):
        return self.blue_level_

    @red_level.setter
    def red_level(self, channel):
        Color._is_correct_ch(channel)
        self.red_level_ = channel

    @blue_level.setter
    def blue_level(self, channel):
        Color._is_correct_ch(channel)
        self.blue_level_ = channel

    @green_level.setter
    def green_level(self, channel):
        Color._is_correct_ch(channel)
        self.green_level_ = channel

    def __eq__(self, other):
        """Сравнение цветов"""
        if self is other:
            return True
        return (self.red_level == other.red_level) and (self.green_level == other.green_level) \
            and (self.blue_level == other.blue_level)

    def __add__(self, other):
        """Смешение цветов"""
        return Color(self.red_level + other.red_level, self.green_level + other.green_level,
                     self.blue_level + other.blue_level)

    def __hash__(self):
        """Вывод уникальных цветов из списка"""
        return hash((self.red_level, self.green_level, self.blue_level))

    def __mul__(self, other):
        """Уменьшение контраста цвета"""
        if other < 0 or other > 1:
            raise ValueError("Contrast constant must be between 0 and 1")
        cl = -256 * (1 - other)
        f = 259 * (cl + 255) / (255 * (259 - cl))
        r = int(f * (self.red_level - 128) + 128)
        g = int(f * (self.green_level - 128) + 128)
        b = int(f * (self.blue_level - 128) + 128)
        return Color(r, g, b)

    def __rmul__(self, other):
        return self.__mul__(other)


if __name__ == '__main__':
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    orange1 = Color(255, 165, 0)
    orange2 = Color(255, 165, 0)
    color_list = [orange1, red, green, orange2]
    print(red)
    print(red == green)
    print(red + green)
    print(set(color_list))
    print(0.5 * red)
    print(red * 0.8)
