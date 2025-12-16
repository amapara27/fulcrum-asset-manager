import requests
import pandas
import time
import os

from dotenv import load_dotenv
load_dotenv()

from collections import defaultdict

COINS = {
    "BTC" : "bitcoin", 
    "ETH" : "ethereum", 
    "USDT" : "tether", 
    "BNB" : "binancecoin", 
    "USDC" : "usd-coin", 
    "XRP" : "ripple",
    "SOL": "solana",
    "TRON" : "tron",
    "DOGE" : "dogecoin",
    "ADA" : "cardano"
}

COIN_GECKO_API_KEY = os.getenv("COIN_GECKO_API_KEY")

def get_curr_prices(symbols):
    prices = {}

    for symbol in symbols:

        coin = COINS[symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&x_cg_demo_api_key={COIN_GECKO_API_KEY}"

        try:
            data = requests.get(url)
            info = data.json()

            coin_info = info[coin]
            prices[symbol] = coin_info["usd"]

        except Exception as e:
            print(f"Error finding prices : {e}")
        
    return prices

def get_historical_prices(symbols):
    prices = defaultdict(list)

    for symbol in symbols:
        id = COINS[symbol]
        url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=90&x_cg_demo_api_key={COIN_GECKO_API_KEY}"

        try:
            data = requests.get(url)
            info = data.json()

            coin_prices = info["prices"]
            prices[symbol].append(coin_prices)

        except Exception as e:
            print(f"Error finding prices : {e}")

        time.sleep(1)
    
    return prices


def main():
    symbols = []

    num = int(input("Enter amount of coins held: "))

    print(f"Enter your top {num} most held coins:")

    for i in range(num):
        symbol = input()
        symbols.append(symbol)
    
    res = get_historical_prices(symbols)

    print(res)

    for key in res:
        print(key)

if __name__ == "__main__":
    main()