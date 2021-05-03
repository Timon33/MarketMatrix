import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

from .strategy import Strategy

interval_to_timedelta = {
    "1m": timedelta(minutes=1),
    "15m": timedelta(minutes=15),
    "30m": timedelta(minutes=30),
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "1wk": timedelta(weeks=1)
}

class BacktestSimulation():

    def __init__(self, strategy: Strategy, start_date: datetime, end_date: datetime=datetime.today(), starting_cash: float=100000, interval: str="1d", parameters: dict=None):

        self.strategy = strategy(start_date, end_date)
        self.strategy._initialize(starting_cash, parameters)

        tickers = self.strategy.tickers

        self.start_date = start_date
        self.end_date = end_date
        self.data = {}

        try:
            self.timedelta = interval_to_timedelta[interval]
        except:
            print(f"time interval '{interval}' not supported")
            return

        for sym in tickers:
            ticker = yf.Ticker(sym)
            try:
                ticker_data = ticker.history(start=start_date, end=end_date, interval=interval)
            except Exception as e:
                print(e)
                continue
            
            self.strategy._holdings[sym] = 0
            self.data[sym] = ticker_data


    def run(self):

        time = self.start_date
        while time < self.end_date:
            data_slice = {}
            for sym in self.data.keys():
                data_slice[sym] = self.data[sym].loc[:time]

            self.strategy._on_data(time, data_slice)

            time += self.timedelta

        self.strategy._terminate()

        return self.strategy