class BrokerBase:
    """Basic broker API wrapper."""

    def place_order(self, side: str, amount: float, price: float) -> str:
        raise NotImplementedError
