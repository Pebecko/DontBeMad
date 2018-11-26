import random
import time
from preparation import *


class Game:
    def __init__(self):
        self.dice_roll = 0
        self.figs1 = []
        self.figs2 = []
        self.figs3 = []
        self.figs4 = []

    def game_status(self):
        # info o figurkách hráče 1
        for i in pl.player1.figures:
            self.figs1.append(i.tile.position)

        if self.figs1[0] + self.figs1[1] + self.figs1[2] + self.figs1[3] == 0:
            pl.player1.undeployed = True
            print("Hráč 1 nemá žádnou nasazenou figurku.\n")
        else:
            print("Figurky hráče jedna jsou na políčkách:", self.figs1[0], self.figs1[1], self.figs1[2],
                  self.figs1[3], "\n")

        # info o figurkách hráče 2
        for j in pl.player2.figures:
            self.figs2.append(j.tile.position)

        if self.figs2[0] + self.figs2[1] + self.figs2[2] + self.figs2[3] == 0:
            pl.player2.undeployed = True
            print("Hráč 2 nemá žádnou nasazenou figurku.\n")
        else:
            print("Figurky hráče dva jsou na políčkách:", self.figs2[0], self.figs2[1], self.figs2[2],
                  self.figs2[3], "\n")

        # info o figurkách hráče 3
        if pl.player3.playing:
            for k in pl.player3.figures:
                self.figs3.append(k.tile.position)

            if self.figs3[0] + self.figs3[1] + self.figs3[2] + self.figs3[3] == 0:
                pl.player3.undeployed = True
                print("Hráč 3 nemá žádnou nasazenou figurku.\n")
            else:
                print("Figurky hráče tři jsou na políčkách:", self.figs3[0], self.figs3[1], self.figs3[2],
                      self.figs3[3], "\n")

        # info o figurkách hráče 4
        if pl.player4.playing:
            for l in pl.player4.figures:
                self.figs4.append(l.tile.position)

            if self.figs4[0] + self.figs4[1] + self.figs4[2] + self.figs4[3] == 0:
                pl.player4.undeployed = True
                print("Hráč 4 nemá žádnou nasazenou figurku.\n")
            else:
                print("Figurky hráče čtyři jsou na políčkách:", self.figs4[0], self.figs4[1], self.figs4[2],
                      self.figs4[3], "\n")

    def side_selection(self):
        if pl.player4.playing and pl.player4.turns < pl.player3.turns:
            print("Hraje hráč 4.")
            return pl.player4
        elif pl.player3.playing and pl.player3.turns < pl.player2.turns:
            print("Hraje hráč 3.")
            return pl.player3
        elif pl.player2.turns < pl.player1.turns:
            print("Hraje hráč 2.")
            return pl.player2
        else:
            print("Hraje hráč 1.")
            return pl.player1

    def possible_moves(self, num, side):
        first = True
        fig1 = side.figures[0]
        fig2 = side.figures[1]
        fig3 = side.figures[2]
        fig4 = side.figures[3]

        # TODO - Specializované funkce na jednotlivé části

        while num == 6 or first is True:
            skip = False

            if side.undeployed is True:
                if num == 6:
                    print("Padla vám 6, nasazujete.")
                else:
                    print("Padla vám", num, ",nemůžete nasadit ale máte ještě dvě šance.")
                    for i in range(0, 2):
                        num = random.randint(1, 6)
                        if num == 6:
                            print("Padla vám 6, nasazujete.")
                            break
                        else:
                            print("Padla vám", num)
                    else:
                        print("Nemůžete nasadit, možná příště.\n")
                        skip = True

            if fig1.position != 0:
                pass

            first = False

            if num == 6:
                num = random.randint(1, 6)

        return

    def main(self):
        player_number()

        while True:
            num = random.randint(1, 6)

            self.game_status()

            side = self.side_selection()

            side.turns += 1

            time.sleep(2)


app = Game()
app.main()
