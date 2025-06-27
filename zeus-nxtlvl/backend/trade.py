from .broker.base import BaseBroker

class TradeExecutor:
    def __init__(self, broker: BaseBroker):
        self.broker = broker

    def execute(self, symbol, qty, side):
        self.broker.place_order(symbol, qty, side)
