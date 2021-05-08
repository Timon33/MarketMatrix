from datetime import datetime, timedelta
import pandas as pd

class Strategy():

    def __init__(self, start_date: datetime, end_date: datetime):
        self._start_date = start_date
        self._end_date = end_date

        self._recordings = pd.DataFrame()
        self._holdings = {}
        self._trades = []
        self.tickers = []

        self.broker = None

        self.fee = 0

    # propertys
    @property
    def start_cash(self):
        return self._start_cash

    @property
    def start_date(self):
        return self.start_date

    @property
    def end_date(self):
        return self.end_date

    @property
    def holdings(self):
        return self._holdings
    
    @property
    def trades(self):
        return self._trades
    
    @property
    def recordings(self):
        return self._recordings

    @property
    def net_liq(self):
        net_liq = self._cash

        for sym in self.holdings.keys():
            price = self.data[sym].Close[-1]
            net_liq += self.holdings[sym] * price

        return net_liq

    @property
    def bp(self):
        bp = self.net_liq

        for sym in self.holdings.keys():
            price = self.data[sym].Close[-1]
            bp -= abs(self.holdings[sym] * price)

        return bp


    # methodes
    def record(self, name: str, value):
        self._recordings.loc[self.time, name] = value

    def add_ticker(ticker: str):
        self.tickers.append(ticker)

    def market_order(self, symbol: str, qty: float):

        if round(qty) == 0:
            return

        price = self.data[symbol].Close[-1]
        cost = price * qty
        self._cash -= abs(cost) * self.fee

        if abs(cost) < self.bp:
            self._cash -= cost
            self._holdings[symbol] += qty

            self._trades.append({"time": self.time, "symbol": symbol, "price": price, "qty": qty, "cost": cost})
        else:
            raise Exception("Not enoght Buying Power")
    

    # internals
    def _initialize(self, start_cash: float, parameters: dict):
        self._start_cash = start_cash
        self._cash = start_cash
        self._bp = start_cash
        self.paramters = parameters
        self.initialize()

    def _on_data(self, time: datetime, data: dict):
        self.data = data
        self.time = time

        self.record("equity", self.net_liq)
        for sym in data:
            self.record(sym, data[sym].Close[-1])

        self.on_data()

    def _terminate(self):
        self._cash = self.net_liq
        self._holdings = {}
        self.terminate()


    # overwrite
    def initialize(self):
        pass

    def on_data(self):
        pass

    def terminate(self):
        pass

