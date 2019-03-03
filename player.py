from tactics import *
from figures import Figure, red_figures, blue_figures, green_figures, yellow_figures, white_figures, orange_figures, \
    purple_figures


# TODO - Zautomatizovat player_traits (vše si budou brát jen z figurek)


class Player:
    def __init__(self, num, color=""):
        self.number = num
        self.color = color
        self.turns = 0
        self.figures = [Figure]
        self.playing = False
        self.undeployed = True
        self.result = ""
        self.rolls = []
        self.ai = False
        self.tactic = Tactic()


# definování hráčů
players = []
player_traits = [[red_figures, "red", "[č]ervená", "č"],
                 [blue_figures, "blue", "[m]odrá", "m"],
                 [green_figures, "green", "[z]elená", "z"],
                 [yellow_figures, "yellow", "[ž]lutá", "ž"],
                 [white_figures, "white", "[b]ílá", "b"],
                 [orange_figures, "orange", "[o]ranžová", "o"],
                 [purple_figures, "purple", "[f]ialová", "f"]]
for i in range(1, len(player_traits) + 1):
    players.append(Player(i))
