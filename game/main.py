from random import choice
from time import sleep
from pathlib import Path
from player import Player
from tile import Tile
from dice import Dice
from preparation import Preparation
from tactics import tactics
from settings import settings


# TODO - Changing possible number of figures and upgrade changing distance between start tiles
# TODO - Add new stats to the results (size of the board, number of figures,...)
# TODO - Tactics folder for player to edit tactics (No need to get inside code)
# TODO - Filling rest of undecided player slots as an option
# TODO - Do not allow commands shorter than 4 letters
# TODO - Rewrite base AI
# TODO - Create useful README
# TODO - Make code check for existence of (.csv) files
# TODO - *Make the AI decide using a neural network
# TODO - *Make a version using PyQt5


class Game:
    def __init__(self):
        self.finish_marking_character = "-"
        self.rules = {}

        # board setting
        self.max_number_of_players = 2  # maximum number of players playing
        self.distance_between_starts = 10  # distance between start tiles
        self.max_tiles = 20

        # game variables
        self.players = []
        self.dice = Dice()
        self.player_index = 0
        self.playing = True
        self.repeating = False  # repeating game with the same settings
        self.current_fig = None
        self.current_player = Player(0)

    def main(self):
        self.game_presetting()

        self.game_loop()

        # ending game
        settings.translate_slow_print("game_ended")
        return self.results()

    # game preparation
    def game_presetting(self):
        if not self.repeating:
            self.getting_variables_from_preparation()
            self.setting_variables_from_preparation()

            settings.translate_slow_print("character_means_home", (self.finish_marking_character,),
                                          no_record=self.rules["no_record"])

        self.presetting_players_and_figures()

        return

    def getting_variables_from_preparation(self):
        self.max_number_of_players, self.distance_between_starts, self.players, self.rules, \
            self.dice = Preparation().main()

    def setting_variables_from_preparation(self):
        self.max_tiles = self.max_number_of_players * self.distance_between_starts
        if self.rules["rnd_tcs"]:
            self.random_ai_tactics_choosing()

    def random_ai_tactics_choosing(self):
        for player in self.players:
            player.tactic = choice(tactics)

        return

    def presetting_players_and_figures(self):
        for player in self.players:
            if player.playing:
                for figure in player.figures:
                    figure.start.position = figure.start.position * self.distance_between_starts + 1
                if player.figures[0].start.position > self.max_tiles:
                    player.playing = False

    # main game
    def game_loop(self):
        while self.playing:
            self.choosing_playing_player()

            self.choosing_number_of_rolls()

            self.game_status()

            self.finding_if_player_should_move_again()

            sleep(settings.turn_pause)

    def choosing_playing_player(self):
        self.changing_player_index()

        self.current_player = self.players[self.player_index]

        # skipping inactive players
        if not self.current_player.playing:
            return self.choosing_playing_player()

        if not self.rules["no_record"]:
            self.outputting_choosing_playing_player_message()

        return

    def changing_player_index(self):
        if (self.dice.dice_roll < self.dice.min_deploy_roll or not self.current_player.playing) and \
                (self.players[0].turns != 0 or not self.players[0].playing):
            self.player_index += 1

        self.checking_for_player_index_overflowing()

    def checking_for_player_index_overflowing(self):
        if self.player_index == len(self.players):
            self.player_index = 0

    def outputting_choosing_playing_player_message(self):
        print("========================================")
        settings.translate_slow_print("player_is_playing",
                                      (self.current_player.number, self.current_player.color.translation))

    def choosing_number_of_rolls(self):
        self.dice.dice_rolling(self.current_player)

        # player has no figures in the field or in finish
        if self.current_player.undeployed:
            self.all_player_figures_home()

        if self.current_player.ai:
            return self.ai_moving()
        else:
            return self.player_moving()

    def all_player_figures_home(self):
        # player can deploy instantly
        if self.dice.dice_roll >= self.dice.min_deploy_roll:
            settings.translate_slow_print("rolled_st", (self.dice.dice_roll,), no_record=self.rules["no_record"])

        # player has no more rolls in this turn thanks to rules
        elif self.rules["thr_rls_onl_first"] and self.current_player.has_deployed:
            settings.translate_slow_print("rolled_st", (self.dice.dice_roll,), no_record=self.rules["no_record"])
            settings.translate_slow_print("no_moves", no_record=self.rules["no_record"])

        # player has two more rolls
        else:
            self.player_rolling_two_more_times()

    def player_rolling_two_more_times(self):
        settings.translate_slow_print("rolled_st_more_chances", (self.dice.dice_roll,),
                                      no_record=self.rules["no_record"])
        for j in range(0, 2):
            self.dice.dice_rolling(self.current_player)
            if self.dice.dice_roll >= self.dice.min_deploy_roll:
                settings.translate_slow_print("rolled_st", (self.dice.dice_roll,), no_record=self.rules["no_record"])
                return self.deploying_first_figure_in_three_rolls()
            else:
                settings.translate_slow_print("rolled_st", (self.dice.dice_roll,),
                                              no_record=self.rules["no_record"])

        return

    def deploying_first_figure_in_three_rolls(self):
        self.dice.dice_rolling(self.current_player)
        self.current_fig = self.current_player.figures[0]
        return self.figure_deploying()

    def player_moving(self):
        self.movement_string_compilation()

        exists_movable_figure = self.finding_if_exists_movable_figure()

        while exists_movable_figure:
            return self.player_choosing_move()

        # no figures can move
        else:
            return self.player_has_no_moves()

    def player_choosing_move(self):
        settings.translate_slow_print("rolled_st", (self.dice.dice_roll,))

        player_option = settings.base_options(self.compiling_movement_message(), translate=False)

        for figure in self.current_player.figures:
            if player_option == str(figure.number) and figure.movable:
                self.current_fig = figure
                return self.choosing_how_should_figure_move()

        self.checking_if_player_changed_settings(player_option)

    def movement_string_compilation(self):
        self.finding_possible_move()

        for figure in self.current_player.figures:
            if figure.movable and not self.rules["no_record"]:
                self.compiling_movement_string_if_figure_movable(figure)
            else:
                figure.move_mess = ""

        return

    def finding_possible_move(self):
        for figure in self.current_player.figures:
            new_tile = self.finding_figures_new_coordinates(figure.tile.position, figure.tile.finishing)
            figure.movable = False

            if figure.tile.position == 0:
                self.finding_move_if_figure_at_home(figure)
            elif not new_tile.finish and figure.tile.finish:
                figure.move = "illegal"
            elif self.figure_blocked_checking(new_tile):
                figure.move = "blocked"
            elif not new_tile.finish and self.dice.dice_roll > self.finding_minimal_roll_to_get_to_finish(figure):
                figure.move = "illegal"
            else:
                self.finding_move_if_figure_in_field(figure)

        return

    def finding_move_if_figure_at_home(self, figure):
        if self.dice.dice_roll >= self.dice.min_deploy_roll and not self.figure_blocked_checking(figure.start):
            figure.movable, figure.move = True, "deploy"
        else:
            figure.move = "undeployable"

    def figure_blocked_checking(self, new_tile):
        for figure in self.current_player.figures:
            if figure.tile.position == new_tile.position and figure.tile.color.name == new_tile.color.name:
                return True

        return False

    def finding_minimal_roll_to_get_to_finish(self, figure):
        if figure.start.position > figure.tile.position:
            return figure.start.position - figure.tile.position
        else:
            return figure.start.position + self.max_tiles - figure.tile.position

    def finding_move_if_figure_in_field(self, figure):
        # player can only move if he has no figures at home due to rules
        if self.dice.dice_roll >= self.dice.min_deploy_roll and self.rules["no_mv_whl_dp"]:
            if self.finding_if_player_has_figures_at_home():
                figure.move = "illegal"
            else:
                figure.movable, figure.move = True, "reposition"
        # player can normally move
        else:
            figure.movable, figure.move = True, "reposition"

    def finding_if_player_has_figures_at_home(self):
        for figure in self.current_player.figures:
            if figure.tile.home:
                return True
        else:
            return False

    @staticmethod
    def compiling_movement_string_if_figure_movable(figure):
        figure.move_mess = ", "
        if figure.move == "deploy":
            figure.move_mess += settings.translation("deploy")
        else:
            figure.move_mess += settings.translation("reposition")
        figure.move_mess += settings.translation("figure").format(figure.number)

        return

    def finding_if_exists_movable_figure(self):
        for figure in self.current_player.figures:
            if figure.movable:
                return True
        else:
            return False

    def compiling_movement_message(self):
        message = settings.translation("moving_figure_choosing")

        for figure in self.current_player.figures:
            if figure.movable:
                message += figure.move_mess

        return message

    def checking_if_player_changed_settings(self, player_option):
        if player_option != "skip":
            settings.translate_slow_print("input_error")
        else:
            self.movement_string_compilation()

        return

    def player_has_no_moves(self):
        if not self.current_player.undeployed:
            settings.translate_slow_print("rolled_st", (self.dice.dice_roll,), no_record=self.rules["no_record"])

        settings.translate_slow_print("no_moves")
        self.current_player.inactive_turns += 1

        return

    def ai_moving(self):
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

    def choosing_how_should_figure_move(self):
        # deploying selected figure
        if self.current_fig.tile.position == 0:
            self.figure_deploying()
        # repositioning selected figure
        else:
            self.figure_repositioning()

    def figure_deploying(self):
        self.current_fig.tile = self.current_fig.start
        settings.translate_slow_print("deploying_figure", (self.current_fig.number, self.current_fig.start.position),
                                      no_record=self.rules["no_record"])

        if not self.current_player.has_deployed:
            self.current_player.has_deployed = True

        return self.figure_kicking()

    def figure_repositioning(self):
        self.current_fig.tile = self.finding_figures_new_coordinates(self.current_fig.tile.position,
                                                                     self.current_fig.tile.finishing)
        settings.translate_slow_print("figure_moved", (self.current_fig.number, self.current_fig.tile.position),
                                      no_record=self.rules["no_record"])
        if self.current_fig.tile.finish:
            settings.translate_slow_print("figure_at_home", no_record=self.rules["no_record"])

        return self.figure_kicking()

    def finding_figures_new_coordinates(self, current_position, finishing, num=0):
        new_position = self.finding_new_position_value(current_position, num)

        if current_position == 0:
            return self.current_player.figures[0].start
        elif self.current_player.figures[0].start.position <= new_position <= \
                self.current_player.figures[0].start.position + len(self.current_player.figures) - 1:
            if finishing:
                return Tile(new_position, color=self.current_player.color, finish=True)
            elif abs(new_position % self.distance_between_starts) == len(self.current_player.figures):
                return Tile(new_position)
            else:
                return Tile(new_position, finishing=False)
        else:
            return Tile(new_position)

    def finding_new_position_value(self, current_position, num):
        if num == 0:
            num = self.dice.dice_roll
        new_position = current_position + num

        if new_position < 1 and num < 1:
            new_position += self.max_tiles

        if new_position > self.max_tiles:
            new_position -= self.max_tiles

        return new_position

    def figure_kicking(self):
        for player in self.players:
            if player.playing and player.color.name != self.current_player.color.name:
                for figure in player.figures:
                    if figure.tile.position == self.current_fig.tile.position and \
                            figure.tile.color.name == self.current_fig.tile.color.name and \
                            figure.color.name != self.current_fig.color.name:
                        figure.tile = figure.home
                        settings.translate_slow_print("figure_kicked",
                                                      (figure.number, player.number, figure.color.translation),
                                                      no_record=self.rules["no_record"])

                        player.own_figures_kicked += 1
                        self.current_player.others_figures_kicked += 1

    def game_status(self):
        if not self.rules["no_record"]:
            print("----------------------------------------")

        for player in self.players:
            if player.playing:
                self.finding_player_status(player)

        return

    def finding_player_status(self, player):
        message = self.setting_status_message()
        figure_not_in_finish = False
        figures_on_board = False

        for figure in player.figures:
            message = self.updating_status_message(figure, message)
            if not figure.tile.finish and not figure_not_in_finish:
                figure_not_in_finish = True
            if figure.tile.position != 0 and not figures_on_board:
                figures_on_board = True

        if not figure_not_in_finish:
            return self.setting_player_placing(player)

        if figures_on_board:
            self.player_has_figures_on_board(player, message)
        else:
            self.player_has_all_figures_at_home(player)

    def setting_status_message(self):
        if not self.rules["no_record"]:
            message = settings.translation("figures_are_on_tiles")
        else:
            message = ""

        return message

    def updating_status_message(self, figure, message):
        if not self.rules["no_record"]:
            if figure.tile.finish is False:
                message += " {};".format(figure.tile.position)
            else:
                message += " {}{}{};".format(self.finish_marking_character, figure.tile.position,
                                             self.finish_marking_character)
        return message

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

        return

    def checking_for_last_player(self):
        number_of_playing_players = 0
        last_playing_player = None

        for player in self.players:
            if player.playing:
                number_of_playing_players += 1
                last_playing_player = player

        # last player in game
        if number_of_playing_players == 1:
            self.playing = False
            return self.setting_player_placing(last_playing_player, True)

        return

    def player_has_figures_on_board(self, player, message):
        player.undeployed = False

        if not self.rules["no_record"]:
            message = message[:-1]
            settings.slow_print(message.format(player.number, player.color.translation))

    def player_has_all_figures_at_home(self, player):
        player.undeployed = True
        if not self.rules["no_record"]:
            settings.translate_slow_print("player_no_figure", (player.number, player.color.translation))

    def finding_if_player_should_move_again(self):
        if self.dice.dice_roll < self.dice.min_deploy_roll and not self.rules["no_rpt_whl_six"]:
            self.current_player.turns += 1

    # end of the game
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
                    figure.start.position = int((figure.start.position - 1) / self.distance_between_starts)

        return self.main()


app = Game()
app.main()
