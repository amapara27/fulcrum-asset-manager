import time
import os

import pandas as pd

from sklearn.cluster import KMeans
from price_fetcher import generate_df
from price_fetcher import get_curr_prices

CLUSTERS = 4
ANCHOR_SAFE_ASSET = "USDC"
CACHE_FILE = "data/market_prices.csv"
CACHE_DURATION_SECONDS = 86400

# only generates new data every 24 hrs (increased speed and less API calls)
def get_market_data():
    # check if cache file exists
    if os.path.exists(CACHE_FILE):
        # Get the file's last modified timestamp
        last_modified = os.path.getmtime(CACHE_FILE)
        current_time = time.time()
        
        # check if it is less than 24 hours old
        if current_time - last_modified < CACHE_DURATION_SECONDS:
            print("Loading data from local cache (fast)...")
            # load from CSV and ensure Ticker is the index
            df = pd.read_csv(CACHE_FILE, index_col=0)
            return df
        
        else:
            print("Cache is expired (>24h). Fetching fresh data...")

    else:
        print("No cache found. Fetching fresh data...")

    # fetch fresh data
    df_fresh = generate_df()
    df_fresh.to_csv(CACHE_FILE)
    
    return df_fresh

# train KMeans model
def train_model(df):
    if 'Ticker' in df.columns:
        df = df.set_index('Ticker')

    model = KMeans(n_clusters=CLUSTERS, random_state=42, n_init=10)
    model.fit(df)

    clustered_coins = pd.Series(model.labels_, index=df.index)
    
    return clustered_coins

# classifies what cluster specific coins are in --> used for recommendations
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

# generates hedge recommendations for single asset based on classifications
def get_hedge_rec(coin, clustered_coins):
    if coin not in clustered_coins:
        return "Coin not found in database."

    # 1. Identify the User's Context
    user_cluster_id = clustered_coins[coin]
    user_theme = classify_clusters(user_cluster_id, clustered_coins)
    
    print(f"\n--- ANALYSIS FOR {coin} ---")
    print(f"Asset Class: {user_theme} (Cluster #{user_cluster_id})")

    # 2. Find the "Target" Clusters for Hedging
    safe_cluster_id = -1
    blue_chip_cluster_id = -1
    
    unique_clusters = clustered_coins.unique()
    for c_id in unique_clusters:
        theme = classify_clusters(c_id, clustered_coins)
        if "Safe Haven" in theme:
            safe_cluster_id = c_id
        elif "Blue Chips" in theme:
            blue_chip_cluster_id = c_id

    # 3. Generate Specific Advice
    if "Safe Haven" in user_theme:
        print("Insight: You are playing it safe. This protects capital but limits gains.")
        if blue_chip_cluster_id != -1:
            print(f"Recommendation: For growth, consider adding 'Blue Chip' assets (Cluster #{blue_chip_cluster_id}).")
            print(f"Examples: {clustered_coins[clustered_coins == blue_chip_cluster_id].index.tolist()[:5]}")
            
    elif "High Volatility" in user_theme:
        print("Insight: This is a high-risk 'Degen' play. High upside, massive downside.")
        
        # Suggestion 1: Safety
        if safe_cluster_id != -1:
             print(f"Recommendation A (Safety): Hedge massive swings with 'Safe Haven' assets.")
             print(f"  -> Options: {clustered_coins[clustered_coins == safe_cluster_id].index.tolist()[:5]}")
        
        # Suggestion 2: Majors (The new addition)
        if blue_chip_cluster_id != -1:
             print(f"Recommendation B (Stability): Rotate profits into 'Blue Chips' for sustained growth.")
             print(f"  -> Options: {clustered_coins[clustered_coins == blue_chip_cluster_id].index.tolist()[:5]}")
             
    elif "Blue Chips" in user_theme:
        print("Insight: You hold a Market Mover. It follows the general market trend.")
        print("Recommendation: To reduce volatility, hedge with Stablecoins.")
        if safe_cluster_id != -1:
             print(f"Hedge with: {clustered_coins[clustered_coins == safe_cluster_id].index.tolist()[:5]}")
             
    else: # Mid-Cap Alts
        print("Insight: You hold a Mid-Cap Altcoin. These often bleed against ETH/BTC.")
        print("Recommendation: Consider rotating into market leaders (Blue Chips) or cash (Safe Haven).")

def analyze_portfolio(portfolio_dict, current_prices, clustered_coins):
    cluster_exposure = {}
    total_value = 0.0
    holdings_data = []
    
    # calculate value per cluster
    for coin, quantity in portfolio_dict.items():
        if coin in clustered_coins:
            cluster_id = clustered_coins[coin]
            theme = classify_clusters(cluster_id, clustered_coins)

            price = current_prices.get(coin, 0)
            value = price * quantity
            
            cluster_exposure[cluster_id] = cluster_exposure.get(cluster_id, 0) + value
            total_value += value

            # for table to display
            holdings_data.append({
                "Asset": coin,
                "Value": value,
                "Role": theme
            })

    time.sleep(2.5)
    print("Building dashboard...")

    if total_value == 0:
        print("Portfolio value is $0 or coins not found in database.")
        return

    # prints portfolio breakdown (table view)
    print(f"\n{'='*60}")
    print(f"PORTFOLIO BREAKDOWN (Total: ${total_value:,.2f})")
    print(f"{'='*60}")
    print(f"{'ASSET':<10} | {'VALUE ($)':<12} | {'WEIGHT':<8} | {'ROLE'}")
    print(f"{'-'*60}")
    
    # sort holdings by Value (highest to lowest)
    holdings_data.sort(key=lambda x: x['Value'], reverse=True)
    
    for item in holdings_data:
        weight = (item['Value'] / total_value) * 100
        print(f"{item['Asset']:<10} | {item['Value']:<12,.2f} | {weight:<7.1f}% | {item['Role']}")
    print(f"{'='*60}\n")

    # initialize tracking variables for theme stats
    stats = {
        "Safe Haven": {"pct": 0, "id": -1},
        "Blue Chips": {"pct": 0, "id": -1},
        "High Volatility": {"pct": 0, "id": -1},
        "Altcoins": {"pct": 0, "id": -1}
    }

    time.sleep(2.5)
    print("Loading analysis...")

    print(f"\n--- PORTFOLIO ANALYSIS (Total: ${total_value:,.2f}) ---")
    
    # calculate pct & identify ids
    for c_id, value in cluster_exposure.items():
        pct = (value / total_value) * 100
        theme = classify_clusters(c_id, clustered_coins)
        
        print(f"  {theme}: {pct:.1f}% (${value:,.2f})")

        if "Safe Haven" in theme:
            key = "Safe Haven"
        elif "Blue Chips" in theme:
            key = "Blue Chips"
        elif "High Volatility" in theme:
            key = "High Volatility"
        else:
            key = "Altcoins"
            
        stats[key]["pct"] += pct
        stats[key]["id"] = c_id

    print("\n")

    # fill in Missing ids
    unique_clusters = clustered_coins.unique()
    
    for key in stats:
        if stats[key]["id"] == -1:
            for c in unique_clusters:
                theme = classify_clusters(c, clustered_coins)
                if key in theme: # e.g. "Blue Chips" in "Blue Chips (L1s)"
                    stats[key]["id"] = c
                    break
    
    # Extract vars for readability in logic tree
    safe_pct = stats["Safe Haven"]["pct"]
    safe_id = stats["Safe Haven"]["id"]
    vol_id = stats["High Volatility"]["id"]
    vol_pct = stats["High Volatility"]["pct"]
    blue_chip_pct = stats["Blue Chips"]["pct"]
    blue_chip_id = stats["Blue Chips"]["id"]
    alt_id = stats["Altcoins"]["id"]
    alt_pct = stats["Altcoins"]["pct"]

    time.sleep(2.5)
    print("Generating advice...")

    print(f"--- AI PORTFOLIO RECOMMENDATIONS & ACTION PLAN ---")

    # Scenario 1: The "Barbell" (Cash + Memes, No Middle)
    if safe_pct > 30 and vol_pct > 30 and blue_chip_pct < 10:
        print("⚖️  Diagnosis: The 'Barbell' Strategy.")
        print("   Insight: You are betting on extremes (Safety + High Risk) but lack a solid anchor.")
        print(f"   Action: Consider smoothing volatility by adding 'Blue Chips' (Cluster #{blue_chip_id}).")

    # Scenario 2: The "Altcoin Bleeder" (Too many random alts)
    elif alt_pct > 40:
        print("🩸 Diagnosis: Altcoin Heavy.")
        print("   Insight: You hold many mid-cap assets. Historically, these bleed value against BTC/ETH during downturns.")
        print(f"   Action: Consolidate. Rotate weak performers into Market Leaders (Cluster #{blue_chip_id}).")

    # Scenario 3: The "Degenerate" (Too much Volatility)
    elif vol_pct > 30:
        print("🔥 Diagnosis: High Risk Exposure.")
        print(f"   Insight: {vol_pct:.1f}% of your portfolio is highly speculative.")
        if safe_id != -1:
             print(f"   Action: Lock in profits. Rotate 15% into 'Safe Haven' assets (Cluster #{safe_id}).")

    # Scenario 4: The "Turtle" (Too much Cash)
    elif safe_pct > 50:
        print("🐢 Diagnosis: Excessively Conservative.")
        print("   Insight: You are losing to inflation/opportunity cost.")
        if blue_chip_id != -1:
             print(f"   Action: Deploy capital into 'Blue Chips' (Cluster #{blue_chip_id}) for growth.")

    # Scenario 5: The "Maxi" (Concentration Risk)
    elif blue_chip_pct > 90:
        print("🐳 Diagnosis: Heavy Concentration.")
        print("   Insight: You are highly correlated to the market index.")
        if safe_id != -1:
             print(f"   Action: Add a 5-10% 'Safe Haven' buffer (Cluster #{safe_id}) to buy future dips.")

    # Scenario 6: The "Paper Hands" (No Cash)
    elif safe_pct < 5:
        print("🚨 Diagnosis: Liquidity Danger.")
        print("   Insight: You have zero dry powder to buy the dip.")
        if safe_id != -1:
             print(f"   Action: Build a 10-15% cash position in Cluster #{safe_id}.")

    # Scenario 7: The "Strategist"
    else:
        print("✅ Diagnosis: Healthy Balance.")
        print("   Insight: Well-structured exposure to Growth, Safety, and Speculation.")
        print("   Action: Maintain current weights.")

def main():
    # generates df
    print("Scraping market data...")
    df = get_market_data()

    if 'Ticker' in df.columns:
        df = df.set_index('Ticker')

    time.sleep(2.5)

    print("Training model...")
    time.sleep(2.5)
    print("Generating clusters...")
    clusters = train_model(df)

    time.sleep(2.5)

    # user interface
    while True:
        query = input("\n1. Analyze single asset\n" \
                        "2. Analyze portfolio\n" \
                        "3. Quit\n" \
                        "Enter choice: ")

        match query:
            case '1':
                coin = input("Enter coin ticker: ").upper()
                get_hedge_rec(coin, clusters)
                break

            case '2':
                portfolio = {}

                while True: 
                    coin = input("Enter ticker or Q to quit: ").upper()

                    if coin != 'Q':
                        amt = float(input(f"Enter amount of {coin} held: "))
                        portfolio[coin] = portfolio.get(coin, 0) + amt
                    else:
                        break
                
                curr_prices = get_curr_prices(portfolio.keys())

                analyze_portfolio(portfolio, curr_prices, clusters)
                break     

            case '3':
                break

if __name__ == "__main__":
    main()


