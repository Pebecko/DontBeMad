class Tactic:
    def __init__(self, fin_dis=1, kick_out=1):
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out


move_nearest = Tactic(10, 8)
kicker = Tactic(5, 10)
