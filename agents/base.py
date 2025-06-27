class BaseAgent:
    def __init__(self, capital=1000):
        self.capital = capital
        self.trade_history = []
        self.wins = 0
        self.losses = 0

    def record_trade(self, pnl):
        self.trade_history.append(pnl)
        if pnl > 0:
            self.wins += 1
        elif pnl < 0:
            self.losses += 1

    def day_roi(self):
        if not self.trade_history:
            return 0
        return sum(self.trade_history) / self.capital

    @property
    def win_rate(self):
        total = self.wins + self.losses
        return self.wins / total if total else 0
