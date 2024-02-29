# https://github.com/coinbase/coinbase-advanced-py?tab=readme-ov-file
# https://coinbase.github.io/coinbase-advanced-py/
# OVerview: https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-cfm
# actual calls are in the API Reference tab
from time import time, sleep, ctime
import sys
from coinbase.rest import RESTClient
client=RESTClient()
BUY='BUY'
SELL='SELL'

from json import dumps
# this gets uuid for each asset type that I can hold (28 types)
# accounts = client.get_accounts()
# print(dumps(accounts, indent=2))

# args are $ amount to buy of btc and eth
def place_order(dollar_amount, trading_pair, trade_side):
    print()
    orderID=str(time())+trading_pair  # time+trading_pair is unique
    # place the two orders
    # Note the quote currency matters: it is the account it will draw funds from!
    # Order will fail if use USD and everything is in USDC

    if trade_side==BUY:
        trade_price=client.get_best_bid_ask(trading_pair)['pricebooks'][0]['bids'][0]['price']
        trade_price=float(trade_price)-1     # make sure we get maker fees by ensuring we are a maker by buying 1 point lower than bid
    else: # sell order
        trade_price=client.get_best_bid_ask(trading_pair)['pricebooks'][0]['asks'][0]['price']
        trade_price=float(trade_price)+1     # make sure we get maker fees by ensuring we are a maker by buying 1 point lower than bid

# BTC-USDC, i.e. BTC is the base currency and USDC is the quote currency. 
# I want to buy 0.01 BTC at current market price. 

    amt=str(round(dollar_amount/trade_price,7))  # make sure proper num digits
    order=client.limit_order_gtc(orderID, trading_pair, side=trade_side, base_size=amt, 
                           limit_price=str(trade_price))
    if order['success']:
        # print order in human readable terms
        print(trade_side, amt, trading_pair, "@", trade_price)

# order = client.market_order_buy(client_order_id="clientOrderId", product_id="BTC-USD", quote_size="1")
# print(dumps(order, indent=2))
# place_order(4.50, 'BTC-USD')   # buy $4.50 worth of BTC

# now for the twap to buy 1% of total at num_days/100 interval
def twap(total_USD_amt, trade_side,  pairs, num_hours, granularity=100, start=0):
    sleep_seconds=num_hours*3600/granularity
    for i in range(start, granularity):
        print(f"\n{ctime()}: Placing order {i} of {granularity}")
        print("Minutes between orders=", sleep_seconds/60)
        print("Order amount (USD)", total_USD_amt/(granularity*len(pairs)))
        # place all orders
        for pair in pairs:
            try:
                place_order(total_USD_amt/(granularity*len(pairs)), pair, trade_side)
            except:
                print("An error occurred:", sys.exc_info()[0])  # Print the error type
                print("The error message:", sys.exc_info()[1])  # Print the error message
                # Optionally, you can also print the traceback for more details:
                # traceback.print_exc()
        sleep(sleep_seconds)   # convert entire interval to seconds and divide by number of intervals 

# buy $280K total over 6 hours with 24 trade granularity for $ amount 
# every 15 minutes        
twap(40000, BUY, ('BTC-USDC', 'ETH-USDC'), 6, 50)