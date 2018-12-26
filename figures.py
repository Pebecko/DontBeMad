import tile


class Figure:
    def __init__(self, number, tile, start, color=""):
        self.number = number
        self.tile = tile
        self.start = start
        self.color = color
        self.home = tile


# definování figurek
red_fig1 = Figure(1, tile.home_red, tile.tile31, "red")
red_fig2 = Figure(2, tile.home_red, tile.tile31, "red")
red_fig3 = Figure(3, tile.home_red, tile.tile31, "red")
red_fig4 = Figure(4, tile.home_red, tile.tile31, "red")
blue_fig1 = Figure(1, tile.home_blue, tile.tile11, "blue")
blue_fig2 = Figure(2, tile.home_blue, tile.tile11, "blue")
blue_fig3 = Figure(3, tile.home_blue, tile.tile11, "blue")
blue_fig4 = Figure(4, tile.home_blue, tile.tile11, "blue")
green_fig1 = Figure(1, tile.home_green, tile.tile11, "green")
green_fig2 = Figure(2, tile.home_green, tile.tile11, "green")
green_fig3 = Figure(3, tile.home_green, tile.tile11, "green")
green_fig4 = Figure(4, tile.home_green, tile.tile11, "green")
yellow_fig1 = Figure(1, tile.home_yellow, tile.tile21, "yellow")
yellow_fig2 = Figure(2, tile.home_yellow, tile.tile21, "yellow")
yellow_fig3 = Figure(3, tile.home_yellow, tile.tile21, "yellow")
yellow_fig4 = Figure(4, tile.home_yellow, tile.tile21, "yellow")
