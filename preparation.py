import player as pl
import figures as fig


def first_player():
    while True:
        player_option = input("Jakou bude mít hráč 1 barvu, [č]ervenou, [m]odrou, [z]elenou, nebo [ž]lutou?\n")
        if player_option == "č":
            pl.player1.color = "red"
            pl.player1.figures = [fig.red_fig1, fig.red_fig2, fig.red_fig3, fig.red_fig4]
            return
        elif player_option == "m":
            pl.player1.color = "blue"
            pl.player1.figures = [fig.blue_fig1, fig.blue_fig2, fig.blue_fig3, fig.blue_fig4]
            return
        elif player_option == "z":
            pl.player1.color = "green"
            pl.player1.figures = [fig.green_fig1, fig.green_fig2, fig.green_fig3, fig.green_fig4]
            return
        elif player_option == "ž":
            pl.player1.color = "yellow"
            pl.player1.figures = [fig.yellow_fig1, fig.yellow_fig2, fig.yellow_fig3, fig.yellow_fig4]
            return
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def two_players():
    pl.player1.playing = True
    pl.player2.playing = True

    first_player()

    if pl.player1.color == "red":
        colors = ["[m]odrou", "[z]elenou", "[ž]lutou"]
    elif pl.player1.color == "blue":
        colors = ["[č]ervenou", "[z]elenou", "[ž]lutou"]
    elif pl.player1.color == "green":
        colors = ["[č]ervenou", "[m]odrou", "[ž]lutou"]
    else:
        colors = ["[č]ervenou", "[m]odrou", "[z]elenou"]

    while True:
        player_option = input("Jakou bude mít druhý hráč barvu, {}, {}, nebo {}?\n"
                              "".format(colors[0], colors[1], colors[2]))
        if player_option == "č" and pl.player1.color != "red":
            pl.player2.color = "red"
            pl.player2.figures = [fig.red_fig1, fig.red_fig2, fig.red_fig3, fig.red_fig4]
            return
        elif player_option == "m" and pl.player1.color != "blue":
            pl.player2.color = "blue"
            pl.player2.figures = [fig.blue_fig1, fig.blue_fig2, fig.blue_fig3, fig.blue_fig4]
            return
        elif player_option == "z" and pl.player1.color != "green":
            pl.player2.color = "green"
            pl.player2.figures = [fig.green_fig1, fig.green_fig2, fig.green_fig3, fig.green_fig4]
            return
        elif player_option == "ž" and pl.player1.color != "yellow":
            pl.player2.color = "yellow"
            pl.player2.figures = [fig.yellow_fig1, fig.yellow_fig2, fig.yellow_fig3, fig.yellow_fig4]
            return
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def three_players():
    pl.player1.playing = True
    pl.player2.playing = True
    pl.player3.playing = True

    first_player()

    while True:
        player_option = input("Která barva hrát nebude?\n")


def four_players():
    pl.player1.playing = True
    pl.player2.playing = True
    pl.player3.playing = True
    pl.player4.playing = True

    first_player()

    if pl.player1.color == "red":
        pl1 = pl.player1
        pl2 = pl.player2
        pl3 = pl.player3
        pl4 = pl.player4
    elif pl.player1.color == "blue":
        pl1 = pl.player4
        pl2 = pl.player1
        pl3 = pl.player2
        pl4 = pl.player3
    elif pl.player1.color == "green":
        pl1 = pl.player3
        pl2 = pl.player4
        pl3 = pl.player1
        pl4 = pl.player2
    else:
        pl1 = pl.player2
        pl2 = pl.player3
        pl3 = pl.player4
        pl4 = pl.player1

    pl1.color = "red"
    pl1.figures = [fig.red_fig1, fig.red_fig2, fig.red_fig3, fig.red_fig4]

    pl2.color = "blue"
    pl2.figures = [fig.blue_fig1, fig.blue_fig2, fig.blue_fig3, fig.blue_fig4]

    pl3.color = "green"
    pl3.figures = [fig.green_fig1, fig.green_fig2, fig.green_fig3, fig.green_fig4]

    pl4.color = "yellow"
    pl4.figures = [fig.yellow_fig1, fig.yellow_fig2, fig.yellow_fig3, fig.yellow_fig4]


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
