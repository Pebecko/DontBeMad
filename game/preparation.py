from player import players, player_traits


# TODO - Přenastavování pravidel


def board_size():
    # string formating
    if len(players) > 5:
        message = "Jak velkou chcete mít herní plochu, pro [2], [3], [4], [5]"
        for i in range(5, len(players) + 1):
            if i == len(players):
                message += ", nebo [{}] hráčů?\n".format(i)
            else:
                message += ", [{}]".format(i)
    else:
        message = "Něco se pokazilo (není dostatek hráčů)"

    while True:
        player_option = input(message)
        try:
            int(player_option)
        except ValueError:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")
        else:
            if 1 < int(player_option) <= len(players):
                return int(player_option)
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")


def player_color_deciding(max_pl):
    removed_player_traits = []
    for num in range(0, max_pl):
        # no need for player to choose color of last player if there is only one to choose from
        if num == len(players) and len(player_traits) == 1:
            players[-1].playing = True
            for figure in player_traits[0][0]:
                figure.start.position = len(players) - 1
            players[-1].figures = player_traits[0][0]
            players[-1].color = player_traits[0][1]
            break

        # finding if player must be chosen
        playing_pl = 0
        for player in players:
            if player.playing:
                playing_pl += 1

        must_choose = False
        if (num == max_pl - 2 and playing_pl == 0) or (num == max_pl - 1 and playing_pl == 1):
            must_choose = True

        # forming message for player
        trait_num = 0
        possible_colors = ""
        for trait in player_traits:
            trait_num += 1
            if trait_num != len(players) - playing_pl:
                possible_colors += "{}, ".format(trait[2])
            else:
                possible_colors += "nebo {}?".format(trait[2])
        if not must_choose:
            possible_colors += " Pokud si přejete aby nehrál stiskněte [Shift+n] / [N]."

        # player choosing
        while True:
            next = False
            player_option = input("Za jakou barvu bude hrát hráč {} (začíná na políčku {}) {}\n"
                                  "".format(num + 1, num * 10 + 1, possible_colors))
            for trait in player_traits:
                if player_option == trait[3]:
                    players[num].playing = True
                    for figure in trait[0]:
                        figure.start.position = num
                    players[num].figures = trait[0]
                    players[num].color = trait[1]
                    player_traits.remove(trait)
                    removed_player_traits.append(trait)
                    next = True
                    break
                elif player_option == "N" and not must_choose:
                    players[num].playing = False
                    next = True
                    break
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")
            if next:
                break

    # returning traits to list
    for trait in removed_player_traits:
        player_traits.append(trait)

    return


def start_distance_setting():
    while True:
        player_option = input("Jaká vzdálenost bude mezi startovacími políčky? (základní je 10) [zadejte celé číslo"
                              " větší než 9]\n")
        try:
            int(player_option)
        except ValueError:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")
        else:
            if int(player_option) < 10:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")
            else:
                return int(player_option)


def choosing_pl_ai():
    for player in players:
        while player.playing:
            player_option = input("Chcete aby hráč {} byl ovládán [h]ráčem, nebo [u]mělou inteligencí?\n"
                                  "".format(player.number))
            if player_option == "h":
                player.ai = False
                break
            elif player_option == "u":
                player.ai = True
                break
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")


def ai_setting(max_pl, distance):
    while True:
        player_option = input("Bodou hrát jen [h]ráči, samotná [u]mělá inteligence, nebo si chcete [v]ybrat jak budou"
                              " jednotlivé barvy ovládány?\n")
        if player_option == "h":
            for player in players:
                player.ai = False
            break
        elif player_option == "u":
            for player in players:
                player.ai = True
            break
        elif player_option == "v":
            choosing_pl_ai()
            break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

    return max_pl, distance


def board_setting():
    max_pl = board_size()

    player_color_deciding(max_pl)

    distance = start_distance_setting()

    return ai_setting(max_pl, distance)
