import pandas as pd
import random
from datetime import datetime, timedelta

from market import strategy

sma = []

class Sma(strategy.Strategy):

    def initialize(self):
        self.tickers = ["ETH-USD"]
    
    def on_data(self):
        spy_c = self.data["ETH-USD"].Close
        sma_l = spy_c[-35:].mean()
        sma_s = spy_c[-8:].mean()

        self.record("sma_l", sma_l)
        self.record("sma_s", sma_s)

        if self.holdings["ETH-USD"] > 0:
            if sma_s < sma_l:
                self.market_order("ETH-USD", -self.holdings["ETH-USD"])
                self.record("sell", spy_c[-1])

        else:
            if sma_s > sma_l:
                self.market_order("ETH-USD", 1)
                self.record("buy", spy_c[-1])
