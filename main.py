import random
import time
import tile
from preparation import *

# TODO - Side selection caring for finished players
# TODO - AI tactics
# TODO - Saving results to different file


class Game:
    def __init__(self):
        self.wait_time = 0.00
        self.dice_roll = 0
        self.figs1 = []
        self.figs2 = []
        self.figs3 = []
        self.figs4 = []
        self.players = [pl.player1, pl.player2, pl.player3, pl.player4]

    def player_placing(self, player, last=False):
        player.playing = False
        results = []
        for player_ in self.players:
            results.append(player_.result)
        if "první" not in results:
            player.result = "první"
        elif "druhý" not in results:
            player.result = "druhý"
        elif "třetí" not in results:
            player.result = "třetí"
        else:
            player.result = "čtvrtý"

        if not last:
            self.checking_last()

    def finish_control(self, player):
        for figure in player.figures:
            if figure.tile.finish is not True:
                break
        else:
            self.player_placing(player)

    def checking_last(self):
        num = 0
        player_ = None
        for player in self.players:
            if player.playing:
                num += 1
                player_ = player

        if num == 1:
            return self.player_placing(player_, True)

    def game_status(self):
        print("----------------------------------------")
        # info o figurkách hráče 1
        if pl.player1.playing:
            self.figs1 = []
            for figure in pl.player1.figures:
                if figure.tile.finish is False:
                    self.figs1.append(figure.tile.position)
                else:
                    self.figs1.append(-figure.tile.position)
            for fig in pl.player1.figures:
                if fig.tile.position != 0:
                    print("Figurky hráče jedna jsou na políčkách:", self.figs1[0], self.figs1[1], self.figs1[2],
                          self.figs1[3], "\n")
                    pl.player1.undeployed = False
                    break
            else:
                pl.player1.undeployed = True
                print("Hráč 1 nemá žádnou nasazenou figurku.\n")
            self.finish_control(pl.player1)

        # info o figurkách hráče 2
        if pl.player2.playing:
            self.figs2 = []
            for figure in pl.player2.figures:
                if figure.tile.finish is False:
                    self.figs2.append(figure.tile.position)
                else:
                    self.figs2.append(-figure.tile.position)
            for fig in pl.player2.figures:
                if fig.tile.position != 0:
                    print("Figurky hráče dva jsou na políčkách:", self.figs2[0], self.figs2[1], self.figs2[2],
                          self.figs2[3], "\n")
                    pl.player2.undeployed = False
                    break
            else:
                pl.player2.undeployed = True
                print("Hráč 2 nemá žádnou nasazenou figurku.\n")
            self.finish_control(pl.player2)

        # info o figurkách hráče 3
        if pl.player3.playing:
            self.figs3 = []
            for figure in pl.player3.figures:
                if figure.tile.finish is False:
                    self.figs3.append(figure.tile.position)
                else:
                    self.figs3.append(-figure.tile.position)
            for fig in pl.player3.figures:
                if fig.tile.position != 0:
                    print("Figurky hráče tři jsou na políčkách:", self.figs3[0], self.figs3[1], self.figs3[2],
                          self.figs3[3], "\n")
                    pl.player3.undeployed = False
                    break
            else:
                pl.player3.undeployed = True
                print("Hráč 3 nemá žádnou nasazenou figurku.\n")
            self.finish_control(pl.player3)

        # info o figurkách hráče 4
        if pl.player4.playing:
            self.figs4 = []
            for figure in pl.player4.figures:
                if figure.tile.finish is False:
                    self.figs4.append(figure.tile.position)
                else:
                    self.figs4.append(-figure.tile.position)
            for fig in pl.player4.figures:
                if fig.tile.position != 0:
                    print("Figurky hráče čtyři jsou na políčkách:", self.figs4[0], self.figs4[1], self.figs4[2],
                          self.figs4[3], "\n")
                    pl.player4.undeployed = False
                    break
            else:
                pl.player4.undeployed = True
                print("Hráč 4 nemá žádnou nasazenou figurku.\n")
            self.finish_control(pl.player4)

    def side_selection(self):
        print("========================================")
        if pl.player4.playing and pl.player4.turns < pl.player3.turns:
            print("Hraje hráč 4. -", pl.player4.color)
            return pl.player4
        elif pl.player3.playing and pl.player3.turns < pl.player2.turns:
            print("Hraje hráč 3. -", pl.player3.color)
            return pl.player3
        elif pl.player2.playing and (pl.player2.turns < pl.player1.turns or not pl.player1.playing):
            print("Hraje hráč 2. -", pl.player2.color)
            return pl.player2
        elif pl.player1.playing:
            print("Hraje hráč 1. -", pl.player1.color)
            return pl.player1

    def figure_kicking(self, tile, col):
        for player in [pl.player1, pl.player2, pl.player3, pl.player4]:
            for figure in player.figures:
                if figure.tile.position == tile.position and figure.tile.color == tile.color and figure.color != col:
                    figure.tile = figure.home
                    print("Figurka {}, hráče {}, byla vyhozena.".format(figure.number, figure.color))

    def deploying(self, fig):
        fig.tile = fig.start
        print("Nasazujete figurku {} na pozici {}.".format(fig.number, fig.start.position))

        return self.figure_kicking(fig.tile, fig.color)

    def repositioning(self, fig):
        fig.tile = self.new_coordinates(fig.tile.position, fig.color, fig.tile.finishing)
        print("Figurka {} se posunula na políčko {}.".format(fig.number, fig.tile.position))

        return self.figure_kicking(fig.tile, fig.color)

    def new_coordinates(self, pos, col, finishing, num=0):
        if num == 0:
            num = self.dice_roll
        new_pos = pos + num

        if pos == 0:
            if col == "red":
                new_tile = tile.tile1
            elif col == "blue":
                new_tile = tile.tile11
            elif col == "green":
                new_tile = tile.tile21
            else:
                new_tile = tile.tile31
        elif new_pos == 1 or new_pos == 41:
            if tile.finish_red1.color != col or not finishing:
                new_tile = tile.tile1
            else:
                new_tile = tile.finish_red1
        elif new_pos == 2 or new_pos == 42:
            if tile.finish_red1.color != col or not finishing:
                new_tile = tile.tile2
            else:
                new_tile = tile.finish_red2
        elif new_pos == 3 or new_pos == 43:
            if tile.finish_red1.color != col or not finishing:
                new_tile = tile.tile3
            else:
                new_tile = tile.finish_red3
        elif new_pos == 4 or new_pos == 44:
            if tile.finish_red1.color != col or not finishing:
                new_tile = tile.tile4
            else:
                new_tile = tile.finish_red4
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
            if tile.finish_blue1.color != col or not finishing:
                new_tile = tile.tile11
            else:
                new_tile = tile.finish_blue1
        elif new_pos == 12:
            if tile.finish_blue1.color != col or not finishing:
                new_tile = tile.tile12
            else:
                new_tile = tile.finish_blue2
        elif new_pos == 13:
            if tile.finish_blue1.color != col or not finishing:
                new_tile = tile.tile13
            else:
                new_tile = tile.finish_blue3
        elif new_pos == 14:
            if tile.finish_blue1.color != col or not finishing:
                new_tile = tile.tile14
            else:
                new_tile = tile.finish_blue4
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
            if tile.finish_green1.color != col or not finishing:
                new_tile = tile.tile21
            else:
                new_tile = tile.finish_green1
        elif new_pos == 22:
            if tile.finish_green1.color != col or not finishing:
                new_tile = tile.tile22
            else:
                new_tile = tile.finish_green2
        elif new_pos == 23:
            if tile.finish_green1.color != col or not finishing:
                new_tile = tile.tile23
            else:
                new_tile = tile.finish_green3
        elif new_pos == 24:
            if tile.finish_green1.color != col or not finishing:
                new_tile = tile.tile24
            else:
                new_tile = tile.finish_green4
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
            if tile.finish_yellow1.color != col or not finishing:
                new_tile = tile.tile31
            else:
                new_tile = tile.finish_yellow1
        elif new_pos == 32:
            if tile.finish_yellow1.color != col or not finishing:
                new_tile = tile.tile32
            else:
                new_tile = tile.finish_yellow2
        elif new_pos == 33:
            if tile.finish_yellow1.color != col or not finishing:
                new_tile = tile.tile33
            else:
                new_tile = tile.finish_yellow3
        elif new_pos == 34:
            if tile.finish_yellow1.color != col or not finishing:
                new_tile = tile.tile34
            else:
                new_tile = tile.finish_yellow4
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
                side.rolls.append(self.dice_roll)
                if self.dice_roll == 6:
                    print("Padla vám 6.")
                    break
                else:
                    print("Padla vám", self.dice_roll)

            else:
                deploy = False

        if deploy:
            self.dice_roll = random.randint(1, 6)
            side.rolls.append(self.dice_roll)
            return self.deploying(side.figures[0])

    def block_checking(self, new_tile, col):
        figs = []
        for player in [pl.player1, pl.player2, pl.player3, pl.player4]:
            if player.color == col:
                for figure in player.figures:
                    if figure.tile.position == new_tile.position and figure.tile.color == new_tile.color:
                        return True
                    else:
                        pass

        return False

    def possible_move(self, fig):
        movable = False
        new_tile = self.new_coordinates(fig.tile.position, fig.color, fig.tile.finishing)

        if fig.tile.position == 0:
            if self.dice_roll == 6 and not self.block_checking(fig.start, fig.color):
                movable = True
                move = "deploy"
            else:
                move = "undeployable"
        elif not new_tile.finish and fig.tile.finish:
            move = "illegal"
        elif self.new_coordinates(fig.tile.position, fig.color, fig.tile.finishing, 4).finish and (not new_tile.finish
                and not fig.tile.finish) and (self.dice_roll == 5 or self.dice_roll == 6):
            move = "illegal"
        elif self.block_checking(new_tile, fig.color):
            move = "blocked"
        else:
            movable = True
            move = "reposition"

        return movable, move

    def ai_move_choosing(self, side, fig1, fig1_movable, fig1_move,
                         fig2, fig2_movable, fig2_move,
                         fig3, fig3_movable, fig3_move,
                         fig4, fig4_movable, fig4_move):

        weight1, weight2, weight3, weight4 = 0, 0, 0, 0

        if fig1_movable:
            weight1 = 1

            if not fig1.tile.finish and not fig1.tile.position == 0:
                target = fig1.start.position
                if fig1.tile.position >= target:
                    target += 40
                finnish_distance = target - fig1.tile.position
                weight1 += (10 * side.tactic.finnish_distance / finnish_distance)
                print(finnish_distance, "1 k cíli")

            if fig1.tile.position == 0:
                weight1 += 10 * side.tactic.deploy

            if fig1.tile.finish:
                weight1 *= 0.1

        if fig2_movable:
            weight2 = 1

            if not fig2.tile.finish and not fig2.tile.position == 0:
                target = fig2.start.position
                if fig2.tile.position >= target:
                    target += 40
                finnish_distance = target - fig2.tile.position
                weight2 += (10 * side.tactic.finnish_distance / finnish_distance)
                print(finnish_distance, "2 k cíli")

            if fig2.tile.position == 0:
                weight2 += 10 * side.tactic.deploy

            if fig2.tile.finish:
                weight2 *= 0.1

        if fig3_movable:
            weight3 = 1

            if not fig3.tile.finish and not fig3.tile.position == 0:
                target = fig3.start.position
                if fig3.tile.position >= target:
                    target += 40
                finnish_distance = target - fig3.tile.position
                weight3 += (10 * side.tactic.finnish_distance / finnish_distance)
                print(finnish_distance, "3 k cíli")

            if fig3.tile.position == 0:
                weight3 += 10 * side.tactic.deploy

            if fig3.tile.finish:
                weight3 *= 0.1

        if fig4_movable:
            weight4 = 1

            if not fig4.tile.finish and not fig4.tile.position == 0:
                target = fig4.start.position
                if fig4.tile.position >= target:
                    target += 40
                finnish_distance = target - fig4.tile.position
                weight4 += (10 * side.tactic.finnish_distance / finnish_distance)
                print(finnish_distance, "4 k cíli")

            if fig4.tile.position == 0:
                weight4 += 10 * side.tactic.deploy

            if fig4.tile.finish:
                weight4 *= 0.1

        if weight1 >= weight2 and weight1 >= weight3 and weight1 >= weight4:
            if fig1_move == "deploy":
                self.deploying(fig1)
            elif fig1_move == "reposition":
                self.repositioning(fig1)
        elif weight2 >= weight1 and weight2 >= weight3 and weight2 >= weight4:
            if fig2_move == "deploy":
                self.deploying(fig2)
            elif fig2_move == "reposition":
                self.repositioning(fig2)
        elif weight3 >= weight1 and weight3 >= weight2 and weight3 >= weight4:
            if fig3_move == "deploy":
                self.deploying(fig3)
            elif fig3_move == "reposition":
                self.repositioning(fig3)
        else:
            if fig4_move == "deploy":
                self.deploying(fig4)
            elif fig4_move == "reposition":
                self.repositioning(fig4)

        return

    def string_compilation(self, fig1, fig2, fig3, fig4, side=pl.Player(0)):
        fig1_movable, fig1_move = self.possible_move(fig1)
        fig2_movable, fig2_move = self.possible_move(fig2)
        fig3_movable, fig3_move = self.possible_move(fig3)
        fig4_movable, fig4_move = self.possible_move(fig4)

        if side.ai:
            self.ai_move_choosing(side, fig1, fig1_movable, fig1_move,
                                  fig2, fig2_movable, fig2_move,
                                  fig3, fig3_movable, fig3_move,
                                  fig4, fig4_movable, fig4_move)

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

        mov1, mov2, mov3, mov4 = self.string_compilation(fig1, fig2, fig3, fig4, side)

        while (mov1 != "" or mov2 != "" or mov3 != "" or mov4 != "") and side.ai is False:
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
            print("Padla vám {}. Nemáte žádné tahy na výběr.\n".format(self.dice_roll))

        return

    def movement(self, side):
        if side.undeployed is True:
            self.all_home(side)

        return self.move_choosing(side)

    def main(self):
        player_number()

        print("Mínus [-] před pozicí figurky znamená, že je v domečku.")

        while True:
            self.dice_roll = random.randint(1, 6)

            self.game_status()

            side = self.side_selection()

            for player in self.players:
                if player.playing is True:
                    break
            else:
                print("Hra skončila")
                return self.results()

            side.rolls.append(self.dice_roll)

            self.movement(side)

            if self.dice_roll != 6:
                side.turns += 1

            time.sleep(self.wait_time)

    def results(self):
        avr_1, avr_2, avr_3, avr_4 = 0, 0, 0, 0
        for num in pl.player1.rolls:
            avr_1 += num
        else:
            if len(pl.player1.rolls) != 0:
                avr_1 /= len(pl.player1.rolls)

        for num in pl.player2.rolls:
            avr_2 += num
        else:
            if len(pl.player2.rolls) != 0:
                avr_2 /= len(pl.player2.rolls)

        for num in pl.player3.rolls:
            avr_3 += num
        else:
            if len(pl.player3.rolls) != 0:
                avr_3 /= len(pl.player3.rolls)

        for num in pl.player4.rolls:
            avr_4 += num
        else:
            if len(pl.player4.rolls) != 0:
                avr_4 /= len(pl.player4.rolls)

        print(pl.player1.result, avr_1, pl.player1.rolls, "\n", pl.player2.result, avr_2, pl.player2.rolls, "\n",
              pl.player3.result, avr_3, pl.player3.rolls, "\n", pl.player4.result, avr_4, pl.player4.rolls)


app = Game()
app.main()
