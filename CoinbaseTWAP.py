import time
import requests

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
BASE_URL = "https://api.coinbase.com"

def place_order(asset, quantity):
    # Example: Place a market order
    order = {
        "product_id": asset,
        "side": "buy",
        "type": "market",
        "size": quantity,
    }
    response = requests.post(
        f"{BASE_URL}/v2/orders", json=order, headers={"Authorization": f"Bearer {API_KEY}"}
    )
    print(response.json())

def execute_twap(asset, total_quantity, intervals, duration):
    split_quantity = total_quantity / intervals
    interval_time = duration / intervals

    for i in range(intervals):
        place_order(asset, split_quantity)
        time.sleep(interval_time)  # Wait before placing the next order

# Example usage:
execute_twap("BTC-USD", 0.01, 6, 3600)  # Buy 0.01 BTC over 1 hour in 6 intervals
