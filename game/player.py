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
        self.result = 0
        self.rolls = []
        self.ai = False
        self.tactic = Tactic()
