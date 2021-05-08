import pandas as pd
import random
from datetime import datetime, timedelta
import ta

from market import strategy

sma = []

class Rsi(strategy.Strategy):

    def initialize(self):
        self.sym = "ETH-USD"
        self.tickers = [self.sym]

        self.entry_rsi = 25
        self.exit_rsi = 80
        self.rsi_window = 14

    def rsi(self, window):
        rsi = ta.momentum.RSIIndicator(self.data[self.sym].Close[-window:], window=window).rsi()
        self.record("rsi", rsi[-1])
        return rsi

    def entry_signal(self):

        return self.rsi(self.rsi_window)[-1] < self.entry_rsi
    
    def exit_signal(self):

        return self.rsi(self.rsi_window)[-1] > self.exit_rsi

    def on_data(self):

        if self.holdings[self.sym] > 0 and self.exit_signal():
            self.market_order(self.sym, -self.holdings[self.sym])

        elif self.holdings[self.sym] == 0 and self.entry_signal():
            self.market_order(self.sym, 1)
        
