"""
simple quantconnect strategy to see how it works

pick the top 5 market cap stocks in QQQ index, equal weight
Every 10 months rebalance so equal weight

CURRENT BUGS:
1. It's rebalancing every month, instead of every 10 months
2. It's picking stocks based on name of the stock instead of the market cap
3. This takes many seconds to run. Run report shows:
Algorithm Id:(6e99e3f6452bb131acabf387d346935e) completed in 102.52 seconds at 55k data points per second. Processing total of 5,595,977 data points.

But it should only be looking once every 10 months to rebalance so 5M datapoints seems pretty ridiculous.

Apparently Mia and ChatGPT can't generate working quantconnect code

"""

# region imports
from AlgorithmImports import *

# endregion

NUM_STOCKS = 5  # Number of top stocks by market cap to trade
REBALANCE_MONTHS = (3, 6, 9, 12)  # rebalance months
STOCK_INDEX = "QQQ"  # look only in stocks in QQQ (would like to pick s&p vs. qqq)
STARTING_CASH = 1000000  # starting cash


class MarketCapStrategy(QCAlgorithm):
    def Initialize(self):
        self.set_start_date(2019, 1, 1)  # start
        self.set_end_date(2024, 7, 28)  # last day on free account data
        self.set_cash(STARTING_CASH)  # 1M starting amount

        # Define market cap threshold and limit
        self.market_cap_limit = NUM_STOCKS

        # Universe selection to get fine fundamental data
        self._universe: Universe = self.add_universe(
            self.CoarseSelectionFunction, self.FineSelectionFunction
        )

        # Schedule daily rebalancing
        self.schedule.on(
            self.date_rules.month_start(STOCK_INDEX),
            self.time_rules.at(9, 31),  # at 9:31am rebalance (wait 1 min for data)
            self.Rebalance,
        )

    def CoarseSelectionFunction(self, coarse: list[CoarseFundamental]):
        # Select stocks with fundamental data available and sort by dollar volume
        return [x.symbol for x in coarse if x.has_fundamental_data]

    def FineSelectionFunction(self, fine: list[FineFundamental]):
        # Sort by market cap and select the top stocks
        sorted_by_market_cap = sorted(fine, key=lambda x: x.market_cap, reverse=True)
        top_market_cap_stocks = sorted_by_market_cap[: self.market_cap_limit]
        return [stock.symbol for stock in top_market_cap_stocks]

    def Rebalance(self):
        if self.time.month not in REBALANCE_MONTHS:
            return

        targets: list[PortfolioTarget] = [
            PortfolioTarget(x, 1 / NUM_STOCKS) for x in self._universe.selected
        ]
        self.set_holdings(targets, liquidate_existing_holdings=True)

    def OnEndOfAlgorithm(self):
        ending_cash = self.portfolio.total_portfolio_value
        roi = (ending_cash - STARTING_CASH) / STARTING_CASH * 100
        self.debug(f"Final Portfolio Value: ${ending_cash:.2f}")
        self.debug(f"ROI: {roi:.2f}%")
