import player as pl
import figures as fig
from tactics import move_nearest, kicker, deployer


pl.player1.ai = True
pl.player1.tactic = move_nearest
pl.player2.ai = True
pl.player2.tactic = deployer
pl.player3.ai = True
pl.player4.ai = True


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
            break
        elif player_option == "m" and pl.player1.color != "blue":
            pl.player2.color = "blue"
            pl.player2.figures = [fig.blue_fig1, fig.blue_fig2, fig.blue_fig3, fig.blue_fig4]
            break
        elif player_option == "z" and pl.player1.color != "green":
            pl.player2.color = "green"
            pl.player2.figures = [fig.green_fig1, fig.green_fig2, fig.green_fig3, fig.green_fig4]
            break
        elif player_option == "ž" and pl.player1.color != "yellow":
            pl.player2.color = "yellow"
            pl.player2.figures = [fig.yellow_fig1, fig.yellow_fig2, fig.yellow_fig3, fig.yellow_fig4]
            break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")


def three_players():
    pl.player1.playing = True
    pl.player2.playing = True
    pl.player3.playing = True

    first_player()

    colors = ["red", "blue", "green", "yellow"]
    figures = [[fig.red_fig1, fig.red_fig2, fig.red_fig3, fig.red_fig4],
               [fig.blue_fig1, fig.blue_fig2, fig.blue_fig3, fig.blue_fig4],
               [fig.green_fig1, fig.green_fig2, fig.green_fig3, fig.green_fig4],
               [fig.yellow_fig1, fig.yellow_fig2, fig.yellow_fig3, fig.yellow_fig4]]

    colors.remove(pl.player1.color)
    figures.remove(pl.player1.figures)

    if pl.player1.color == "red":
        players = ["[m]odrá", "[z]elená", "[ž]lutá"]
    elif pl.player1.color == "blue":
        players = ["[č]ervená", "[z]elená", "[ž]lutá"]
    elif pl.player1.color == "green":
        players = ["[č]ervená", "[m]odrá", "[ž]lutá"]
    else:
        players = ["[č]ervená", "[m]odrá", "[z]elená"]

    while True:
        player_option = input("Jaká barva hrát nebude, {}, {}, nebo {}?\n".format(players[0], players[1], players[2]))
        if player_option == "č" and pl.player1.color != "red":
            colors.remove("red")
            del figures[0]
            break
        elif player_option == "m" and pl.player1.color != "blue":
            pos = colors.index("blue")
            colors.remove("blue")
            del figures[pos]
            break
        elif player_option == "z" and pl.player1.color != "green":
            pos = colors.index("green")
            colors.remove("green")
            del figures[pos]
            break
        elif player_option == "ž" and pl.player1.color != "yellow":
            pos = colors.index("yellow")
            colors.remove("yellow")
            del figures[pos]
            break
        else:
            print("Zadaný vstup nesouhlasí s možnostmi.\n")

    pl.player2.color, pl.player2.figures = colors[0], figures[0]
    pl.player3.color, pl.player3.figures = colors[1], figures[1]

    return


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
