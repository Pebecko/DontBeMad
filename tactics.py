class Tactic:
    def __init__(self, fin_dis=1, kick_out=1, deploy=1):
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out
        self.deploy = deploy


move_nearest = Tactic(10, 6, 1)
kicker = Tactic(6, 10, 2)
deployer = Tactic(1, 6, 10)