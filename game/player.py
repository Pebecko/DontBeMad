from tactics import Tactic
from figures import Figure
from color import Color


class Player:
    def __init__(self, num, color=Color()):
        self.number = num
        self.color = color
        self.turns = 0
        self.figures = [Figure]
        self.playing = False
        self.undeployed = True
        self.has_deployed = False
        self.ai = False
        self.tactic = Tactic()
        # after game stats
        self.result = 0
        self.rolls = []
        self.inactive_turns = 0
        self.others_figures_kicked = 0
        self.own_figures_kicked = 0
