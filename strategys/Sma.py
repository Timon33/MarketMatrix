import pandas as pd
import random
from datetime import datetime, timedelta
import ta

from market import strategy

sma = []

class Sma(strategy.Strategy):

    def initialize(self):
        self.tickers = ["ETH-USD"]

    def rsi(self, window):
        rsi = ta.momentum.RSIIndicator(self.data["ETH-USD"].Close, window=window).rsi()
        self.record("rsi", rsi[-1])
        return rsi


    def entry_signal(self):
        ema_dst = spy_c[-8:].mean() - spy_c[-35:].mean()
    
    def on_data(self):
        spy_c = self.data["ETH-USD"].Close
        sma_l = spy_c[-35:].mean()
        sma_s = spy_c[-8:].mean()

        self.record("sma_l", sma_l)
        self.record("sma_s", sma_s)

        self.rsi(15)
