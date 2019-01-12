class Tile:
    def __init__(self, position, color="", home=False, finish=False, finishing=True):
        self.position = position
        self.color = color
        self.home = home
        self.finish = finish
        self.finishing = finishing


# definování polí
home_red = Tile(0, color="red", home=True)
home_blue = Tile(0, color="blue", home=True)
home_green = Tile(0, color="green", home=True)
home_yellow = Tile(0, color="yellow", home=True)

finish_red1 = Tile(1, color="red", finish=True)
finish_red2 = Tile(2, color="red", finish=True)
finish_red3 = Tile(3, color="red", finish=True)
finish_red4 = Tile(4, color="red", finish=True)
finish_blue1 = Tile(11, color="blue", finish=True)
finish_blue2 = Tile(12, color="blue", finish=True)
finish_blue3 = Tile(13, color="blue", finish=True)
finish_blue4 = Tile(14, color="blue", finish=True)
finish_green1 = Tile(21, color="green", finish=True)
finish_green2 = Tile(22, color="green", finish=True)
finish_green3 = Tile(23, color="green", finish=True)
finish_green4 = Tile(24, color="green", finish=True)
finish_yellow1 = Tile(31, color="yellow", finish=True)
finish_yellow2 = Tile(32, color="yellow", finish=True)
finish_yellow3 = Tile(33, color="yellow", finish=True)
finish_yellow4 = Tile(34, color="yellow", finish=True)
