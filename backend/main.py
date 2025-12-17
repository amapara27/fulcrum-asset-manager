import pandas as pd
import time
from sklearn.cluster import KMeans

from price_fetcher import generate_df

CLUSTERS = 4
ANCHOR_SAFE_ASSET = "USDC"

def train_model(df):
    if 'Ticker' in df.columns:
        df = df.set_index('Ticker')

    model = KMeans(n_clusters=CLUSTERS, random_state=42, n_init=10)
    model.fit(df)

    clustered_coins = pd.Series(model.labels_, index=df.index)
    
    return clustered_coins

def classify_clusters(cluster_id, clustered_coins):
    coins_in_cluster = clustered_coins[clustered_coins == cluster_id].index.tolist()
    
    # Stables
    if "USDC" in coins_in_cluster or "USDT" in coins_in_cluster:
        return "Safe Haven (Stablecoins)"
    
    # Major Alts
    if "ETH" in coins_in_cluster or "SOL" in coins_in_cluster:
        return "Blue Chips (L1s & Majors)"
        
    # Memes & speculative
    if "PEPE" in coins_in_cluster or "DOGE" in coins_in_cluster:
        return "High Volatility (Memes & Speculative)"
        
    # Broad Altcoin market
    return "Altcoins (Mid-Cap)"

def get_hedge_rec(coin, clustered_coins):
    if coin not in clustered_coins:
        return "Coin not found in database."

    # Identify the User's Context
    user_cluster_id = clustered_coins[coin]
    user_theme = classify_clusters(user_cluster_id, clustered_coins)
    
    print(f"\n--- ANALYSIS FOR {coin} ---")
    print(f"Asset Class: {user_theme} (Cluster #{user_cluster_id})")

    # Find the Target Clusters for Hedging
    safe_cluster_id = -1
    blue_chip_cluster_id = -1
    
    # Scan all clusters to find targets
    unique_clusters = clustered_coins.unique()
    for c_id in unique_clusters:
        theme = classify_clusters(c_id, clustered_coins)
        if "Safe Haven" in theme:
            safe_cluster_id = c_id
        elif "Blue Chips" in theme:
            blue_chip_cluster_id = c_id

    # Generate Specific Advice
    if "Safe Haven" in user_theme:
        print("Insight: You are playing it safe. This protects capital but limits gains.")
        if blue_chip_cluster_id != -1:
            print(f"Recommendation: For growth, consider adding 'Blue Chip' assets (Cluster #{blue_chip_cluster_id}).")
            print(f"Examples: {clustered_coins[clustered_coins == blue_chip_cluster_id].index.tolist()[:5]}")
            
    elif "High Volatility" in user_theme:
        print("Insight: This is a high-risk 'Degen' play. High upside, massive downside.")
        print("Recommendation: Lock in profits by hedging with 'Safe Haven' assets.")
        if safe_cluster_id != -1:
             print(f"Hedge with: {clustered_coins[clustered_coins == safe_cluster_id].index.tolist()[:5]}")
             
    elif "Blue Chips" in user_theme:
        print("Insight: You hold a Market Mover. It follows the general market trend.")
        print("Recommendation: To reduce volatility, hedge with Stablecoins.")
        if safe_cluster_id != -1:
             print(f"Hedge with: {clustered_coins[clustered_coins == safe_cluster_id].index.tolist()[:5]}")
             
    else: # Mid-Cap Alts
        print("Insight: You hold a Mid-Cap Altcoin. These often bleed against ETH/BTC.")
        print("Recommendation: Consider rotating into market leaders (Blue Chips) or cash (Safe Haven).")
    

def main():
    # generates df
    print("Scraping market data...")
    df = generate_df()

    # Ensure Ticker is the index
    if 'Ticker' in df.columns:
        df = df.set_index('Ticker')

    # trains kmeans model
    print("Training model...")
    time.sleep(2.5)
    print("Generating clusters...")
    clusters = train_model(df)

    # user interface
    while True:
        user_input = input("\nEnter a coin symbol (or 'q' to quit): ").upper()
        if user_input == 'Q':
            break
        get_hedge_rec(user_input, clusters)

if __name__ == "__main__":
    main()


