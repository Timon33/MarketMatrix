from market.symbol import Symbol

class Order:

    def __init__(self):
        pass

class MarketOrder(Order):

    def __init__(self, symbol: Symbol, qty: float):
        self.symbol = symbol
        self.qty = qty

class LimitOrder(Order):

    def __init__(self, symbol: Symbol, qty: float, limit: float):
        self.symbol = symbol
        self.qty = qty
        self.limit = limit