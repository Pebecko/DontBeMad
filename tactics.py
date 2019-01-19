class Tactic:
    def __init__(self, fin_dis=1, kick_out=1, deploy=1, clr_start=1, opp_start=1, run_away=1):
        """1 - 10"""
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out
        self.deploy = deploy
        self.clearing_start = clr_start
        self.opponent_start = opp_start
        self.running_away = run_away


move_nearest = Tactic(10, 6, 1)
kicker = Tactic(6, 10, 2)
deployer = Tactic(1, 6, 10)
running_away = Tactic(1, 1, 1, 1, 1, 10)