# Fulcrum - Crypto Asset Risk Management Tool

> **ML-powered tool that analyzes crypto portfolio correlation and recommends hedge assets to reduce systemic risk.**

## Overview

Fulcrum applies **Modern Portfolio Theory** to cryptocurrency investing using **K-Means Clustering** to identify correlated assets and recommend hedge positions.

**The Problem**: When Bitcoin crashes, most crypto portfolios crash together due to high correlation.

**The Solution**: Analyze price patterns, calculate correlations, cluster coins by behavior, and recommend hedges.

---

## Tech Stack

### Backend
- **Python** + **FastAPI** (REST API)
- **Scikit-Learn** (K-Means Clustering)
- **Pandas** (Data processing & correlation analysis)
- **CoinGecko API** (90-day historical price data)
- **Seaborn/Matplotlib** (Heatmap visualization)

### Frontend _(planned)_
- **React** + **TypeScript** + **Vite**
- **ApexCharts** (Interactive correlation heatmap)
- Type-safe API integration

### ML/Analytics
- **K-Means Clustering** (4 clusters trained on 50 coins)
- **Pearson Correlation** coefficients
- **Percentage returns normalization** for ML compatibility

---

## Architecture

```
┌─────────────┐
│ User Input  │  "BTC, ETH, SOL, PEPE"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Backend (Python)                    │
│  1. Fetch 90-day price history      │
│  2. Normalize to % returns          │
│  3. Calculate correlation matrix    │
│  4. Run K-Means clustering          │
│  5. Generate hedge recommendations  │
└──────┬──────────────────────────────┘
       │
       │  JSON Response
       ▼
┌─────────────────────────────────────┐
│ Frontend (React/TypeScript)         │
│  • Render correlation heatmap       │
│  • Display cluster assignments      │
│  • Show hedge recommendations       │
└─────────────────────────────────────┘
```

---

## Current Implementation

### ✅ Core ML Engine Complete
- CoinGecko API integration (50 coins with 90-day historical data)
- Data normalization via percentage returns
- Correlation matrix calculation and heatmap visualization
- K-Means clustering (4 clusters: Safe Haven, Blue Chips, High Volatility, Altcoins)
- Context-aware hedge recommendation system
- Interactive CLI for querying coins

### Modules

**[price_fetcher.py](backend/price_fetcher.py)**: Fetches historical data, normalizes to percentage returns, exports CSV
**[correlation_analyzer.py](backend/correlation_analyzer.py)**: Calculates correlations, generates heatmap PNG
**[main.py](backend/main.py)**: Trains K-Means, classifies clusters, provides hedge recommendations

### Example Usage
```bash
$ python backend/main.py
Enter a coin symbol (or 'q' to quit): PEPE

--- ANALYSIS FOR PEPE ---
Asset Class: High Volatility (Memes & Speculative)
Recommendation: Hedge with Safe Haven assets
Hedge with: ['USDC', 'USDT', 'DAI']
```

---

## Roadmap

### Backend API Layer
- [ ] FastAPI REST endpoints (`POST /api/analyze`, `GET /api/coins`, `GET /api/clusters`)
- [ ] JSON response structure for ML output
- [ ] Portfolio-level risk scoring

### Frontend
- [ ] React + TypeScript + Vite setup
- [ ] Correlation heatmap component (ApexCharts)
- [ ] Coin input form and API integration

### Deployment
- [ ] Backend: Railway/Render
- [ ] Frontend: Vercel/Netlify

### Stretch Goals
- [ ] Crash simulation feature
- [ ] Historical backtesting
- [ ] PDF export
- [ ] Portfolio rebalancing suggestions

---

## Setup

### Prerequisites
Python 3.9+, CoinGecko API Key (free tier)

### Installation
```bash
cd backend
pip install pandas scikit-learn requests python-dotenv seaborn matplotlib
echo "COIN_GECKO_API_KEY=your_key_here" > .env
python main.py
```

---

## Resources

- [CoinGecko API](https://www.coingecko.com/en/api/documentation) | [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) | [Scikit-Learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)

---

**Status**: ✅ Backend ML Engine Complete → 🚧 Building FastAPI REST Layer
