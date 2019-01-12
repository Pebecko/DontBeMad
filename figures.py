from tile import *


# TODO - redo import


class Figure:
    def __init__(self, number, tile, start, color=""):
        self.number = number
        self.tile = tile
        self.start = start
        self.color = color
        self.home = tile
        self.movable = False
        self.move = ""
        self.weight = 0


#definování figurek
red_figures = []
blue_figures = []
green_figures = []
yellow_figures = []
for i in range(1, 5):
    red_figures.append(Figure(i, home_red, tile1, "red"))
    blue_figures.append(Figure(i, home_blue, tile11, "blue"))
    green_figures.append(Figure(i, home_green, tile21, "green"))
    yellow_figures.append(Figure(i, home_yellow, tile31, "yellow"))
