from tile import Tile


class Figure:
    def __init__(self, number, tile, start, color=""):
        self.number = number
        self.tile = tile
        self.start = start
        self.color = color
        self.home = tile
        self.movable = False
        self.move = ""
        self.move_mess = ""
        self.weight = 0


# definování figurek
red_figures = []
blue_figures = []
green_figures = []
yellow_figures = []
white_figures = []
orange_figures = []
purple_figures = []

for i in range(1, 5):
    red_figures.append(Figure(i, Tile(0, color="red", home=True), Tile(0, finishing=False), "red"))
    blue_figures.append(Figure(i, Tile(0, color="blue", home=True), Tile(1, finishing=False), "blue"))
    green_figures.append(Figure(i, Tile(0, color="green", home=True), Tile(2, finishing=False), "green"))
    yellow_figures.append(Figure(i, Tile(0, color="yellow", home=True), Tile(3, finishing=False), "yellow"))
    white_figures.append(Figure(i, Tile(0, color="black", home=True), Tile(4, finishing=False), "black"))
    orange_figures.append(Figure(i, Tile(0, color="orange", home=True), Tile(5, finishing=False), "orange"))
    purple_figures.append(Figure(i, Tile(0, color="purple", home=True), Tile(6, finishing=False), "purple"))
figures = [red_figures, blue_figures, green_figures, yellow_figures, white_figures, orange_figures, purple_figures]