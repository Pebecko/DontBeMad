from tactics import *
from figures import Figure, figures


# TODO - vylepšit kontrolu stejných prvních písmen u jednotlivých barev


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


# identical strings detections
color_names = []
for figs in figures:
    color_names.append(figs[0].language_color)

same_letters = []
for name in color_names:
    color_names.remove(name)
    for nm in color_names:
        if name[0] == nm[0]:
            same_letters.append(nm)

wanted_input = []
end_part = []
for figs in figures:
    if figs[0].language_color not in same_letters:
        wanted_input.append(figs[0].language_color[0])
        end_part.append((figs[0].language_color[1:]))
    else:
        wanted_input.append(figs[0].language_color)
        end_part.append("")

# definování hráčů
players = []
player_traits = []
for i in range(len(figures)):
    player_traits.append([figures[i], figures[i][0].color, "[" + wanted_input[i] + "]" + end_part[i], wanted_input[i]])

    players.append(Player(i + 1))
