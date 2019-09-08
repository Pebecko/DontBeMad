import random
import time
from pathlib import Path
from player import Player
from tile import Tile
from preparation import board_setting
from tactics import tactics
from settings import settings


# TODO - Tactics folder for player to edit tactics (No need to get inside code)
# TODO - Filling rest of player slots as an option
# TODO - Do not allow commands shorter than 4 letters
# TODO - Rewrite base AI
# TODO - Create useful README
# TODO - Make code check for (.csv) files
# TODO - *Make the AI decide using a neural network
# TODO - *Make a version using PyQt5


class Game:
    def __init__(self):
        # rules
        self.no_repeat_when_six = bool  # player will not get a second turn when rolling six
        self.no_moving_while_dep = bool  # player must deploy if he can
        self.random_tactics = bool  # choosing UI tactics randomly
        self.once_three_rolls = bool  # player rolls three times only before he first deploys
        self.no_record = bool  # game will print out only results

        # board setting
        self.possible_players = 4  # maximum number of players playing
        if self.possible_players < 2:
            self.possible_players = 2
        self.start_distance = 10  # distance between start tiles
        if self.start_distance < 10:
            self.start_distance = 10
        self.max_tiles = self.possible_players * self.start_distance

        # game variables
        self.players = []
        self.dice_roll = 0
        self.player_index = 0
        self.playing = True
        self.repeating = False  # repeating game with the same settings
        self.current_fig = None
        self.current_player = Player(0)

    def game_status(self):
        if not self.no_record:
            print("----------------------------------------")
        # player figures info
        for player in self.players:
            if player.playing:
                figs = []
                for figure in player.figures:
                    if figure.tile.finish is False:
                        figs.append(figure.tile.position)
                    else:
                        figs.append(-figure.tile.position)

                # checking if players figures are in the field and printing their positions
                for fig in player.figures:
                    if fig.tile.position != 0:
                        if not self.no_record:
                            settings.translate_slow_print("figures_are_on_tiles",
                                                          (player.number, figs[0], figs[1], figs[2], figs[3]))
                        player.undeployed = False
                        break
                # printing out there are no players figures in the field
                else:
                    player.undeployed = True
                    if not self.no_record:
                        settings.translate_slow_print("player_no_figure", (player.number,))
                self.all_figures_finished_control(player)

    def choosing_playing_player(self):
        if (self.dice_roll != 6 or not self.current_player.playing) and \
                (self.players[0].turns != 0 or not self.players[0].playing):
            self.player_index += 1

        if self.player_index == len(self.players):
            self.player_index = 0

        self.current_player = self.players[self.player_index]

        if not self.current_player.playing:
            return self.choosing_playing_player()

        if not self.no_record:
            print("========================================")
            settings.translate_slow_print("player_is_playing",
                                          (self.current_player.number, self.current_player.color.translation))

    def game_presetting(self):
        if not self.repeating:
            self.possible_players, self.start_distance, self.players, rules = board_setting()
            self.no_repeat_when_six, self.no_moving_while_dep, self.random_tactics, self.once_three_rolls, \
                self.no_record = rules["no_rpt_whl_six"], rules["no_mv_whl_dp"], rules["rnd_tcs"], \
                rules["thr_rls_onl_first"], rules["no_record"]

            self.max_tiles = self.possible_players * self.start_distance
            self.random_ai_tactics_choosing()

            if not self.no_record:
                settings.translate_slow_print("minus_means_home")

        for player in self.players:
            if player.playing:
                for figure in player.figures:
                    figure.start.position = figure.start.position * self.start_distance + 1
                if player.figures[0].start.position > self.max_tiles:
                    player.playing = False

        return

    def main_game_loop(self):
        self.game_presetting()

        # game loop
        while self.playing:
            self.choosing_playing_player()

            self.choosing_number_of_rolls()

            self.game_status()

            # finding out if player should play again
            if self.dice_roll != 6 and not self.no_repeat_when_six:
                self.current_player.turns += 1

            time.sleep(settings.turn_pause)

        # ending game
        settings.translate_slow_print("game_ended")
        return self.results()

    def dice_rolling(self):
        self.dice_roll = random.randint(1, 6)
        self.current_player.rolls.append(self.dice_roll)

        return

    def figure_kicking(self):
        for player in self.players:
            if player.playing:
                for figure in player.figures:
                    if figure.tile.position == self.current_fig.tile.position and \
                            figure.tile.color.name == self.current_fig.tile.color.name and \
                            figure.color.name != self.current_fig.color.name:
                        figure.tile = figure.home
                        if not self.no_record:
                            settings.translate_slow_print("figure_kicked",
                                                          (figure.number, player.number, figure.color.translation))

                        player.own_figures_kicked += 1
                        self.current_player.others_figures_kicked += 1

    def figure_deploying(self):
        self.current_fig.tile = self.current_fig.start
        if not self.no_record:
            settings.translate_slow_print("deploying_figure", (self.current_fig.number,
                                                               self.current_fig.start.position))

        if not self.current_player.has_deployed:
            self.current_player.has_deployed = True

        return self.figure_kicking()

    def figure_repositioning(self):
        self.current_fig.tile = self.finding_figures_new_coordinates(self.current_fig.tile.position,
                                                                     self.current_fig.tile.finishing)
        if not self.no_record:
            settings.translate_slow_print("figure_moved", (self.current_fig.number, self.current_fig.tile.position))
        if self.current_fig.tile.finish and not self.no_record:
            settings.translate_slow_print("figure_at_home")

        return self.figure_kicking()

    def finding_figures_new_coordinates(self, pos, finishing, num=0):
        if num == 0:
            num = self.dice_roll
        new_pos = pos + num

        if new_pos < 1 and num < 1:
            new_pos -= 1

        # going to be deployed
        if pos == 0:
            new_tile = self.current_player.figures[0].start
        # going to one of first six tiles of the board
        elif new_pos == 1 or new_pos == self.max_tiles + 1 or new_pos == -1:
            if (self.current_player.figures[0].start.position + self.max_tiles == new_pos or
                    self.current_player.figures[0].start.position == new_pos) and finishing:
                new_tile = Tile(1, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(1, finishing=False)
        elif new_pos == 2 or new_pos == self.max_tiles + 2 or new_pos == -2:
            if (self.current_player.figures[0].start.position + self.max_tiles + 1 == new_pos or
                    self.current_player.figures[0].start.position + 1 == new_pos) and finishing:
                new_tile = Tile(2, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(2, finishing=False)
        elif new_pos == 3 or new_pos == self.max_tiles + 3 or new_pos == -3:
            if (self.current_player.figures[0].start.position + self.max_tiles + 2 == new_pos or
                    self.current_player.figures[0].start.position + 2 == new_pos) and finishing:
                new_tile = Tile(3, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(3, finishing=False)
        elif new_pos == 4 or new_pos == self.max_tiles + 4 or new_pos == -4:
            if (self.current_player.figures[0].start.position + self.max_tiles + 3 == new_pos or
                    self.current_player.figures[0].start.position + 3 == new_pos) and finishing:
                new_tile = Tile(4, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(4, finishing=False)
        elif new_pos == 5 or new_pos == self.max_tiles + 5 or new_pos == -5:
            new_tile = Tile(5, finishing=True)
        elif new_pos == 6 or new_pos == self.max_tiles + 6 or new_pos == -6:
            new_tile = Tile(6, finishing=True)
        # going to the finish
        elif new_pos % self.start_distance == 1:
            if self.current_player.figures[0].start.position == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % self.start_distance == 2:
            if self.current_player.figures[0].start.position + 1 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % self.start_distance == 3:
            if self.current_player.figures[0].start.position + 2 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        elif new_pos % self.start_distance == 4:
            if self.current_player.figures[0].start.position + 3 == new_pos and finishing:
                new_tile = Tile(new_pos, color=self.current_player.color, finish=True)
            else:
                new_tile = Tile(new_pos, finishing=False)
        # going to a normal tile
        else:
            new_tile = Tile(new_pos)

        return new_tile

    def all_player_figures_home(self):
        # dice rolls for players deploying
        if self.dice_roll == 6 and not self.no_record:
            settings.translate_slow_print("rolled_six")
        elif self.once_three_rolls and self.current_player.has_deployed and not self.no_record:
            settings.translate_slow_print("rolled_st", (self.dice_roll,))
            settings.translate_slow_print("no_moves")
        else:
            if not self.no_record:
                settings.translate_slow_print("rolled_st_more_chances", (self.dice_roll,))
            for j in range(0, 2):
                self.dice_rolling()
                if self.dice_roll == 6:
                    if not self.no_record:
                        settings.translate_slow_print("rolled_six")
                    break
                else:
                    if not self.no_record:
                        settings.translate_slow_print("rolled_st", (self.dice_roll,))
            else:
                return

        # dice roll for players movement after deploying his first figure
        self.dice_rolling()
        self.current_fig = self.current_player.figures[0]
        return self.figure_deploying()

    def figure_blocked_checking(self, new_tile):
        for figure in self.current_player.figures:
            if figure.tile.position == new_tile.position and figure.tile.color.name == new_tile.color.name:
                return True

        return False

    def finding_possible_move(self):
        for figure in self.current_player.figures:
            new_tile = self.finding_figures_new_coordinates(figure.tile.position, figure.tile.finishing)
            figure.movable = False

            if figure.tile.position == 0:
                if self.dice_roll == 6 and not self.figure_blocked_checking(figure.start):
                    figure.movable = True
                    figure.move = "deploy"
                else:
                    figure.move = "undeployable"
            elif not new_tile.finish and figure.tile.finish:
                figure.move = "illegal"
            elif self.finding_figures_new_coordinates(figure.tile.position, figure.tile.finishing, 4).finish and \
                    not new_tile.finish and not figure.tile.finish and (self.dice_roll == 5 or self.dice_roll == 6):
                figure.move = "illegal"
            elif self.figure_blocked_checking(new_tile):
                figure.move = "blocked"
            else:
                if self.dice_roll == 6 and self.no_moving_while_dep:
                    for fig in self.current_player.figures:
                        if fig.tile.home:
                            fig.move = "illegal"
                            break
                    else:
                        figure.movable = True
                        figure.move = "reposition"
                else:
                    figure.movable = True
                    figure.move = "reposition"

        return

    def movement_string_compilation(self):
        self.finding_possible_move()

        # AI choosing move
        if self.current_player.ai:
            self.ai_move_choosing()

        for figure in self.current_player.figures:
            if figure.movable:
                figure.move_mess = ", "
                if figure.move == "deploy":
                    figure.move_mess += settings.translation("deploy")
                else:
                    figure.move_mess += settings.translation("reposition")
                figure.move_mess += settings.translation("figure").format(figure.number)
            else:
                figure.move_mess = ""

    def ai_move_choosing(self):
        for figure in self.current_player.figures:
            # checking if figure can move
            if figure.movable:
                figure.weight = 1

                # figure is in home
                if figure.tile.position == 0:
                    figure.weight += 10 * self.current_player.tactic.deploy

                # figure is in finish
                elif figure.tile.finish:
                    figure.weight *= 0.1

                # figure is in field
                else:
                    # searching for figures distance to the finish
                    target = figure.start.position
                    if figure.tile.position >= target:
                        target += self.max_tiles
                    finnish_distance = target - figure.tile.position
                    if finnish_distance != 0:
                        figure.weight += round(self.current_player.tactic.finnish_distance / finnish_distance * 200, 2)

                    # looking if figure isn't blocking her start tile
                    if figure.tile.position == figure.start.position and \
                            figure.tile.color.name == figure.start.color.name:
                        figure.weight += 10 * self.current_player.tactic.clearing_start

                    # looking if figure isn't standing on others start tiles
                    for pl in self.players:
                        if pl.playing and pl.number != self.current_player.number:
                            if figure.tile.position == pl.figures[0].start.position:
                                figure.weight += 12 * self.current_player.tactic.opponent_start

                # looking if figure can kick other figures with her move
                new_tile = self.finding_figures_new_coordinates(figure.tile.position, figure.tile.finishing)
                for player in self.players:
                    if player.playing:
                        for fig in player.figures:
                            if new_tile.color.name == fig.tile.color.name and new_tile.position == fig.tile.position:
                                figure.weight += 10 * self.current_player.tactic.kicking_out

                # looking if figure can be kicked
                if not figure.tile.finish:
                    for pos in range(1, 7):
                        tile_behind = self.finding_figures_new_coordinates(figure.tile.position, False, -pos)
                        for player in self.players:
                            if player.playing and player.number != self.current_player.number:
                                for fig in player.figures:
                                    if fig.tile.position == tile_behind.position and \
                                            fig.tile.color.name == tile_behind.color.name:
                                        figure.weight += pos * 5 * self.current_player.tactic.running_away

                if figure.weight <= 0:
                    figure.weight = 0.01

            else:
                figure.weight = 0

            # debug
            # print(figure.weight)

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
            self.figure_deploying()
        elif self.current_fig.move == "reposition":
            self.figure_repositioning()
        else:
            self.current_player.inactive_turns += 1

        return

    def player_move_choosing(self):
        self.movement_string_compilation()

        while (self.current_player.figures[0].move_mess != "" or self.current_player.figures[1].move_mess != "" or
               self.current_player.figures[2].move_mess != "" or self.current_player.figures[3].move_mess != "") and \
                self.current_player.ai is False:
            self.movement_string_compilation()

            settings.translate_slow_print("rolled_st", (self.dice_roll,))
            player_option = settings.base_options("moving_figure_choosing", (self.current_player.figures[0].move_mess,
                                                                             self.current_player.figures[1].move_mess,
                                                                             self.current_player.figures[2].move_mess,
                                                                             self.current_player.figures[3].move_mess))
            # first figure
            if player_option == "1" and self.current_player.figures[0].move_mess != "":
                self.current_fig = self.current_player.figures[0]
                break
            # second figure
            elif player_option == "2" and self.current_player.figures[1].move_mess != "":
                self.current_fig = self.current_player.figures[1]
                break
            # third figure
            elif player_option == "3" and self.current_player.figures[2].move_mess != "":
                self.current_fig = self.current_player.figures[2]
                break
            # fourth figure
            elif player_option == "4" and self.current_player.figures[3].move_mess != "":
                self.current_fig = self.current_player.figures[3]
                break
            # player changing settings
            elif player_option != "skip":
                settings.translate_slow_print("input_error")
        # no figures can move
        else:
            if not self.current_player.undeployed and not self.no_record:
                settings.translate_slow_print("rolled_st", (self.dice_roll,))
            if not self.current_player.ai:
                settings.translate_slow_print("no_moves")
                self.current_player.inactive_turns += 1
            return

        # deploying selected figure
        if self.current_fig.tile.position == 0:
            self.figure_deploying()
        # repositioning selected figure
        else:
            self.figure_repositioning()

        return

    def choosing_number_of_rolls(self):
        self.dice_rolling()

        # player has no figures in the field or in finish
        if self.current_player.undeployed:
            self.all_player_figures_home()

        return self.player_move_choosing()

    def all_figures_finished_control(self, player):
        for figure in player.figures:
            if figure.tile.finish is not True:
                return
        # all figures are in the finish
        else:
            self.setting_player_placing(player)

    def checking_for_last_player(self):
        num = 0
        player = None
        for pl in self.players:
            if pl.playing:
                num += 1
                player = pl

        # last player in game
        if num == 1:
            self.playing = False
            return self.setting_player_placing(player, True)

    def setting_player_placing(self, player, last=False):
        player.playing = False
        results = []
        for pl in self.players:
            results.append(pl.result)
        for i in range(1, len(self.players) + 1):
            if i not in results:
                player.result = i
                break

        if not last:
            return self.checking_for_last_player()

    def results(self):
        # printing results to the player
        message = ""
        for player in self.players:
            if player.result != 0:
                avr = 0
                for num in player.rolls:
                    avr += num
                else:
                    if len(player.rolls) != 0:
                        avr /= len(player.rolls)
                message += settings.translation("player_placing").format(player.figures[0].color.translation,
                                                                         player.result)
                message += " - " + str(round(avr, 4)) + " " + str(player.rolls) + " " + str(player.turns) + " " + \
                           str(player.inactive_turns) + " " + str(player.others_figures_kicked) + " " + \
                           str(player.own_figures_kicked) + "\n"
                if player.ai:
                    message += settings.translation("his_tactic").format(player.tactic.name, "\r\n")

        message += "\r\n"

        print(message)

        # saving results to results.txt in data folder
        file = open(Path(__file__).parent.parent / "data/results.txt", "a+")
        file.write(str(message))
        file.close()

        while True:
            option = settings.base_options("end_message")
            if option == "s":
                return self.restarting()
            elif option == "r":
                return self.restarting(True)
            elif option != "skip":
                exit()

    def restarting(self, repeat=False):
        # resetting game variables
        self.playing = True
        self.repeating = False
        self.player_index = 0

        # resetting player variables
        for player in self.players:
            player.playing = False
            if player.result != 0:
                if repeat:
                    self.repeating = True
                    player.playing = True
                player.turns = 0
                player.rolls = []
                player.result = 0
                for figure in player.figures:
                    figure.tile = figure.home
                    figure.start.position = int((figure.start.position - 1) / self.start_distance)

        return self.main_game_loop()

    def random_ai_tactics_choosing(self):
        if self.random_tactics:
            for player in self.players:
                player.tactic = random.choice(tactics)

        return


app = Game()
app.main_game_loop()
