class Player:
    def __init__(self, num, color=""):
        self.number = num
        self.color = color
        self.turns = 0
        self.figures = []
        self.playing = False
        self.undeployed = True
        self.result = ""
        self.rolls = []


# definování hráčů
player1 = Player(1)
player2 = Player(2)
player3 = Player(3)
player4 = Player(4)
