import requests
import pandas as pd
import time
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "BNB": "binancecoin",
    "SOL": "solana",
    "USDC": "usd-coin",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "TON": "the-open-network",
    "ADA": "cardano",
    "SHIB": "shiba-inu",
    "AVAX": "avalanche-2",
    "TRX": "tron",
    "DOT": "polkadot",
    "BCH": "bitcoin-cash",
    "LINK": "chainlink",
    "NEAR": "near",
    "MATIC": "matic-network",
    "LTC": "litecoin",
    "ICP": "internet-computer",
    "LEO": "leo-token",
    "DAI": "dai",
    "UNI": "uniswap",
    "APT": "aptos",
    "ETC": "ethereum-classic",
    "MANTLE": "mantle",
    "RNDR": "render-token",
    "HBAR": "hedera-hashgraph",
    "FIL": "filecoin",
    "ATOM": "cosmos",
    "ARB": "arbitrum",
    "IMX": "immutable-x",
    "STX": "blockstack",
    "CRO": "crypto-com-chain",
    "VET": "vechain",
    "MKR": "maker",
    "INJ": "injective-protocol",
    "OP": "optimism",
    "GRT": "the-graph",
    "KAS": "kaspa",
    "XLM": "stellar",
    "XMR": "monero",
    "PEPE": "pepe",
    "FDUSD": "first-digital-usd",
    "SUI": "sui",
    "OKB": "okb",
    "LDO": "lido-dao",
    "QNT": "quant-network",
    "THETA": "theta-token",
    "SEI": "sei-network",
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

def get_historical_prices():
    prices = {}

    for symbol, id in COINS.items():
        url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=90&x_cg_demo_api_key={COIN_GECKO_API_KEY}"

        try:
            data = requests.get(url)
            info = data.json()

            coin_prices = info["prices"]

            formatted_prices = []

            for price in coin_prices:
                ms = price[0]
                s = ms / 1000.0
                date = datetime.datetime.fromtimestamp(s)
                formatted_date = date.strftime("%m-%d-%Y")
                formatted_prices.append([formatted_date, price[1]])

            prices[symbol] = formatted_prices

        except Exception as e:
            print(f"Error finding prices : {e}")

        time.sleep(2)

    return prices

def generate_df():
    prices = get_historical_prices()

    df_list = []

    for ticker, data in prices.items():
        df = pd.DataFrame(data, columns=['date', 'price'])

        # converts dates to pd dates
        df['date'] = pd.to_datetime(df['date'])

        # groups all prices on singular day into and chooses last to represent, then puts into df
        df = df.groupby(df['date'].dt.date)['price'].last().to_frame()

        # renames price column to name of ticker
        df.columns = [ticker]

        df_list.append(df)

    merged = pd.concat(df_list, axis=1)
    merged = merged.dropna()

    # changes from prices to % return - normalizes
    merged_pct = merged.pct_change().dropna()

    final_merged = merged_pct.T

    final_merged.to_csv("prices.csv", index=True)

    return final_merged

def alter_df(df):


    return df

def main():
    # symbols = []

    # num = int(input("Enter amount of coins held: "))

    # print(f"Enter your top {num} most held coins:")

    # for i in range(num):
    #     symbol = input()
    #     symbols.append(symbol.upper())
    
    res = generate_df()

    print(res)

if __name__ == "__main__":
    main()