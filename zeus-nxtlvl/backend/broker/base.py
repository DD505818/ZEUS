class BaseBroker:
    """Base class for broker implementations."""

    def place_order(self, symbol, quantity, side):
        raise NotImplementedError
