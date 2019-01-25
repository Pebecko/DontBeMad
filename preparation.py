from player import player1, player2, player3, player4
from figures import red_figures, blue_figures, green_figures, yellow_figures


# TODO - 6 player game mode


def first_player():
    player1.playing = True
    player2.playing = True
    
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
    first_player()

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


def three_players():
    player3.playing = True

    first_player()

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

    return


def four_players():
    player3.playing = True
    player4.playing = True

    first_player()

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


def player_number():
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
