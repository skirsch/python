# https://github.com/coinbase/coinbase-advanced-py?tab=readme-ov-file
# https://coinbase.github.io/coinbase-advanced-py/
# OVerview: https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-cfm
# actual calls are in the API Reference tab
from time import time
from coinbase.rest import RESTClient
client=RESTClient()

from json import dumps
# this gets uuid for each asset type that I can hold (28 types)
# accounts = client.get_accounts()
# print(dumps(accounts, indent=2))

def place_orders(btc, eth):

    orderID=str(time())
    # place the two orders
    # Note the quote currency matters: it is the account it will draw funds from!
    # Order will fail if use USD and everything is in USDC
    for trading_pair,amt in (('BTC-USD',btc), ('ETH-USD',eth)): 
        bid_price=client.get_best_bid_ask(trading_pair)['pricebooks'][0]['bids'][0]['price']
        bid_price=str(float(bid_price)-1)     # make sure we get maker fees by ensuring we are a maker

## BTC-USDC, i.e. BTC is the base currency and USDC is the quote currency. 
# I want to buy 0.01 BTC at current market price. 
# if you don't change the orderID, it will simply return values for the first
# time you placed the order. OrderID is just the time.
        order=client.limit_order_gtc_buy(orderID+trading_pair, trading_pair, base_size=amt, 
                           limit_price=bid_price)
        print(order)


# order = client.market_order_buy(client_order_id="clientOrderId", product_id="BTC-USD", quote_size="1")
# print(dumps(order, indent=2))
place_orders('.0001', '.001')