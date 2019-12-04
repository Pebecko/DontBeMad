from random import randint
from player import Player


class Dice:
    def __init__(self):
        self.maximal_roll = 1
        self.minimal_roll = 1
        self.min_deploy_roll = 1

        self.dice_roll = 1

    def dice_rolling(self, player=Player):
        self.dice_roll = randint(self.minimal_roll, self.maximal_roll)
        player.rolls.append(self.dice_roll)
