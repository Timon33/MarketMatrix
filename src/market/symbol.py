

class Symbol:

    def __init__(self, ticker: str):

        self.ticker = ticker

    def __hash__(self) -> int:
        return hash(self.ticker)