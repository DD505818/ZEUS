import pandas as pd

class ORBAgent:
    def __init__(self, symbol, data, range_minutes=15):
        self.symbol = symbol
        self.range_minutes = range_minutes
        self.data = data.copy()
        self.orb_high = None
        self.orb_low = None
        self.triggered = False

    def calculate_opening_range(self):
        open_time = self.data.index[0]
        end_time = open_time + pd.Timedelta(minutes=self.range_minutes)
        opening_range_data = self.data.loc[open_time:end_time]
        self.orb_high = opening_range_data['high'].max()
        self.orb_low = opening_range_data['low'].min()

    def evaluate_breakout(self, current_time):
        if not self.orb_high or not self.orb_low:
            self.calculate_opening_range()

        if self.triggered:
            return None

        current_price = self.data.loc[current_time]['close']
        volume = self.data.loc[current_time]['volume']

        if current_price > self.orb_high and volume > self.data['volume'].rolling(15).mean().iloc[-1]:
            self.triggered = True
            return {
                'signal': 'buy',
                'price': current_price,
                'reason': 'ORB breakout above high',
                'time': current_time
            }
        elif current_price < self.orb_low and volume > self.data['volume'].rolling(15).mean().iloc[-1]:
            self.triggered = True
            return {
                'signal': 'sell',
                'price': current_price,
                'reason': 'ORB breakdown below low',
                'time': current_time
            }
        return None

    def reset_daily(self):
        self.orb_high = None
        self.orb_low = None
        self.triggered = False
