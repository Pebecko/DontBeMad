class Tactic:
    def __init__(self, name="", fin_dis=1, kick_out=1, deploy=1, clr_start=1, opp_start=1, run_away=1):
        self.name = name
        self.finnish_distance = fin_dis
        self.kicking_out = kick_out
        self.deploy = deploy
        self.clearing_start = clr_start
        self.opponent_start = opp_start
        self.running_away = run_away


basic = Tactic("basic")
move_nearest = Tactic("move nearest", fin_dis=10)
kicker = Tactic("kick", kick_out=10)
deployer = Tactic("deploy", deploy=10)
running_away = Tactic("run away from other figures", run_away=10)
tac_1 = Tactic("tactic 1", 5, 10, 8, 3, 4, 6)
tac_2 = Tactic("tactic 2", 7, 6, 6, 2, 3, 4)

tactics = [basic, move_nearest, kicker, deployer, running_away, tac_1, tac_2]
