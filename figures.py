from tile import Tile


class Figure:
    def __init__(self, number, tile, start, color="", lang_color=""):
        self.number = number
        self.tile = tile
        self.start = start
        self.color = color
        self.language_color = lang_color
        self.home = tile
        self.movable = False
        self.move = ""
        self.move_mess = ""
        self.weight = 0


# definování barev - pro přidání nového hráče stačí přidat - {, ["barva anglicky", "barva česky"]} do colors
# zatím je potřeba kontrolovat, že první písmena barev v češtině nejsou stejná
colors = [["red", "červená"], ["blue", "modrá"], ["green", "zelená"], ["yellow", "žlutá"], ["white", "bílá"],
          ["orange", "oranžová"], ["purple", "fialová"], ["pink", "růžová"]]

# definování figurek
figures = [[] for x in range(0, len(colors))]

for i in range(0, len(colors)):
    for j in range(1, 5):
        figures[i].append(Figure(j, Tile(0, color=colors[i][0], home=True), Tile(i, finishing=False), colors[i][0],
                                 colors[i][1]))
