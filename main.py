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


class Game:
    def __init__(self):
        self.wait_time = 0  # čas, který hra čeká po každém tahu
        self.dice_roll = 0
        self.playing = True
        self.repeating = False  # pokud má hra opakovat vše se stejným nastavením

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

    # všechny figurky v domečku => 3 šance na nasazení
    def all_home(self):
        if self.dice_roll == 6:
            print("Padla vám 6.")
        else:
            print("Padla vám " + str(self.dice_roll) + ", nemůžete nasadit ale máte ještě dvě šance.")
            for i in range(0, 2):
                self.dice_roll = random.randint(1, 6)
                self.current_player.rolls.append(self.dice_roll)
                if self.dice_roll == 6:
                    print("Padla vám 6.")
                    break
                else:
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
                figure.movable = True
                figure.move = "reposition"

        return

    # skládání zprávy pro hráče o možných pohybech
    def string_compilation(self):
        self.possible_move()

        # vybírání tahu AI
        if self.current_player.ai:
            self.ai_move_choosing()

        mov1, mov2, mov3, mov4 = "", "", "", ""

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
        avr_1, avr_2, avr_3, avr_4 = 0, 0, 0, 0
        for num in player1.rolls:
            avr_1 += num
        else:
            if len(player1.rolls) != 0:
                avr_1 /= len(player1.rolls)

        for num in player2.rolls:
            avr_2 += num
        else:
            if len(player2.rolls) != 0:
                avr_2 /= len(player2.rolls)

        for num in player3.rolls:
            avr_3 += num
        else:
            if len(player3.rolls) != 0:
                avr_3 /= len(player3.rolls)

        for num in player4.rolls:
            avr_4 += num
        else:
            if len(player4.rolls) != 0:
                avr_4 /= len(player4.rolls)

        result = "{} - {} {} {}\n{} - {} {} {}\n{} - {} {} {}\n{} - {} {} {}" \
                 "\r\n".format(player1.result, player1.color, avr_1, player1.rolls,
                               player2.result, player2.color, avr_2, player2.rolls,
                               player3.result, player3.color, avr_3, player3.rolls,
                               player4.result, player4.color, avr_4, player4.rolls)

        print(result)

        # ukládání výsledků do souboru
        f = open("results.txt", "a+")
        f.write(str(result))
        f.close()

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

        player1.turns = 0
        player2.turns = 0
        player3.turns = 0
        player4.turns = 0

        player1.rolls = []
        player2.rolls = []
        player3.rolls = []
        player4.rolls = []

        player1.result = ""
        player2.result = ""
        player3.result = ""
        player4.result = ""

        red_fig1.tile = tile.home_red
        red_fig2.tile = tile.home_red
        red_fig3.tile = tile.home_red
        red_fig4.tile = tile.home_red
        blue_fig1.tile = tile.home_blue
        blue_fig2.tile = tile.home_blue
        blue_fig3.tile = tile.home_blue
        blue_fig4.tile = tile.home_blue
        green_fig1 .tile = tile.home_green
        green_fig2 .tile = tile.home_green
        green_fig3 .tile = tile.home_green
        green_fig4 .tile = tile.home_green
        yellow_fig1.tile = tile.home_yellow
        yellow_fig2.tile = tile.home_yellow
        yellow_fig3.tile = tile.home_yellow
        yellow_fig4.tile = tile.home_yellow

        return self.main()


app = Game()
app.main()
