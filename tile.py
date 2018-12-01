class Tile:
    def __init__(self, position, color="", home=False, finish=False):
        self.position = position
        self.color = color
        self.home = home
        self.finish = finish
        self.finishing = True


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

tile1 = Tile(1)
tile2 = Tile(2)
tile3 = Tile(3)
tile4 = Tile(4)
tile5 = Tile(5)
tile6 = Tile(6)
tile7 = Tile(7)
tile8 = Tile(8)
tile9 = Tile(9)
tile10 = Tile(10)
tile11 = Tile(11)
tile12 = Tile(12)
tile13 = Tile(13)
tile14 = Tile(14)
tile15 = Tile(15)
tile16 = Tile(16)
tile17 = Tile(17)
tile18 = Tile(18)
tile19 = Tile(19)
tile20 = Tile(20)
tile21 = Tile(21)
tile22 = Tile(22)
tile23 = Tile(23)
tile24 = Tile(24)
tile25 = Tile(25)
tile26 = Tile(26)
tile27 = Tile(27)
tile28 = Tile(28)
tile29 = Tile(29)
tile30 = Tile(30)
tile31 = Tile(31)
tile32 = Tile(32)
tile33 = Tile(33)
tile34 = Tile(34)
tile35 = Tile(35)
tile36 = Tile(36)
tile37 = Tile(37)
tile38 = Tile(38)
tile39 = Tile(39)
tile40 = Tile(40)

tile1.finishing = False
tile2.finishing = False
tile3.finishing = False
tile11.finishing = False
tile12.finishing = False
tile13.finishing = False
tile21.finishing = False
tile22.finishing = False
tile23.finishing = False
tile31.finishing = False
tile32.finishing = False
tile33.finishing = False
