# Fulcrum - Crypto Asset Risk Management Tool

> **ML-powered tool that analyzes crypto portfolio correlation and recommends hedge assets to reduce systemic risk.**

## Overview

Fulcrum applies **Modern Portfolio Theory** to cryptocurrency investing using **K-Means Clustering** to identify correlated assets and recommend hedge positions.

**The Problem**: When Bitcoin crashes, most crypto portfolios crash together due to high correlation.

**The Solution**: Analyze price patterns, calculate correlations, cluster coins by behavior, and recommend hedges.

---

## Tech Stack

- **Python 3.9+**
- **Scikit-Learn** (K-Means Clustering, PCA)
- **Pandas** (Data processing & correlation analysis)
- **Matplotlib/Seaborn** (Visualization)
- **CoinGecko API** (90-day historical price data)

---

## Features

### Single Asset Analysis
Analyze any individual cryptocurrency to understand its risk profile and get hedge recommendations based on its cluster classification.

### Portfolio Analysis
Input your entire portfolio with quantities to receive:
- **Portfolio breakdown** with asset values and weights
- **Cluster exposure analysis** showing allocation across risk categories
- **AI-powered recommendations** with specific action plans based on portfolio composition

### Portfolio Visualization
Generates a PCA-based scatterplot that:
- Displays all assets clustered by price behavior
- Highlights your portfolio assets with star markers
- Shows variance explained by principal components
- Saves as high-resolution PNG image

### Intelligent Caching
Market data is cached locally for 24 hours to reduce API calls and improve performance.

---

## Cluster Classifications

| Cluster | Description | Examples |
|---------|-------------|----------|
| Safe Haven | Stablecoins with minimal volatility | USDC, USDT, DAI |
| Blue Chips | Major L1s and market leaders | ETH, SOL, BTC |
| High Volatility | Meme coins and speculative assets | PEPE, DOGE, SHIB |
| Altcoins | Mid-cap alternative cryptocurrencies | Various mid-caps |

---

## Modules

| File | Description |
|------|-------------|
| [main.py](backend/main.py) | CLI interface, K-Means training, portfolio analysis, hedge recommendations |
| [price_fetcher.py](backend/price_fetcher.py) | CoinGecko API integration, data normalization, CSV export |
| [correlation_analyzer.py](backend/correlation_analyzer.py) | Correlation matrix calculation, heatmap generation |
| [portfolio_visualizer.py](backend/portfolio_visualizer.py) | PCA visualization, scatterplot generation with portfolio highlighting |

---

## Usage

### Installation
```bash
cd backend
pip install -r requirements.txt
echo "COIN_GECKO_API_KEY=your_key_here" > .env
```

### Running the Tool
```bash
python main.py
```

### Menu Options

**Option 1: Analyze Single Asset**
```
Enter coin ticker: PEPE

--- ANALYSIS FOR PEPE ---
Asset Class: High Volatility (Memes & Speculative)
Insight: This is a high-risk 'Degen' play. High upside, massive downside.
Recommendation A (Safety): Hedge massive swings with 'Safe Haven' assets.
  -> Options: ['USDC', 'USDT', 'DAI']
```

**Option 2: Analyze Portfolio**
```
Enter ticker or Q to quit: BTC
Enter amount of BTC held: 0.5
Enter ticker or Q to quit: ETH
Enter amount of ETH held: 2
Enter ticker or Q to quit: PEPE
Enter amount of PEPE held: 1000000
Enter ticker or Q to quit: Q

============================================================
PORTFOLIO BREAKDOWN (Total: $52,340.00)
============================================================
ASSET      | VALUE ($)    | WEIGHT   | ROLE
------------------------------------------------------------
BTC        | 47,250.00    | 90.3%    | Blue Chips (L1s & Majors)
ETH        | 4,800.00     | 9.2%     | Blue Chips (L1s & Majors)
PEPE       | 290.00       | 0.5%     | High Volatility (Memes & Speculative)
============================================================

--- AI PORTFOLIO RECOMMENDATIONS & ACTION PLAN ---
🐳 Diagnosis: Heavy Concentration.
   Insight: You are highly correlated to the market index.
   Action: Add a 5-10% 'Safe Haven' buffer to buy future dips.

--- GENERATING VISUALIZATION ---
✓ Portfolio visualization saved to: data/visualizations/portfolio_clusters_20241229_143052.png
```

---

## Visualization Output

The portfolio visualization displays:
- All market assets as circles, colored by cluster
- Your portfolio assets as large star markers with yellow labels
- PCA variance explained on each axis
- Saved to `data/visualizations/` with timestamp

---

## Resources

- [CoinGecko API](https://www.coingecko.com/en/api/documentation)
- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Scikit-Learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Principal Component Analysis](https://scikit-learn.org/stable/modules/decomposition.html#pca)
