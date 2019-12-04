from player import Player
from figures import Figure
from dice import Dice
from tile import Tile
from settings import settings


class Preparation:
    def __init__(self):
        self.dice = Dice()

        # figures data
        self.number_of_figures = 1
        self.figures = []

        # players data
        self.max_number_of_players = 2
        self.players = []

        # board data
        self.minimal_distance_between_starts = 1
        self.distance_between_starts = 1

        # rules
        self.rules = {}

    def main(self):
        self.choosing_maximal_roll()

        self.choosing_minimal_roll()

        self.choosing_min_deploy_roll()

        self.choosing_number_of_figures()

        self.choosing_max_number_of_players()

        self.start_distance_setting()

        self.player_color_deciding()

        self.removing_redundant_players()

        self.rules_setting()

        self.ai_setting()

        return self.max_number_of_players, self.distance_between_starts, self.players, self.rules, self.dice

    @staticmethod
    def choosing_int_value(player_option, minimal_value, maximal_value=float("inf")):
        try:
            int(player_option)
        except ValueError:
            if player_option != "skip":
                settings.translate_slow_print("input_error")
        else:
            if minimal_value <= int(player_option) <= maximal_value:
                return int(player_option)
            else:
                settings.translate_slow_print("input_error")
                return None

    @staticmethod
    def choosing_rule(rule_mess="", rule_ans_1="", rule_ans_2=""):
        while True:
            player_option = settings.base_options(rule_mess)
            if player_option == settings.translation(rule_ans_1):
                return True
            elif player_option == settings.translation(rule_ans_2):
                return False
            elif player_option != "skip":
                settings.translate_slow_print("input_error")

    def choosing_maximal_roll(self):
        while True:
            player_option = settings.base_options("how_big_maximal_roll")

            response = self.choosing_int_value(player_option, 1)
            if response is not None:
                self.dice.maximal_roll = response
                return

    def choosing_minimal_roll(self):
        while True:
            player_option = settings.base_options("how_big_minimal_roll", (self.dice.maximal_roll,))

            response = self.choosing_int_value(player_option, 1, self.dice.maximal_roll)
            if response is not None:
                self.dice.minimal_roll = response
                return

    def choosing_min_deploy_roll(self):
        # skipping player choosing if there is only one possibility
        if self.dice.minimal_roll == self.dice.maximal_roll:
            self.dice.min_deploy_roll = self.dice.minimal_roll
            return

        # player choosing
        while True:
            player_option = settings.base_options("how_big_min_deploy_roll",
                                                  (self.dice.minimal_roll, self.dice.maximal_roll))

            response = self.choosing_int_value(player_option, self.dice.minimal_roll, self.dice.maximal_roll)
            if response is not None:
                self.dice.min_deploy_roll = response
                return

    def choosing_number_of_figures(self):
        while True:
            player_option = settings.base_options("how_many_figures")

            response = self.choosing_int_value(player_option, 1)
            if response is not None:
                self.number_of_figures = response
                return self.defining_figures()

    def defining_figures(self):
        settings.translating_colors()

        figures = [[] for x in range(0, len(settings.color_names))]

        for i in range(0, len(settings.color_names)):
            for j in range(1, self.number_of_figures + 1):
                figures[i].append(Figure(j, Tile(0, color=settings.color_names[i], home=True, finishing=False),
                                         Tile(i, finishing=False), settings.color_names[i]))

        self.figures = figures

    def choosing_max_number_of_players(self):
        while True:
            # string formatting
            if len(self.figures) >= 2:
                message = settings.translation("how_big_board")
                for player_number in range(2, len(self.figures) + 1):
                    if player_number == 2:
                        message += "[{}]".format(player_number)
                        if len(self.figures) == 2:
                            message += settings.translation("two_players").format(player_number)
                    elif player_number == len(self.figures) and len(self.figures) >= 5:
                        message += settings.translation("or_players_greater_five").format(player_number)
                    elif player_number == len(self.figures):
                        message += settings.translation("or_players_less_five").format(player_number)
                    else:
                        message += ", [{}]".format(player_number)
            else:
                message = settings.translation("not_enough_colors_error")

            # players response
            player_option = settings.base_options(message, translate=False)

            response = self.choosing_int_value(player_option, 2, len(self.figures))

            if response is not None:
                self.max_number_of_players = response
                return self.defining_players()

    def defining_players(self):
        players = []
        for i in range(len(self.figures)):
            players.append(Player(i + 1))

        self.players = players

    def counting_minimal_distance_between_starts(self):
        # rounding up the value using negative numbers
        self.minimal_distance_between_starts = \
            -(-(self.number_of_figures + self.dice.maximal_roll - 1) // self.max_number_of_players)

    def start_distance_setting(self):
        self.counting_minimal_distance_between_starts()

        while True:
            player_option = settings.base_options("which_distance_between_starts",
                                                  (self.minimal_distance_between_starts,))

            response = self.choosing_int_value(player_option, self.minimal_distance_between_starts)
            if response is not None:
                self.distance_between_starts = response
                return

    def player_color_deciding(self):
        for num in range(0, self.max_number_of_players):
            # no need for player to choose color of last player if there is only one to choose from
            if num == len(self.players) and len(self.figures) == 1:
                self.players[-1].playing = True
                for figure in self.figures[0]:
                    figure.start.position = len(self.players) - 1
                self.players[-1].self.figures = self.figures[0]
                self.players[-1].color = self.figures[0][0].color
                break

            # finding if player must be chosen
            playing_pl = 0
            for player in self.players:
                if player.playing:
                    playing_pl += 1

            must_choose = False
            if (num == self.max_number_of_players - 2 and playing_pl == 0) or \
                    (num == self.max_number_of_players - 1 and playing_pl == 1):
                must_choose = True

            # player choosing
            while True:
                # forming message for player
                trait_num = 0
                possible_colors = ""
                for figs in self.figures:
                    trait_num += 1
                    if trait_num != len(self.players) - playing_pl:
                        possible_colors += "[{}]{}, ".format(figs[0].color.prefix, figs[0].color.suffix)
                    else:
                        possible_colors += settings.translation("or_?").format(figs[0].color.prefix,
                                                                               figs[0].color.suffix)
                if not must_choose:
                    possible_colors += settings.translation("this_player_not_playing")

                next_pl = False
                player_option = settings.base_options("which_color_is_player",
                                                      (num + 1, num * self.distance_between_starts + 1,
                                                       possible_colors))
                for figs in self.figures:
                    if player_option == figs[0].color.prefix:
                        self.players[num].playing = True
                        for figure in figs:
                            figure.start.position = num
                        self.players[num].figures = figs
                        self.players[num].color = figs[0].color
                        self.figures.remove(figs)
                        next_pl = True
                        break
                    elif player_option == "N" and not must_choose:
                        self.players[num].playing = False
                        next_pl = True
                        break
                else:
                    if player_option != "skip":
                        settings.translate_slow_print("input_error")
                if next_pl:
                    break

    def removing_redundant_players(self):
        new_players = []

        for player in self.players:
            if player.playing :
                new_players.append(player)

        self.players = new_players

    def rules_setting(self):
        while True:
            self.rules = {"no_rpt_whl_six": False, "rnd_tcs": True, "no_mv_whl_dp": False, "thr_rls_onl_first": True,
                          "no_record": False}
            player_option = settings.base_options("rules_setting")
            if player_option == settings.translation("rules_setting_1"):
                # no repositioning if deploying is possible
                self.rules["no_mv_whl_dp"] = self.choosing_rule("rules_no_mv_whl_dp", "rules_no_mv_whl_dp_1",
                                                                "rules_no_mv_whl_dp_2")

                # random ai tactics
                self.rules["rnd_tcs"] = self.choosing_rule("rules_rnd_tcs", "rules_rnd_tcs_1", "rules_rnd_tcs_2")

                # no repeating when six
                self.rules["no_rpt_whl_six"] = self.choosing_rule("rules_no_rpt_whl_six", "rules_no_rpt_whl_six_1",
                                                                  "rules_no_rpt_whl_six_2")

                # three rolls only before first deployment
                self.rules["thr_rls_onl_first"] = self.choosing_rule("thr_rls_onl_first", "thr_rls_onl_first_1",
                                                                     "thr_rls_onl_first_2")

                return

            # basic settings
            elif player_option == settings.translation("rules_setting_2"):
                return

            elif player_option != "skip":
                settings.translate_slow_print("input_error")

    def ai_setting(self):
        while True:
            player_option = settings.base_options("what_kind_of_players")

            if player_option == settings.translation("ai_setting_1"):
                for player in self.players:
                    player.ai = False
                break
            elif player_option == settings.translation("ai_setting_2"):
                for player in self.players:
                    player.ai = True

                # asking if player wants to have full record of the game or just the result
                self.rules["no_record"] = self.choosing_rule("no_record", "no_record_1", "no_record_2")
                break

            elif player_option == settings.translation("ai_setting_3"):
                return choosing_human_or_ai()
            elif player_option != "skip":
                settings.translate_slow_print("input_error")

    def choosing_human_or_ai(self):
        for player in self.players:
            while player.playing:
                player_option = settings.base_options("player_ai_or_real", (player.number,))
                if player_option == settings.translation("choosing_pl_ai_1"):
                    player.ai = False
                    break
                elif player_option == settings.translation("choosing_pl_ai_2"):
                    player.ai = True
                    break
                elif player_option != "skip":
                    settings.translate_slow_print("input_error")
