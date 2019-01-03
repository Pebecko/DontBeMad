class Tactic:
    def __init__(self, fin_dis=1, kick_out=1, deploy=1, clr_start=1):
        """1 - 10"""
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out
        self.deploy = deploy
        self.clearing_start = clr_start


move_nearest = Tactic(10, 6, 1)
kicker = Tactic(6, 10, 2)
deployer = Tactic(1, 6, 10)
