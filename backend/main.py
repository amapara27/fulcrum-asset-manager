import requests
import pandas
import os

from dotenv import load_dotenv
load_dotenv()

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

def get_prices(symbols):
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

def main():
    symbols = []

    print("Enter your top 5 most held coins:")

    for i in range(5):
        symbol = input()
        symbols.append(symbol)

    print(get_prices(symbols))

if __name__ == "__main__":
    main()