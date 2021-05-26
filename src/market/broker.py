from datetime import datetime, timedelta

from market.order import Order

# Base class for all Brokers
class Broker():

    def __init__(self):
        pass

    def market_order(self, symbol, qty):
        pass

    def limit_order(self, symbol, qty, limit):
        pass

    def send_order(self, order: Order):
        pass


class BacktestBroker(Broker):

    def __init__(self):
        self.orders = {}
        

    def send_order(self, order: Order):
        self.orders[order.symbol] = order

    def _on_data(self, time: datetime, data: dict):

        for symbol in data:
            pass