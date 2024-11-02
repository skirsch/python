"""
simple quantconnect strategy to see how it works

pick the top 5 market cap stocks in QQQ index, equal weight
Every 10 months rebalance so equal weight

"""

NUM_STOCKS=5         # Number of top stocks by market cap to trade
REBALANCE_MONTH=10   # rebalance every 10 months
MAX_SCAN=100         # look in the top 100 stocks to find top 5 (to limit search for the top 5)? needed?
STOCK_INDEX='QQQ'    # look only in stocks in QQQ (would like to pick s&p vs. qqq)

class MarketCapStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # start
        self.SetEndDate(2024, 7, 28)   # last day on free account data
        self.SetCash(1000000)  # 1M starting amount

        # Define market cap threshold and limit
        self.market_cap_limit = NUM_STOCKS  

        # Universe selection to get fine fundamental data
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # Schedule daily rebalancing
        self.Schedule.On(self.DateRules.MonthStart(STOCK_INDEX, REBALANCE_MONTH), 
                         self.TimeRules.At(9, 30), # at 9:30am rebalance
                         self.Rebalance)

    def CoarseSelectionFunction(self, coarse):
        # Select stocks with fundamental data available and sort by dollar volume
        return [x.Symbol for x in coarse if x.HasFundamentalData][:MAX_SCAN]  # Limit to top  stocks

    def FineSelectionFunction(self, fine):
        # Sort by market cap and select the top stocks
        sorted_by_market_cap = sorted(fine, key=lambda x: x.MarketCap, reverse=True)
        top_market_cap_stocks = sorted_by_market_cap[:self.market_cap_limit]
        return [stock.Symbol for stock in top_market_cap_stocks]

    def Rebalance(self):
        # Liquidate positions in stocks not in the selected top stocks
        for stock in self.Portfolio.Keys:
            if stock not in self.ActiveSecurities.Keys:
                self.Liquidate(stock)

        # Allocate evenly to selected top stocks
        weight = 1 / len(self.ActiveSecurities)
        for stock in self.ActiveSecurities.Values:
            self.SetHoldings(stock.Symbol, weight)

    def OnEndOfAlgorithm(self):
        starting_cash = 100000
        ending_cash = self.Portfolio.TotalPortfolioValue
        roi = (ending_cash - starting_cash) / starting_cash * 100
        self.Debug(f"Final Portfolio Value: ${ending_cash:.2f}")
        self.Debug(f"ROI: {roi:.2f}%")