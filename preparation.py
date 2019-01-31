from player import player1, player2, player3, player4, player5, player6
from figures import red_figures, blue_figures, green_figures, yellow_figures, white_figures, orange_figures


def first_player_basic():
    while True:
        player_option = input("Jakou bude mít hráč 1 barvu, [č]ervenou, [m]odrou, [z]elenou, nebo [ž]lutou?\n")
        if player_option == "č":
            player1.color = "red"
            player1.figures = red_figures
            return
        elif player_option == "m":
            player1.color = "blue"
            player1.figures = blue_figures
            return
        elif player_option == "z":
            player1.color = "green"
            player1.figures = green_figures
            return
        elif player_option == "ž":
            player1.color = "yellow"
            player1.figures = yellow_figures
            return
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def two_players():
    first_player_basic()

    if player1.color == "red":
        colors = ["[m]odrou", "[z]elenou", "[ž]lutou"]
    elif player1.color == "blue":
        colors = ["[č]ervenou", "[z]elenou", "[ž]lutou"]
    elif player1.color == "green":
        colors = ["[č]ervenou", "[m]odrou", "[ž]lutou"]
    else:
        colors = ["[č]ervenou", "[m]odrou", "[z]elenou"]

    while True:
        player_option = input("Jakou bude mít druhý hráč barvu, {}, {}, nebo {}?\n"
                              "".format(colors[0], colors[1], colors[2]))
        if player_option == "č" and player1.color != "red":
            player2.color = "red"
            player2.figures = red_figures
            break
        elif player_option == "m" and player1.color != "blue":
            player2.color = "blue"
            player2.figures = blue_figures
            break
        elif player_option == "z" and player1.color != "green":
            player2.color = "green"
            player2.figures = green_figures
            break
        elif player_option == "ž" and player1.color != "yellow":
            player2.color = "yellow"
            player2.figures = yellow_figures
            break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

    return 4, 10


def three_players():
    player3.playing = True

    first_player_basic()

    colors = ["red", "blue", "green", "yellow"]
    figures = [red_figures, blue_figures, green_figures, yellow_figures]

    colors.remove(player1.color)
    figures.remove(player1.figures)

    if player1.color == "red":
        players = ["[m]odrá", "[z]elená", "[ž]lutá"]
    elif player1.color == "blue":
        players = ["[č]ervená", "[z]elená", "[ž]lutá"]
    elif player1.color == "green":
        players = ["[č]ervená", "[m]odrá", "[ž]lutá"]
    else:
        players = ["[č]ervená", "[m]odrá", "[z]elená"]

    while True:
        player_option = input("Jaká barva hrát nebude, {}, {}, nebo {}?\n".format(players[0], players[1], players[2]))
        if player_option == "č" and player1.color != "red":
            colors.remove("red")
            del figures[0]
            break
        elif player_option == "m" and player1.color != "blue":
            pos = colors.index("blue")
            colors.remove("blue")
            del figures[pos]
            break
        elif player_option == "z" and player1.color != "green":
            pos = colors.index("green")
            colors.remove("green")
            del figures[pos]
            break
        elif player_option == "ž" and player1.color != "yellow":
            pos = colors.index("yellow")
            colors.remove("yellow")
            del figures[pos]
            break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

    player2.color, player2.figures = colors[0], figures[0]
    player3.color, player3.figures = colors[1], figures[1]

    return 4, 10


def four_players():
    player3.playing = True
    player4.playing = True

    first_player_basic()

    if player1.color == "red":
        pl1 = player1
        pl2 = player2
        pl3 = player3
        pl4 = player4
    elif player1.color == "blue":
        pl1 = player4
        pl2 = player1
        pl3 = player2
        pl4 = player3
    elif player1.color == "green":
        pl1 = player3
        pl2 = player4
        pl3 = player1
        pl4 = player2
    else:
        pl1 = player2
        pl2 = player3
        pl3 = player4
        pl4 = player1

    pl1.color = "red"
    pl1.figures = red_figures

    pl2.color = "blue"
    pl2.figures = blue_figures

    pl3.color = "green"
    pl3.figures = green_figures

    pl4.color = "yellow"
    pl4.figures = yellow_figures

    return 4, 10


def player_number_basic():
    for figure in red_figures:
        figure.start.position = 0
    for figure in blue_figures:
        figure.start.position = 1
    for figure in green_figures:
        figure.start.position = 2
    for figure in yellow_figures:
        figure.start.position = 3

    while True:
        player_option = input("Budou hrát [2], [3], nebo [4] hráči?\n")
        if player_option == "2":
            return two_players()
        elif player_option == "3":
            return three_players()
        elif player_option == "4":
            return four_players()
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def player_amount():
    while True:
        player_option = input("Jak velkou chcete mít herní plochu, pro [2], [3], [4], [5], nebo [6] hráčů?\n")
        if player_option == "2":
            return 2
        elif player_option == "3":
            return 3
        elif player_option == "4":
            return 4
        elif player_option == "5":
            return 5
        elif player_option == "6":
            return 6
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def playing_players(positions):
    if positions == 2:
        return 2
    elif positions == 3:
        while True:
            player_option = input("Boudou hrát [2], nebo [3] hráči?\n")
            if player_option == "2":
                return 2
            elif player_option == "3":
                return 3
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")
    elif positions == 4:
        while True:
            player_option = input("Boudou hrát [2], [3], nebo [4] hráči?\n")
            if player_option == "2":
                return 2
            elif player_option == "3":
                return 3
            elif player_option == "4":
                return 4
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")
    elif positions == 5:
        while True:
            player_option = input("Boude hrát [2], [3], [4], nebo [5] hráčů?\n")
            if player_option == "2":
                return 2
            elif player_option == "3":
                return 3
            elif player_option == "4":
                return 4
            elif player_option == "5":
                return 5
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")
    else:
        while True:
            player_option = input("Boude hrát [2], [3], [4], [5], nebo [6] hráčů?\n")
            if player_option == "2":
                return 2
            elif player_option == "3":
                return 3
            elif player_option == "4":
                return 4
            elif player_option == "5":
                return 5
            elif player_option == "6":
                return 6
            else:
                print("Zadaný vstup nesouhlasí s možnostmi.\n")


def first_player(playing_pl):
    red_traits = [red_figures, "red", "[č]ervená", "č"]
    blue_traits = [blue_figures, "blue", "[m]odrá", "m"]
    green_traits = [green_figures, "green", "[z]elená", "z"]
    yellow_traits = [yellow_figures, "yellow", "[ž]lutá", "ž"]
    white_traits = [white_figures, "white", "[b]ílá", "b"]
    orange_traits = [orange_figures, "orange", "[o]ranžová", "o"]

    players_traits = [red_traits, blue_traits, green_traits, yellow_traits, white_traits, orange_traits]

    trait_num = 0
    possible_colors = ""
    for trait in players_traits:
        trait_num += 1
        if trait_num != 6:
            possible_colors += "{}, ".format(trait[2])
        else:
            possible_colors += "nebo {}".format(trait[2])

    while True:
        player_option = input("Za jakou barvu bude hrát hráč jedna (začíná na políčku 1) {}?\n".format(possible_colors))
        for trait in players_traits:
            if player_option == trait[3]:
                for figure in trait[0]:
                    figure.start.position = 0
                player1.figures = trait[0]
                player1.color = trait[1]
                players_traits.remove(trait)
                break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

        if len(players_traits) < 6:
            break

    return second_player(playing_pl, players_traits)


def second_player(playing_pl, players_traits):
    trait_num = 0
    possible_colors = ""
    for trait in players_traits:
        trait_num += 1
        if trait_num != 5:
            possible_colors += "{}, ".format(trait[2])
        else:
            possible_colors += "nebo {}".format(trait[2])

    while True:
        player_option = input("Za jakou barvu bude hrát hráč dva (začíná na políčku 11) {}?\n".format(possible_colors))
        for trait in players_traits:
            if player_option == trait[3]:
                for figure in trait[0]:
                    figure.start.position = 1
                player2.figures = trait[0]
                player2.color = trait[1]
                players_traits.remove(trait)
                break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

        if len(players_traits) < 5:
            break

    if playing_pl > 2:
        return third_player(playing_pl, players_traits)
    else:
        return


def third_player(playing_pl, players_traits):
    player3.playing = True
    trait_num = 0
    possible_colors = ""
    for trait in players_traits:
        trait_num += 1
        if trait_num != 4:
            possible_colors += "{}, ".format(trait[2])
        else:
            possible_colors += "nebo {}".format(trait[2])

    while True:
        player_option = input("Za jakou barvu bude hrát hráč tři (začíná na políčku 21) {}?\n".format(possible_colors))
        for trait in players_traits:
            if player_option == trait[3]:
                for figure in trait[0]:
                    figure.start.position = 2
                player3.figures = trait[0]
                player3.color = trait[1]
                players_traits.remove(trait)
                break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

        if len(players_traits) < 4:
            break

    if playing_pl > 3:
        return fourth_player(playing_pl, players_traits)
    else:
        return


def fourth_player(playing_pl, players_traits):
    player4.playing = True
    trait_num = 0
    possible_colors = ""
    for trait in players_traits:
        trait_num += 1
        if trait_num != 3:
            possible_colors += "{}, ".format(trait[2])
        else:
            possible_colors += "nebo {}".format(trait[2])

    while True:
        player_option = input("Za jakou barvu bude mít hráč čtyři (začíná na políčku 31) {}?\n".format(possible_colors))
        for trait in players_traits:
            if player_option == trait[3]:
                for figure in trait[0]:
                    figure.start.position = 3
                player4.figures = trait[0]
                player4.color = trait[1]
                players_traits.remove(trait)
                break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

        if len(players_traits) < 3:
            break

    if playing_pl > 4:
        return fifth_player(playing_pl, players_traits)
    else:
        return


def fifth_player(playing_pl, players_traits):
    player5.playing = True
    trait_num = 0
    possible_colors = ""
    for trait in players_traits:
        trait_num += 1
        if trait_num != 2:
            possible_colors += "{}, ".format(trait[2])
        else:
            possible_colors += "nebo {}".format(trait[2])

    while True:
        player_option = input("Za jakou barvu bude hrát hráč pět (začíná na políčku 41) {}?\n".format(possible_colors))
        for trait in players_traits:
            if player_option == trait[3]:
                for figure in trait[0]:
                    figure.start.position = 4
                player5.figures = trait[0]
                player5.color = trait[1]
                players_traits.remove(trait)
                break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

        if len(players_traits) < 2:
            break

    if playing_pl > 5:
        return sixth_player(players_traits)
    else:
        return


def sixth_player(players_traits):
    player6.playing = True
    for figure in players_traits[0][0]:
        figure.start.position = 5
    player6.figures = players_traits[0][0]
    player6.color = players_traits[0][1]

    return


def start_distance_setting():
    while True:
        player_option = input("Jaká vzdálenost bude mezi startovacími políčky? (základní je 10) [zadejte celé číslo]\n")
        try:
            int(player_option)
        except ValueError:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")
        else:
            return int(player_option)


def board_setting():
    max_pl = player_amount()
    playing_pl = playing_players(max_pl)

    first_player(playing_pl)

    distance = start_distance_setting()

    return max_pl, distance


def board_type():
    player1.playing = True
    player2.playing = True

    while True:
        player_option = input("Chcete hrát na [z]ákladní herní desce, nebo si vytvořit [s]peciální?\n")
        if player_option == "z":
            return player_number_basic()
        elif player_option == "s":
            return board_setting()
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")
