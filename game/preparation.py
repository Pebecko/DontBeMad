from player import Player
from figures import Figure
from tile import Tile
from settings import settings


def defining_figures():
    settings.translating_colors()

    figures = [[] for x in range(0, len(settings.color_names))]

    for i in range(0, len(settings.color_names)):
        for j in range(1, 5):
            figures[i].append(Figure(j, Tile(0, color=settings.color_names[i], home=True),
                                     Tile(i, finishing=False), settings.color_names[i]))

    return figures


def defining_players(figures):
    players = []
    for i in range(len(figures)):
        players.append(Player(i + 1))

    return players


def choosing_board_size(figures):
    while True:
        # string formatting
        if len(figures) >= 2:
            message = settings.translation("how_big_board")
            for player_number in range(2, len(figures) + 1):
                if player_number == 2:
                    message += "[{}]".format(player_number)
                    if len(figures) == 2:
                        message += settings.translation("two_players").format(player_number)
                elif player_number == len(figures) and len(figures) >= 5:
                    message += settings.translation("or_players_greater_five").format(player_number)
                elif player_number == len(figures):
                    message += settings.translation("or_players_less_five").format(player_number)
                else:
                    message += ", [{}]".format(player_number)
        else:
            message = settings.translation("not_enough_colors_error")

        player_option = settings.base_options(message, translate=False)
        try:
            int(player_option)
        except ValueError:
            if player_option != "skip":
                settings.translate_slow_print("input_error")
        else:
            if 1 < int(player_option) <= len(figures):
                return int(player_option)
            elif player_option != "skip":
                settings.translate_slow_print("input_error")


def player_color_deciding(figures, max_pl, start_gaps):
    players = defining_players(figures)

    for num in range(0, max_pl):
        # no need for player to choose color of last player if there is only one to choose from
        if num == len(players) and len(figures) == 1:
            players[-1].playing = True
            for figure in figures[0]:
                figure.start.position = len(players) - 1
            players[-1].figures = figures[0]
            players[-1].color = figures[0][0].color
            break

        # finding if player must be chosen
        playing_pl = 0
        for player in players:
            if player.playing:
                playing_pl += 1

        must_choose = False
        if (num == max_pl - 2 and playing_pl == 0) or (num == max_pl - 1 and playing_pl == 1):
            must_choose = True

        # player choosing
        while True:
            # forming message for player
            trait_num = 0
            possible_colors = ""
            for figs in figures:
                trait_num += 1
                if trait_num != len(players) - playing_pl:
                    possible_colors += "[{}]{}, ".format(figs[0].color.prefix, figs[0].color.suffix)
                else:
                    possible_colors += settings.translation("or_?").format(figs[0].color.prefix, figs[0].color.suffix)
            if not must_choose:
                possible_colors += settings.translation("this_player_not_playing")

            next_pl = False
            player_option = settings.base_options("which_color_is_player",
                                                  (num + 1, num * start_gaps + 1, possible_colors))
            for figs in figures:
                if player_option == figs[0].color.prefix:
                    players[num].playing = True
                    for figure in figs:
                        figure.start.position = num
                    players[num].figures = figs
                    players[num].color = figs[0].color
                    figures.remove(figs)
                    next_pl = True
                    break
                elif player_option == "N" and not must_choose:
                    players[num].playing = False
                    next_pl = True
                    break
            else:
                if player_option != "skip":
                    settings.translate_slow_print("input_error")
            if next_pl:
                break

    return players


def start_distance_setting():
    while True:
        player_option = settings.base_options("which_distance_between_starts")
        try:
            int(player_option)
        except ValueError:
            if player_option != "skip":
                settings.translate_slow_print("input_error")
        else:
            if int(player_option) < 10:
                settings.translate_slow_print("input_error")
            else:
                return int(player_option)


def choosing_player_ai(players):
    for player in players:
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

    return players


def ai_setting(max_pl, distance, players, no_mv_whl_dp, rnd_tcs):
    while True:
        player_option = settings.base_options("what_kind_of_players")

        if player_option == settings.translation("ai_setting_1"):
            for player in players:
                player.ai = False
            break
        elif player_option == settings.translation("ai_setting_2"):
            for player in players:
                player.ai = True
            break
        elif player_option == settings.translation("ai_setting_3"):
            players = choosing_player_ai(players)
            break
        elif player_option != "skip":
            settings.translate_slow_print("input_error")

    return max_pl, distance, players, no_mv_whl_dp, rnd_tcs


def rules_setting():
    while True:
        player_option = settings.base_options("rules_setting")
        if player_option == settings.translation("rules_setting_1"):
            # no moving while deploying
            while True:
                player_option = settings.base_options("rules_no_mv_whl_dp")
                if player_option == "rules_no_mv_whl_dp_1":
                    no_mv_whl_dp = True
                    break
                elif player_option == "rules_no_mv_whl_dp_2":
                    no_mv_whl_dp = False
                    break
                elif player_option != "skip":
                    settings.translate_slow_print("input_error")
            # random ai tactics
            while True:
                player_option = settings.base_options("rules_rnd_tcs")
                if player_option == "rules_rnd_tcs_1":
                    rnd_tcs = True
                    break
                elif player_option == "rules_rnd_tcs_2":
                    rnd_tcs = False
                    break
                elif player_option != "skip":
                    settings.translate_slow_print("input_error")
            return no_mv_whl_dp, rnd_tcs

        # basic settings
        elif player_option == settings.translation("rules_setting_2"):
            return False, True

        elif player_option != "skip":
            settings.translate_slow_print("input_error")


def board_setting():
    figures = defining_figures()

    max_pl = choosing_board_size(figures)

    distance = start_distance_setting()

    players = player_color_deciding(figures, max_pl, distance)

    no_mv_whl_dp, rnd_tcs = rules_setting()

    return ai_setting(max_pl, distance, players, no_mv_whl_dp, rnd_tcs)
