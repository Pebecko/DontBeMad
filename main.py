import random
import time
import tile
from preparation import *


# TODO - vstupování figurek do cíle
# TODO - zabránit figurkám opakovat kolo
# TODO - vyhazování figurek
# TODO - blokování figurek


class Game:
    def __init__(self):
        self.dice_roll = 0
        self.figs1 = []
        self.figs2 = []
        self.figs3 = []
        self.figs4 = []

    def game_status(self):
        # info o figurkách hráče 1
        self.figs1 = []
        for i in pl.player1.figures:
            self.figs1.append(i.tile.position)

        if self.figs1[0] + self.figs1[1] + self.figs1[2] + self.figs1[3] == 0:
            pl.player1.undeployed = True
            print("Hráč 1 nemá žádnou nasazenou figurku.\n")
        else:
            print("Figurky hráče jedna jsou na políčkách:", self.figs1[0], self.figs1[1], self.figs1[2],
                  self.figs1[3], "\n")
            pl.player1.undeployed = False

        # info o figurkách hráče 2
        self.figs2 = []
        for j in pl.player2.figures:
            self.figs2.append(j.tile.position)

        if self.figs2[0] + self.figs2[1] + self.figs2[2] + self.figs2[3] == 0:
            pl.player2.undeployed = True
            print("Hráč 2 nemá žádnou nasazenou figurku.\n")
        else:
            print("Figurky hráče dva jsou na políčkách:", self.figs2[0], self.figs2[1], self.figs2[2],
                  self.figs2[3], "\n")
            pl.player2.undeployed = False

        # info o figurkách hráče 3
        if pl.player3.playing:
            self.figs3 = []
            for k in pl.player3.figures:
                self.figs3.append(k.tile.position)

            if self.figs3[0] + self.figs3[1] + self.figs3[2] + self.figs3[3] == 0:
                pl.player3.undeployed = True
                print("Hráč 3 nemá žádnou nasazenou figurku.\n")
            else:
                print("Figurky hráče tři jsou na políčkách:", self.figs3[0], self.figs3[1], self.figs3[2],
                      self.figs3[3], "\n")
                pl.player3.undeployed = False

        # info o figurkách hráče 4
        if pl.player4.playing:
            self.figs4 = []
            for l in pl.player4.figures:
                self.figs4.append(l.tile.position)

            if self.figs4[0] + self.figs4[1] + self.figs4[2] + self.figs4[3] == 0:
                pl.player4.undeployed = True
                print("Hráč 4 nemá žádnou nasazenou figurku.\n")
            else:
                print("Figurky hráče čtyři jsou na políčkách:", self.figs4[0], self.figs4[1], self.figs4[2],
                      self.figs4[3], "\n")
                pl.player4.undeployed = False

    def side_selection(self):
        if pl.player4.playing and pl.player4.turns < pl.player3.turns:
            print("Hraje hráč 4. -", pl.player4.color)
            return pl.player4
        elif pl.player3.playing and pl.player3.turns < pl.player2.turns:
            print("Hraje hráč 3. -", pl.player3.color)
            return pl.player3
        elif pl.player2.turns < pl.player1.turns:
            print("Hraje hráč 2. -", pl.player2.color)
            return pl.player2
        else:
            print("Hraje hráč 1. -", pl.player1.color)
            return pl.player1

    def deploying(self, fig):
        fig.tile = fig.start
        print("Nasazujete figurku {} na pozici {}.".format(fig.number, fig.start.position))

    def repositioning(self, fig):
        fig.tile = self.new_coordinates(fig.tile.position)
        print("Figurka {} se posunula na políčko {}.".format(fig.number, fig.tile.position))

    def new_coordinates(self, pos):
        new_pos = pos + self.dice_roll

        if new_pos == 1 or new_pos == 41:
            new_tile = tile.tile1
        elif new_pos == 2 or new_pos == 42:
            new_tile = tile.tile2
        elif new_pos == 3 or new_pos == 43:
            new_tile = tile.tile3
        elif new_pos == 4 or new_pos == 44:
            new_tile = tile.tile4
        elif new_pos == 5 or new_pos == 45:
            new_tile = tile.tile5
        elif new_pos == 6 or new_pos == 46:
            new_tile = tile.tile6
        elif new_pos == 7:
            new_tile = tile.tile7
        elif new_pos == 8:
            new_tile = tile.tile8
        elif new_pos == 9:
            new_tile = tile.tile9
        elif new_pos == 10:
            new_tile = tile.tile10
        elif new_pos == 11:
            new_tile = tile.tile11
        elif new_pos == 12:
            new_tile = tile.tile12
        elif new_pos == 13:
            new_tile = tile.tile13
        elif new_pos == 14:
            new_tile = tile.tile14
        elif new_pos == 15:
            new_tile = tile.tile15
        elif new_pos == 16:
            new_tile = tile.tile16
        elif new_pos == 17:
            new_tile = tile.tile17
        elif new_pos == 18:
            new_tile = tile.tile18
        elif new_pos == 19:
            new_tile = tile.tile19
        elif new_pos == 20:
            new_tile = tile.tile20
        elif new_pos == 21:
            new_tile = tile.tile21
        elif new_pos == 22:
            new_tile = tile.tile22
        elif new_pos == 23:
            new_tile = tile.tile23
        elif new_pos == 24:
            new_tile = tile.tile24
        elif new_pos == 25:
            new_tile = tile.tile25
        elif new_pos == 26:
            new_tile = tile.tile26
        elif new_pos == 27:
            new_tile = tile.tile27
        elif new_pos == 28:
            new_tile = tile.tile28
        elif new_pos == 29:
            new_tile = tile.tile29
        elif new_pos == 30:
            new_tile = tile.tile30
        elif new_pos == 31:
            new_tile = tile.tile31
        elif new_pos == 32:
            new_tile = tile.tile32
        elif new_pos == 33:
            new_tile = tile.tile33
        elif new_pos == 34:
            new_tile = tile.tile34
        elif new_pos == 35:
            new_tile = tile.tile35
        elif new_pos == 36:
            new_tile = tile.tile36
        elif new_pos == 37:
            new_tile = tile.tile37
        elif new_pos == 38:
            new_tile = tile.tile38
        elif new_pos == 39:
            new_tile = tile.tile39
        else:
            new_tile = tile.tile40

        return new_tile

    def all_home(self, side):
        deploy = True

        if self.dice_roll == 6:
            print("Padla vám 6.")
        else:
            print("Padla vám " + str(self.dice_roll) + ", nemůžete nasadit ale máte ještě dvě šance.")
            for i in range(0, 2):
                self.dice_roll = random.randint(1, 6)
                if self.dice_roll == 6:
                    print("Padla vám 6.")
                    break
                else:
                    print("Padla vám", self.dice_roll)
            else:
                deploy = False

        if deploy:
            self.dice_roll = random.randint(1, 6)
            return self.deploying(side.figures[0])

    def possible_move(self, fig):
        movable = False
        move = ""

        if fig.tile.position == 0:
            if self.dice_roll == 6:
                movable = True
                move = "deploy"
        else:
            movable = True
            move = "reposition"

        return movable, move

    def string_compilation(self, fig1, fig2, fig3, fig4):
        fig1_movable, fig1_move = self.possible_move(fig1)
        fig2_movable, fig2_move = self.possible_move(fig2)
        fig3_movable, fig3_move = self.possible_move(fig3)
        fig4_movable, fig4_move = self.possible_move(fig4)

        mov1 = ""
        mov2 = ""
        mov3 = ""
        mov4 = ""

        if fig1_movable:
            mov1 = ", "
            if fig1_move == "deploy":
                mov1 += "nasadit"
            else:
                mov1 += "poposunout"
            mov1 += " figurku [1]"

        if fig2_movable:
            mov2 = ", "
            if fig2_move == "deploy":
                mov2 += "nasadit"
            else:
                mov2 += "poposunout"
            mov2 += " figurku [2]"

        if fig3_movable:
            mov3 = ", "
            if fig3_move == "deploy":
                mov3 += "nasadit"
            else:
                mov3 += "poposunout"
            mov3 += " figurku [3]"

        if fig4_movable:
            mov4 = ", "
            if fig4_move == "deploy":
                mov4 += "nasadit"
            else:
                mov4 += "poposunout"
            mov4 += " figurku [4]"

        return mov1, mov2, mov3, mov4

    def move_choosing(self, side):
        fig1 = side.figures[0]
        fig2 = side.figures[1]
        fig3 = side.figures[2]
        fig4 = side.figures[3]

        mov1, mov2, mov3, mov4 = self.string_compilation(fig1, fig2, fig3, fig4)

        while mov1 != "" or mov2 != "" or mov3 != "" or mov4 != "":
            print("Padla vám {}.".format(self.dice_roll))
            player_option = input("Můžete{}{}{}{}\n".format(mov1, mov2, mov3, mov4))
            if player_option == "1" and mov1 != "":
                if fig1.tile.position == 0:
                    self.deploying(fig1)
                else:
                    self.repositioning(fig1)
                break
            elif player_option == "2" and mov2 != "":
                if fig2.tile.position == 0:
                    self.deploying(fig2)
                else:
                    self.repositioning(fig2)
                break
            elif player_option == "3" and mov3 != "":
                if fig3.tile.position == 0:
                    self.deploying(fig3)
                else:
                    self.repositioning(fig3)
                break
            elif player_option == "4" and mov4 != "":
                if fig4.tile.position == 0:
                    self.deploying(fig4)
                else:
                    self.repositioning(fig4)
                break
            else:
                print("Zadaná možnost nesouhlasí s možnostmi.\n")
        else:
            print("Nemáte žádné tahy.\n")

        return

    def movement(self, side):
        if side.undeployed is True:
            self.all_home(side)

        return self.move_choosing(side)

    def main(self):
        player_number()

        while True:
            self.dice_roll = random.randint(1, 6)

            self.game_status()

            side = self.side_selection()

            self.movement(side)

            if self.dice_roll != 6:
                side.turns += 1

            time.sleep(1)


app = Game()
app.main()
