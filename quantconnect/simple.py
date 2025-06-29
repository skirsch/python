# region imports
from AlgorithmImports import *

# endregion

SYMBOL_LIST = ["GOOG", "AAPL", "NVDA", "MSFT", "AMZN"]
STARTING_CASH = 1000000
STOCK_INDEX = "SPY"


class MarketCapStrategy(QCAlgorithm):
    def Initialize(self):
        self.set_start_date(2010, 1, 1)
        self.set_end_date(2024, 7, 28)
        self.set_cash(STARTING_CASH)

        for symbol in SYMBOL_LIST:
            self.add_equity(symbol, Resolution.DAILY)

        # Schedule daily rebalancing
        self.schedule.on(
            self.date_rules.year_start(STOCK_INDEX),
            self.time_rules.at(9, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        targets: list[PortfolioTarget] = [
            PortfolioTarget(x, 1 / len(SYMBOL_LIST)) for x in SYMBOL_LIST
        ]
        self.set_holdings(targets, liquidate_existing_holdings=True)

    def OnEndOfAlgorithm(self):
        ending_cash = self.portfolio.total_portfolio_value
        roi = (ending_cash - STARTING_CASH) / STARTING_CASH * 100
        self.debug(f"Final Portfolio Value: ${ending_cash:.2f}")
        self.debug(f"ROI: {roi:.2f}%")
