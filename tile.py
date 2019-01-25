class Tile:
    def __init__(self, position, color="", home=False, finish=False, finishing=True):
        self.position = position
        self.color = color
        self.home = home
        self.finish = finish
        self.finishing = finishing
