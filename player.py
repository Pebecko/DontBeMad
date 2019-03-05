from tactics import *
from figures import Figure, figures


# TODO - přidat kontrolu stejných prvních písmen u jednotlivých barev


class Player:
    def __init__(self, num, color=""):
        self.number = num
        self.color = color
        self.turns = 0
        self.figures = [Figure]
        self.playing = False
        self.undeployed = True
        self.result = 0
        self.rolls = []
        self.ai = False
        self.tactic = Tactic()


# definování hráčů
players = []
player_traits = []
for i in range(len(figures)):
    player_traits.append([figures[i], figures[i][0].color, "[" + figures[i][0].language_color[0] + "]" +
                         figures[i][0].language_color[1:], figures[i][0].language_color[0]])

    players.append(Player(i))
