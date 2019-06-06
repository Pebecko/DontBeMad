from color import Color


class Figure:
    def __init__(self, number, tile, start, color=Color()):
        self.number = number
        self.tile = tile
        self.start = start
        self.color = color
        self.home = tile
        self.movable = False
        self.move = ""
        self.move_mess = ""
        self.weight = 0
