import random
import time
from player import player1, player2, player3, player4, Player
from figures import *
from preparation import player_number
from tactics import move_nearest, kicker, deployer


# nastavení UI
player1.ai = True
player2.ai = True
player3.ai = True
player4.ai = True
player1.tactic = move_nearest
player2.tactic = deployer
player3.tactic = kicker


# TODO - better AI


class Game:
    def __init__(self):
        self.no_moving_while_dep = False  # pravidlo pro posouvání figurek když můžete nasadit

        self.wait_time = 0  # čas, který hra čeká po každém tahu
        self.dice_roll = 0
        self.playing = True
        self.repeating = False  # pokud má hra opakovat vše se stejným nastavením

        #Proc to neni v poli?
        self.fig1 = None
        self.fig2 = None
        self.fig3 = None
        self.fig4 = None
        self.current_fig = None

        self.players = [player1, player2, player3, player4]
        self.current_player = Player(0)

    # oznamování stavu hry
    def game_status(self):
        print("----------------------------------------")
        # info o figurkách hráčů
        for player in self.players:
            if player.playing:
                figs = []
                for figure in player.figures:
                    if figure.tile.finish is False:
                        figs.append(figure.tile.position)
                    else:
                        figs.append(-figure.tile.position)

                    #Proc by to neslo takhle?
                    # if fig.tile.position != 0:
                    #     print("Figurky hráče {} jsou na políčkách:".format(player.number), figs[0], figs[1], figs[2],
                    #           figs[3], "\n")
                    #     player.undeployed = False
                for fig in player.figures:
                    if fig.tile.position != 0:
                        print("Figurky hráče {} jsou na políčkách:".format(player.number), figs[0], figs[1], figs[2],
                              figs[3], "\n")
                        player.undeployed = False
                        break
                else:
                    player.undeployed = True
                    print("Hráč {} nemá žádnou nasazenou figurku.\n".format(player.number))
                self.finish_control(player)

    # vybírání hrajícího hráče
    def side_selection(self):
        # TODO - rework player choosing
        print("========================================")
        if player4.playing and ((player4.turns < player3.turns and player3.playing)
                                or (not player3.playing and player2.playing and player4.turns < player2.turns)
                                or (not player3.playing and not player2.playing and player1.playing and
                                player4.turns < player1.turns)):
            print("Hraje hráč 4. -", player4.color)
            self.current_player = player4
        elif player3.playing and ((player3.turns < player2.turns and player2.playing)
                                  or (not player1.playing and not player2.playing)
                                  or player3.turns < player1.turns and player1.playing and not player2.playing):
            print("Hraje hráč 3. -", player3.color)
            self.current_player = player3
        elif player2.playing and (player2.turns < player1.turns or not player1.playing):
            print("Hraje hráč 2. -", player2.color)
            self.current_player = player2
        elif player1.playing:
            print("Hraje hráč 1. -", player1.color)
            self.current_player = player1
        else:
            # pojistka pro případ, že by jeden hráč dohrál dřív
            player1.turns, player2.turns, player3.turns, player4.turns = 0, 0, 0, 0
            return self.side_selection()

    def main(self):
        if not self.repeating:
            player_number()

            print("Mínus [-] před pozicí figurky znamená, že je v domečku.")

        # herní smyčka
        while self.playing:
            # vybírání aktuálně hrajícího hráče
            self.side_selection()

            # pohyb hráčových figurek
            self.movement()

            # oznamování stavu hry
            self.game_status()

            # zjišťování jestli nemá hráč hrát znovu
            if self.dice_roll != 6:
                self.current_player.turns += 1

            time.sleep(self.wait_time)

        print("Hra skončila")
        return self.results()

    # vyhazování figurek
    def figure_kicking(self):
        for player in self.players:
            for figure in player.figures:
                if figure.tile.position == self.current_fig.tile.position and (figure.tile.color ==
                                                                               self.current_fig.tile.color and
                                                                               figure.color != self.current_fig.color):
                    figure.tile = figure.home
                    print("Figurka {}, hráče {} - {}, byla vyhozena."
                          "".format(figure.number, player.number, figure.color))

    # nasazování figurky
    def deploying(self):
        self.current_fig.tile = self.current_fig.start
        print(
            "Nasazujete figurku {} na pozici {}.".format(self.current_fig.number, self.current_fig.start.position))

        return self.figure_kicking()

    # posouvábí figurky
    def repositioning(self):
        self.current_fig.tile = self.new_coordinates(self.current_fig.tile.position, self.current_fig.color,
                                                     self.current_fig.tile.finishing)
        print(
            "Figurka {} se posunula na políčko {}.".format(self.current_fig.number, self.current_fig.tile.position))

        return self.figure_kicking()

    # zjišťování nové pozice
    #Proc proste jen new_title = Tile(new_pos)
    def new_coordinates(self, pos, col, finishing, num=0):
        if num == 0:
            num = self.dice_roll
        new_pos = pos + num

        # return tile.all[new_pos-1] Proc
        
        if pos == 0:
            if col == "red":
                new_tile = Tile(1, finishing=False)
            elif col == "blue":
                new_tile = Tile(11, finishing=False)
            elif col == "green":
                new_tile = Tile(21, finishing=False)
            else:
                new_tile = Tile(31, finishing=False)
        elif new_pos == 1 or new_pos == 41:
            if finish_red1.color != col or not finishing:
                new_tile = Tile(1, finishing=False)
            else:
                new_tile = finish_red1
        elif new_pos == 2 or new_pos == 42:
            if finish_red1.color != col or not finishing:
                new_tile = Tile(2, finishing=False)
            else:
                new_tile = finish_red2
        elif new_pos == 3 or new_pos == 43:
            if finish_red1.color != col or not finishing:
                new_tile = Tile(3, finishing=False)
            else:
                new_tile = finish_red3
        elif new_pos == 4 or new_pos == 44:
            if finish_red1.color != col or not finishing:
                new_tile = Tile(4, finishing=False)
            else:
                new_tile = finish_red4
        elif new_pos == 5 or new_pos == 45:
            new_tile = Tile(5, finishing=False)
        elif new_pos == 6 or new_pos == 46:
            new_tile = Tile(6, finishing=False)
        elif new_pos == 11:
            if finish_blue1.color != col or not finishing:
                new_tile = Tile(11, finishing=False)
            else:
                new_tile = finish_blue1
        elif new_pos == 12:
            if finish_blue1.color != col or not finishing:
                new_tile = Tile(12, finishing=False)
            else:
                new_tile = finish_blue2
        elif new_pos == 13:
            if finish_blue1.color != col or not finishing:
                new_tile = Tile(13, finishing=False)
            else:
                new_tile = finish_blue3
        elif new_pos == 14:
            if finish_blue1.color != col or not finishing:
                new_tile = Tile(14, finishing=False)
            else:
                new_tile = finish_blue4
        elif new_pos == 21:
            if finish_green1.color != col or not finishing:
                new_tile = Tile(21, finishing=False)
            else:
                new_tile = finish_green1
        elif new_pos == 22:
            if finish_green1.color != col or not finishing:
                new_tile = Tile(22, finishing=False)
            else:
                new_tile = finish_green2
        elif new_pos == 23:
            if finish_green1.color != col or not finishing:
                new_tile = Tile(23, finishing=False)
            else:
                new_tile = finish_green3
        elif new_pos == 24:
            if finish_green1.color != col or not finishing:
                new_tile = Tile(24, finishing=False)
            else:
                new_tile = finish_green4
        elif new_pos == 31:
            if finish_yellow1.color != col or not finishing:
                new_tile = Tile(31, finishing=False)
            else:
                new_tile = finish_yellow1
        elif new_pos == 32:
            if finish_yellow1.color != col or not finishing:
                new_tile = Tile(32, finishing=False)
            else:
                new_tile = finish_yellow2
        elif new_pos == 33:
            if finish_yellow1.color != col or not finishing:
                new_tile = Tile(33, finishing=False)
            else:
                new_tile = finish_yellow3
        elif new_pos == 34:
            if finish_yellow1.color != col or not finishing:
                new_tile = Tile(34, finishing=False)
            else:
                new_tile = finish_yellow4
        else:
            new_tile = Tile(new_pos)

        return new_tile

    # všechny figurky v domečku => 3 šance na nasazení
    def all_home(self):
        if self.dice_roll == 6:
            print("Padla vám 6.")
        else:
            print("Padla vám " + str(self.dice_roll) + ", nemůžete nasadit ale máte ještě dvě šance.")
            for j in range(0, 2):
                self.dice_roll = random.randint(1, 6)
                self.current_player.rolls.append(self.dice_roll)
                if self.dice_roll == 6:
                    print("Padla vám 6.")
                    break
                elif j == 0:
                    print("Padla vám", self.dice_roll)
            else:
                return

        self.dice_roll = random.randint(1, 6)
        self.current_player.rolls.append(self.dice_roll)
        self.current_fig = self.current_player.figures[0]
        return self.deploying()

    # kontrolování že na novém políčku nestojí žádná z vlastních figurek
    def block_checking(self, new_tile):
        for figure in self.current_player.figures:
            if figure.tile.position == new_tile.position and figure.tile.color == new_tile.color:
                return True

        return False

    # zjišťování možných akcí figurky
    def possible_move(self):
        for figure in self.current_player.figures:
            new_tile = self.new_coordinates(figure.tile.position, figure.color, figure.tile.finishing)
            figure.movable = False

            if figure.tile.position == 0:
                if self.dice_roll == 6 and not self.block_checking(figure.start):
                    figure.movable = True
                    figure.move = "deploy"
                else:
                    figure.move = "undeployable"
            elif not new_tile.finish and figure.tile.finish:
                figure.move = "illegal"
            elif self.new_coordinates(figure.tile.position, figure.color, figure.tile.finishing, 4).finish and (
                    not new_tile.finish
                    and not figure.tile.finish) and (self.dice_roll == 5 or self.dice_roll == 6):
                figure.move = "illegal"
            elif self.block_checking(new_tile):
                figure.move = "blocked"
            else:
                if self.dice_roll == 6 and self.no_moving_while_dep:
                    for fig in self.current_player.figures:
                        if fig.tile.position == 0:
                            fig.move = "illegal"
                            break
                    else:
                        figure.movable = True
                        figure.move = "reposition"
                else:
                    figure.movable = True
                    figure.move = "reposition"

        return

    # skládání zprávy pro hráče o možných pohybech
    def string_compilation(self):
        self.possible_move()

        # vybírání tahu AI
        if self.current_player.ai:
            self.ai_move_choosing()

        # moves = [] Proc zase pole
        mov1, mov2, mov3, mov4 = "", "", "", "" #Proc by nestacilo jen mov1, mov2, mov3, mov4 = "",?

        if self.fig1.movable:
            mov1 = ", "
            if self.fig1.move == "deploy":
                mov1 += "nasadit"
            else:
                mov1 += "poposunout"
            mov1 += " figurku [1]"

        if self.fig2.movable:
            mov2 = ", "
            if self.fig2.move == "deploy":
                mov2 += "nasadit"
            else:
                mov2 += "poposunout"
            mov2 += " figurku [2]"

        if self.fig3.movable:
            mov3 = ", "
            if self.fig3.move == "deploy":
                mov3 += "nasadit"
            else:
                mov3 += "poposunout"
            mov3 += " figurku [3]"

        if self.fig4.movable:
            mov4 = ", "
            if self.fig4.move == "deploy":
                mov4 += "nasadit"
            else:
                mov4 += "poposunout"
            mov4 += " figurku [4]"

        return mov1, mov2, mov3, mov4

    # ui si vybírá tah
    def ai_move_choosing(self):
        for figure in self.current_player.figures:
            # figurka může hrát
            if figure.movable:
                figure.weight = 1

                # figurka je v domečku
                if figure.tile.position == 0:
                    figure.weight += 10 * self.current_player.tactic.deploy

                # figurka je v cíli
                elif figure.tile.finish:
                    figure.weight *= 0.1

                # figurka je v herním poli
                else:
                    # zjišťování jak daleko je figurka od cíle
                    target = figure.start.position
                    if figure.tile.position >= target:
                        target += 40
                    finnish_distance = target - figure.tile.position
                    if finnish_distance != 0:
                        figure.weight += (200 * (self.current_player.tactic.finnish_distance / finnish_distance))

                    # zjišťování zda figurka neblokuje startovací políčko
                    if figure.tile.position == figure.start.position and figure.tile.color == figure.start.color:
                        figure.weight += 10 * self.current_player.tactic.clearing_start

                # zjišťování zda figurka nemůže vyhodit jinou figurku svým tahem
                new_tile = self.new_coordinates(figure.tile.position, figure.color, figure.tile.finishing)
                for player in self.players:
                    for fig in player.figures:
                        if new_tile.color == fig.tile.color and new_tile.position == fig.tile.position:
                            figure.weight += 10 * self.current_player.tactic.kicking_out

            else:
                figure.weight = 0

            # debug
            print(figure.weight)

        if self.fig1.weight >= self.fig2.weight and self.fig1.weight >= self.fig3.weight \
                and self.fig1.weight >= self.fig4.weight:
            self.current_fig = self.fig1
        elif self.fig2.weight >= self.fig1.weight and self.fig2.weight >= self.fig3.weight \
                and self.fig2.weight >= self.fig4.weight:
            self.current_fig = self.fig2
        elif self.fig3.weight >= self.fig1.weight and self.fig3.weight >= self.fig2.weight \
                and self.fig3.weight >= self.fig4.weight:
            self.current_fig = self.fig3
        else:
            self.current_fig = self.fig4

        if self.current_fig.move == "deploy":
            self.deploying()
        elif self.current_fig.move == "reposition":
            self.repositioning()

        return

    # hráč si vybírá, jaký tah zahraje
    def move_choosing(self):
        self.fig1, self.fig2, self.fig3, self.fig4 = self.current_player.figures[0:4]

        mov1, mov2, mov3, mov4 = self.string_compilation()

        while (mov1 != "" or mov2 != "" or mov3 != "" or mov4 != "") and self.current_player.ai is False:
            print("Padla vám {}.".format(self.dice_roll))
            player_option = input("Můžete{}{}{}{}\n".format(mov1, mov2, mov3, mov4))
            if player_option == "1" and mov1 != "":
                self.current_fig = self.fig1
                break
            elif player_option == "2" and mov2 != "":
                self.current_fig = self.fig2
                break
            elif player_option == "3" and mov3 != "":
                self.current_fig = self.fig3
                break
            elif player_option == "4" and mov4 != "":
                self.current_fig = self.fig4
                break
            else:
                print("Zadaná možnost nesouhlasí s možnostmi.\n")
        else:
            print("Padla vám {}. Nemáte žádné tahy na výběr.\n".format(self.dice_roll))
            return

        if self.current_fig.tile.position == 0:
            self.deploying()
        else:
            self.repositioning()

        return

    # vybírání zda se má házet třikrát, nebo ne
    def movement(self):
        # házení kostkou
        self.dice_roll = random.randint(1, 6)

        self.current_player.rolls.append(self.dice_roll)

        if self.current_player.undeployed is True:
            self.all_home()

        return self.move_choosing()

    # kontrola figurek v cíli
    def finish_control(self, player):
        for figure in player.figures:
            if figure.tile.finish is not True:
                return
        # všechny figurky jsou v cíli
        else:
            self.player_placing(player)

    # kontrolování zda hráč není poslední ve hře
    def checking_last(self):
        num = 0
        player = None
        for pl in self.players:
            if pl.playing:
                num += 1
                player = pl

        # poslední hráč ve hře
        if num == 1:
            self.playing = False
            return self.player_placing(player, True)

    # umisťování hráčů
    def player_placing(self, player, last=False):
        player.playing = False
        results = []
        for pl in self.players:
            results.append(pl.result)
        if "první" not in results:
            player.result = "první"
        elif "druhý" not in results:
            player.result = "druhý"
        elif "třetí" not in results:
            player.result = "třetí"
        else:
            player.result = "čtvrtý"

        if not last:
            return self.checking_last()

    # vypisování a ukládání výsledků
    def results(self):
        message = ""
        for player in self.players:
            if player.result != "":
                avr = 0
                for num in player.rolls:
                    avr += num
                else:
                    if len(player.rolls) != 0:
                        avr /= len(player.rolls)
                message += player.result + " - " + player.color + " " + str(avr) + " " + str(player.rolls) + "\n"

        message += "\r\n"

        print(message)

        # ukládání výsledků do souboru
        file = open("results.txt", "a+")
        file.write(str(message))
        file.close()

        option = input("\nZmáčkněte enter pro konec, nebo [s] pro obnovení hry a znovunastavení hráčů, nebo [r] pro"
                       " restartování s dosavadním nastavením.\n")
        if option == "s":
            self.restarting()
        elif option == "r":
            self.restarting(True)

    # restartování hry
    def restarting(self, repeat=False):
        self.playing = True
        self.repeating = False

        if repeat:
            self.repeating = True
            player1.playing = True
            player2.playing = True
            if player3.color != "":
                player3.playing = True
            if player4.color != "":
                player4.playing = True

        for player in self.players:
            player.turns = 0
            player.rolls = []
            player.result = ""
            for figure in player.figures:
                figure.tile = figure.home

        return self.main()


app = Game()
app.main()
