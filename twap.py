'''
simple steps

0. Install with pip3 install coinbase-advanced-py


1. Generate trading API keys from Coinbase in their API section. Make sure they are locked to your IP (use your full external IPv4 addresss)
2. Add the keys into your environment variables on your windows box (type "environment" into the search box and you'll get the window to do this)

COINBASE_API_KEY=organizations/c9391bba-6513-42f4-891e-1faceb8aef4/apiKeys/1b8222a6-d8cf-4b47-ab18-66afd77892abcdd1
COINBASE_API_SECRET=-----BEGIN EC PRIVATE KEY-----\nMEEIN356AQcoW__no_imnotshowingyouWthekeythatiuseanditSM49\nAwEHo_wouldntworkifidid__alotsmorecharactersJA==\n-----END EC PRIVATE KEY-----\n

3. edit the last line of the script below with how much you want to buy, which pairs, over how many hours, and the granularity

4. write a .bat script with one line:
python <path to the script>

5. Just double click the script to kick things off


'''

# https://github.com/coinbase/coinbase-advanced-py?tab=readme-ov-file
# https://coinbase.github.io/coinbase-advanced-py/
# OVerview: https://docs.cloud.coinbase.com/advanced-trade-api/docs/rest-api-cfm
# actual calls are in the API Reference tab


# I set the environment variables in my windows environment to my API keys as specified by Coinbase.
# Be sure to make it so your API keys are locked to your machine and that they cannot be used for withdraws, only trading
# Here are what my env variables look like:
# 
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
def twap(total_USD_amt, trade_side,  pair, num_hours, granularity=100, start=0):
    sleep_seconds=num_hours*3600/granularity
    for i in range(start, granularity):
        print(f"\n{ctime()}: Placing order {i} of {granularity}")
        print("Minutes between orders=", sleep_seconds/60)
        print("Order amount (USD)", total_USD_amt/(granularity*len(pairs)))
        # place all orders
       
        try:
            place_order(total_USD_amt/(granularity), pair, trade_side)
        except:
            print("An error occurred:", sys.exc_info()[0])  # Print the error type
            print("The error message:", sys.exc_info()[1])  # Print the error message
                # Optionally, you can also print the traceback for more details:
                # traceback.print_exc()
        sleep(sleep_seconds)   # convert entire interval to seconds and divide by number of intervals 

# buy $280K total over 6 hours with 24 trade granularity for $ amount 
# every 15 minutes        
# twap(40000, BUY, ('BTC-USDC', 'ETH-USDC'), 6, 50)
        
# if buying just a single crypto, don't forget the , or you'll be sorry!
# so the line below makes 100 buys over 12 hours with an objective of $60K
#twap(60000, BUY, ('BTC-USDC',), 12, 100)        

# I have a .bat file which simply has 
# python <path to my script>

# then I just double click the bat file to initiate the transaction

## sell my BTC over .2 hours with 2 trades
# twap(1000, SELL, 'BTC-USDC', .2, 4)      
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the TWAP strategy with specified parameters.")

    # Define command-line arguments
    parser.add_argument("amount", type=float, help="Amount in USD to trade")
    parser.add_argument("side", type=str, choices=[BUY, SELL], help="Side of the trade (buy or sell)")
    parser.add_argument("trading_pair", type=str, help="Trading pair (e.g., BTC-USD)")
    parser.add_argument("num_hours", type=int, help="Total time for the TWAP strategy (in hours)")
    parser.add_argument("granularity", type=int, help="Total number of trades within the time period")

    # Parse arguments
    args = parser.parse_args()

    # Call the twap function with the parsed arguments
    twap(args.amount, args.side, args.trading_pair, args.num_hours, args.granularity)

# Example:  
#       python twap.py 1000 'SELL' 'BTC-USDC', .1, 5)
