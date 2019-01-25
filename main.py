import random
import time
from player import player1, player2, player3, player4, player5, player6, Player
from tile import Tile
from figures import black_figures, orange_figures
from preparation import player_number
from tactics import move_nearest, kicker, deployer, running_away


# TODO - Sumarizace výsledků do speciální složky - avarage_results.txt


# nastavení UI
player1.ai = True
player2.ai = True
player3.ai = True
player4.ai = True
player5.ai = True
player6.ai = True

player1.tactic = move_nearest
player2.tactic = running_away
player3.tactic = kicker
player4.tactic = deployer

# prozatimní nastavení
player5.playing = False
player6.playing = False

player5.color = "black"
player6.color = "orange"

player5.figures = black_figures
player6.figures = orange_figures


class Game:
    def __init__(self):
        self.no_moving_while_dep = False  # pravidlo pro posouvání figurek když můžete nasadit

        self.wait_time = 0  # čas, který hra čeká po každém tahu
        self.dice_roll = 0
        self.player_index = 0
        self.playing = True
        self.repeating = False  # pokud má hra opakovat vše se stejným nastavením

        # board setting
        self.possible_players = 4
        if self.possible_players < 2:
            self.possible_players = 2
        self.start_distance = 10
        if self.start_distance < 10:
            self.start_distance = 10
        self.max_tiles = self.possible_players * self.start_distance

        self.current_fig = None

        self.players = [player1, player2, player3, player4, player5, player6]
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
        if (self.dice_roll != 6 or not self.current_player.playing) and player1.turns != 0:
            self.player_index += 1

        if self.player_index == len(self.players):
            self.player_index = 0

        self.current_player = self.players[self.player_index]

        if not self.current_player.playing:
            return self.side_selection()

        print("========================================")
        print("Hraje hráč {}. - {}".format(self.current_player.number, self.current_player.color))

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
            if player.playing:
                for figure in player.figures:
                    if figure.tile.position == self.current_fig.tile.position and \
                            figure.tile.color == self.current_fig.tile.color and figure.color != self.current_fig.color:
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
        self.current_fig.tile = self.new_coordinates(self.current_fig.tile.position, self.current_fig.tile.finishing)
        print("Figurka {} se posunula na políčko {}.".format(self.current_fig.number, self.current_fig.tile.position))
        if self.current_fig.tile.finish:
            print("Figurka je v domečku.")

        return self.figure_kicking()

    # zjišťování nové pozice
    def new_coordinates(self, pos, finishing, num=0):
        if num == 0:
            num = self.dice_roll
        new_pos = pos + num

        if new_pos < 1 and num < 1:
            new_pos -= 1

        if pos == 0:
            new_tile = self.current_player.figures[0].start
        elif new_pos == 1 or new_pos == self.max_tiles + 1 or new_pos == -1:
            if self.current_player.figures[0].start.position + self.max_tiles == new_pos and finishing:
                new_tile = Tile(1, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(1, finishing=False)
        elif new_pos == 2 or new_pos == self.max_tiles + 2 or new_pos == -2:
            if self.current_player.figures[0].start.position + self.max_tiles + 1 == new_pos and finishing:
                new_tile = Tile(2, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(2, finishing=False)
        elif new_pos == 3 or new_pos == self.max_tiles + 3 or new_pos == -3:
            if self.current_player.figures[0].start.position + self.max_tiles + 2 == new_pos and finishing:
                new_tile = Tile(3, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(3, finishing=False)
        elif new_pos == 4 or new_pos == self.max_tiles + 4 or new_pos == -4:
            if self.current_player.figures[0].start.position + self.max_tiles + 3 == new_pos and finishing:
                new_tile = Tile(4, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(4, finishing=False)
        elif new_pos == 5 or new_pos == self.max_tiles + 5 or new_pos == -5:
            new_tile = Tile(5, finishing=True)
        elif new_pos == 6 or new_pos == self.max_tiles + 6 or new_pos == -6:
            new_tile = Tile(6, finishing=True)
        elif new_pos % 10 == 1:
            if self.current_player.figures[0].start.position == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % 10 == 2:
            if self.current_player.figures[0].start.position + 1 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % 10 == 3:
            if self.current_player.figures[0].start.position + 2 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % 10 == 4:
            if self.current_player.figures[0].start.position + 3 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
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
            new_tile = self.new_coordinates(figure.tile.position, figure.tile.finishing)
            figure.movable = False

            if figure.tile.position == 0:
                if self.dice_roll == 6 and not self.block_checking(figure.start):
                    figure.movable = True
                    figure.move = "deploy"
                else:
                    figure.move = "undeployable"
            elif not new_tile.finish and figure.tile.finish:
                figure.move = "illegal"
            elif self.new_coordinates(figure.tile.position, figure.tile.finishing, 4).finish and (
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

        for figure in self.current_player.figures:
            if figure.movable:
                figure.move_mess = ", "
                if figure.move == "deploy":
                    figure.move_mess += "nasadit"
                else:
                    figure.move_mess += "poposunout"
                figure.move_mess += " figurku [{}]".format(figure.number)
            else:
                figure.move_mess = ""

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
                        target += self.max_tiles
                    finnish_distance = target - figure.tile.position
                    if finnish_distance != 0:
                        figure.weight += round(self.current_player.tactic.finnish_distance / finnish_distance * 200, 2)

                    # zjišťování zda figurka neblokuje své startovací políčko
                    if figure.tile.position == figure.start.position and figure.tile.color == figure.start.color:
                        figure.weight += 10 * self.current_player.tactic.clearing_start

                    # zjišťování, zda figurka nestojí na startovním políčku jiného hrajícího hráče
                    for pl in self.players:
                        if pl.playing and pl.number != self.current_player.number:
                            if figure.tile.position == pl.figures[0].start.position:
                                figure.weight += 12 * self.current_player.tactic.opponent_start

                # zjišťování zda figurka nemůže vyhodit jinou figurku svým tahem
                new_tile = self.new_coordinates(figure.tile.position, figure.tile.finishing)
                for player in self.players:
                    if player.playing:
                        for fig in player.figures:
                            if new_tile.color == fig.tile.color and new_tile.position == fig.tile.position:
                                figure.weight += 10 * self.current_player.tactic.kicking_out

                # zjišťování jestli figurka nemůže být vyhozena, když zůstane stát
                if not figure.tile.finish:
                    for pos in range(1, 7):
                        tile_behind = self.new_coordinates(figure.tile.position, False, -pos)
                        for player in self.players:
                            if player.playing and player.number != self.current_player.number:
                                for fig in player.figures:
                                    if fig.tile.position == tile_behind.position and \
                                            fig.tile.color == tile_behind.color:
                                        figure.weight += pos * 5 * self.current_player.tactic.running_away

                if figure.weight <= 0:
                    figure.weight = 0.01

            else:
                figure.weight = 0

            # debug
            print(figure.weight)

        if self.current_player.figures[0].weight >= self.current_player.figures[1].weight and \
                self.current_player.figures[0].weight >= self.current_player.figures[2].weight and \
                self.current_player.figures[0].weight >= self.current_player.figures[3].weight:
            self.current_fig = self.current_player.figures[0]
        elif self.current_player.figures[1].weight >= self.current_player.figures[0].weight and \
                self.current_player.figures[1].weight >= self.current_player.figures[2].weight and \
                self.current_player.figures[1].weight >= self.current_player.figures[3].weight:
            self.current_fig = self.current_player.figures[1]
        elif self.current_player.figures[2].weight >= self.current_player.figures[0].weight and \
                self.current_player.figures[2].weight >= self.current_player.figures[1].weight and \
                self.current_player.figures[2].weight >= self.current_player.figures[3].weight:
            self.current_fig = self.current_player.figures[2]
        else:
            self.current_fig = self.current_player.figures[3]

        if self.current_fig.move == "deploy":
            self.deploying()
        elif self.current_fig.move == "reposition":
            self.repositioning()

        return

    # hráč si vybírá, jaký tah zahraje
    def move_choosing(self):
        self.string_compilation()

        while (self.current_player.figures[0].move_mess != "" or self.current_player.figures[1].move_mess != "" or
               self.current_player.figures[2].move_mess != "" or self.current_player.figures[3].move_mess != "") and \
                self.current_player.ai is False:
            print("Padla vám {}.".format(self.dice_roll))
            player_option = input("Můžete{}{}{}{}\n".format(self.current_player.figures[0].move_mess,
                                                            self.current_player.figures[1].move_mess,
                                                            self.current_player.figures[2].move_mess,
                                                            self.current_player.figures[3].move_mess))
            if player_option == "1" and self.current_player.figures[0].move_mess != "":
                self.current_fig = self.current_player.figures[0]
                break
            elif player_option == "2" and self.current_player.figures[1].move_mess != "":
                self.current_fig = self.current_player.figures[1]
                break
            elif player_option == "3" and self.current_player.figures[2].move_mess != "":
                self.current_fig = self.current_player.figures[2]
                break
            elif player_option == "4" and self.current_player.figures[3].move_mess != "":
                self.current_fig = self.current_player.figures[3]
                break
            else:
                print("Zadaná možnost nesouhlasí s možnostmi.\n")
        else:
            if not self.current_player.undeployed:
                print("Padla vám {}.".format(self.dice_roll))
            print("Nemáte žádné tahy na výběr.\n")
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
        elif "čtvrtý" not in results:
            player.result = "čtvrtý"
        elif "pátý" not in results:
            player.result = "pátý"
        else:
            player.result = "šestý"

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
                message += player.result + " - " + player.color + " " + str(round(avr, 4)) + " " + \
                    str(player.rolls) + "\n"

        message += "\r\n"

        print(message)

        # ukládání výsledků do textového souboru
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
        self.player_index = 0

        for player in self.players:
            if player.result != "":
                if repeat:
                    self.repeating = True
                    player.playing = True
                player.turns = 0
                player.rolls = []
                player.result = ""
                for figure in player.figures:
                    figure.tile = figure.home

        return self.main()


app = Game()
app.main()
