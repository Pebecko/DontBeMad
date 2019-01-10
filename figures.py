import tile


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


# definování figurek
#Proc ne takhle?
# red_figures = []
# blue_figures = []
# green_figures = []
# yellow_figures = []
# for i in range(1, 4):
#     red_figures.append(Figure(i, tile.home_red, Tile(1), "red"))
#     blue_figures.append(Figure(i, tile.home_blue, Tile(11), "blue"))
#     green_figures.append(Figure(i, tile.home_green, Tile(21), "green"))
#    yellow_figures.append(Figure(i, tile.home_yellow, Tile(31), "yellow"))

red_fig1 = Figure(1, tile.home_red, tile.tile1, "red")
red_fig2 = Figure(2, tile.home_red, tile.tile1, "red")
red_fig3 = Figure(3, tile.home_red, tile.tile1, "red")
red_fig4 = Figure(4, tile.home_red, tile.tile1, "red")
blue_fig1 = Figure(1, tile.home_blue, tile.tile11, "blue")
blue_fig2 = Figure(2, tile.home_blue, tile.tile11, "blue")
blue_fig3 = Figure(3, tile.home_blue, tile.tile11, "blue")
blue_fig4 = Figure(4, tile.home_blue, tile.tile11, "blue")
green_fig1 = Figure(1, tile.home_green, tile.tile21, "green")
green_fig2 = Figure(2, tile.home_green, tile.tile21, "green")
green_fig3 = Figure(3, tile.home_green, tile.tile21, "green")
green_fig4 = Figure(4, tile.home_green, tile.tile21, "green")
yellow_fig1 = Figure(1, tile.home_yellow, tile.tile31, "yellow")
yellow_fig2 = Figure(2, tile.home_yellow, tile.tile31, "yellow")
yellow_fig3 = Figure(3, tile.home_yellow, tile.tile31, "yellow")
yellow_fig4 = Figure(4, tile.home_yellow, tile.tile31, "yellow")
