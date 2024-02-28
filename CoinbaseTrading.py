# https://github.com/coinbase/coinbase-advanced-py?tab=readme-ov-file
# https://coinbase.github.io/coinbase-advanced-py/
# OVerview: https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-cfm
# actual calls are in the API Reference tab
from time import time, sleep, ctime
from coinbase.rest import RESTClient
client=RESTClient()

from json import dumps
# this gets uuid for each asset type that I can hold (28 types)
# accounts = client.get_accounts()
# print(dumps(accounts, indent=2))

# args are $ amount to buy of btc and eth
def place_order(dollar_amount, trading_pair):

    orderID=str(time())+trading_pair  # time+trading_pair is unique
    # place the two orders
    # Note the quote currency matters: it is the account it will draw funds from!
    # Order will fail if use USD and everything is in USDC

    bid_price=client.get_best_bid_ask(trading_pair)['pricebooks'][0]['bids'][0]['price']
    bid_price=float(bid_price)-1     # make sure we get maker fees by ensuring we are a maker by buying 1 point lower than bid

## BTC-USDC, i.e. BTC is the base currency and USDC is the quote currency. 
# I want to buy 0.01 BTC at current market price. 
# if you don't change the orderID, it will simply return values for the first
# time you placed the order. OrderID is just the time.
    amt=str(round(dollar_amount/bid_price,7))   # need to make sure not too much precision
    order=client.limit_order_gtc_buy(orderID, trading_pair, base_size=amt, 
                           limit_price=str(bid_price))
    print(order)


# order = client.market_order_buy(client_order_id="clientOrderId", product_id="BTC-USD", quote_size="1")
# print(dumps(order, indent=2))
# place_order(4.50, 'BTC-USD')   # buy $4.50 worth of BTC

# now for the twap to buy 1% of total at num_days/100 interval
def twap(total_USD_amt, pairs, num_days, granularity=100, start=0):
    for i in range(start, granularity):
        print(f"\n{ctime()}: Placing order {i} of {granularity}")
        # place all orders
        for pair in pairs:
            place_order(total_USD_amt/(granularity*len(pairs)), pair)
        sleep(num_days*24*3600/granularity)   # convert entire interval to seconds and divide by number of intervals 

# buy $300K total over 3 days with 100 trade granularity
twap(300000, ('BTC-USDC', 'ETH-USDC'), 3, 100)