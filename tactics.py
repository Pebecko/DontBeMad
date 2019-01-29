class Tactic:
    def __init__(self, fin_dis=1, kick_out=1, deploy=1, clr_start=1, opp_start=1, run_away=1):
        """1 - 10"""
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out
        self.deploy = deploy
        self.clearing_start = clr_start
        self.opponent_start = opp_start
        self.running_away = run_away


move_nearest = Tactic(10)
kicker = Tactic(kick_out=10)
deployer = Tactic(deploy=10)
running_away = Tactic(run_away=10)
tac_1 = Tactic(5, 10, 8, 3, 4, 6)
tac_2 = Tactic(7, 6, 6, 2, 3, 4)
