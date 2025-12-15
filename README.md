# Fulcrum - Crypto Asset Risk Management Tool

> **A ML-powered dashboard that analyzes crypto portfolio correlation and recommends hedge assets to reduce systemic risk.**

## Overview

Fulcrum is a FinTech application that applies **Modern Portfolio Theory** to cryptocurrency investing. It uses **Unsupervised Machine Learning** (K-Means Clustering) to identify highly correlated assets in your portfolio and recommends hedge positions to reduce overall risk exposure.

### The Problem
When Bitcoin crashes, does your entire portfolio crash? Most crypto portfolios are dangerously correlated - if one asset fails, they all fail together.

### The Solution
Fulcrum analyzes price movement patterns across your holdings and:
- Calculates correlation coefficients between all assets
- Visualizes correlation risk in an interactive heatmap
- Uses ML to cluster coins by behavior (not just category)
- Recommends low/negatively correlated assets as hedges

---

## Tech Stack

### Frontend
- **React** + **TypeScript** + **Vite**
- **react-apexcharts** or **react-chartjs-2** (for correlation heatmap)
- Strict TypeScript interfaces for type safety

### Backend
- **Python** + **FastAPI**
- **Scikit-Learn** (K-Means Clustering & PCA)
- **Pandas** (correlation matrix calculation)
- **CoinGecko API** (90-day historical price data)

### ML/Analytics
- Pearson Correlation Coefficient calculation
- K-Means Clustering on top 100 coins
- Portfolio risk scoring

---

## Architecture & Data Flow

```
┌─────────────┐
│ User Input  │  "BTC, ETH, SOL, PEPE"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Backend (Python/FastAPI)            │
│  1. Fetch 90-day price history      │
│  2. Calculate correlation matrix     │
│  3. Run K-Means on top 100 coins    │
│  4. Identify hedge recommendations   │
└──────┬──────────────────────────────┘
       │
       │  JSON Response
       ▼
┌─────────────────────────────────────┐
│ Frontend (React/TypeScript)         │
│  • Render correlation heatmap       │
│  • Display risk warnings            │
│  • Show hedge recommendations       │
└─────────────────────────────────────┘
```

### Example API Response
```json
{
  "tickers": ["BTC", "ETH", "SOL", "PEPE"],
  "matrix": [
    [1.0, 0.87, 0.85, 0.62],
    [0.87, 1.0, 0.81, 0.58],
    [0.85, 0.81, 1.0, 0.55],
    [0.62, 0.58, 0.55, 1.0]
  ],
  "warning": "High correlation detected: SOL & BTC (0.85)",
  "hedge_recommendation": "PAXG",
  "hedge_correlation": -0.12,
  "clusters": {
    "your_assets": [0, 0, 0, 1],
    "hedge": 3
  }
}
```

---

## Current Progress

### ✅ Completed (Day 0-1)
- [x] Project initialization and repository setup
- [x] Basic CoinGecko API integration
- [x] Environment configuration with `.env` support
- [x] Coin symbol to CoinGecko ID mapping for top 10 coins
- [x] Simple price fetching script for current prices

### Current Implementation
The [backend/main.py](backend/main.py) script currently:
- Accepts 5 coin symbols from user input
- Fetches current USD prices from CoinGecko API
- Maps common symbols (BTC, ETH, SOL, etc.) to CoinGecko IDs
- Includes basic error handling

---

## What Still Needs to Be Built

### Backend ML Engine
- [ ] Fetch **90-day historical prices** (not just current prices)
- [ ] Build correlation matrix using `pandas.DataFrame.corr()`
- [ ] Implement K-Means clustering on top 50-100 coins
- [ ] Calculate Pearson correlation coefficients
- [ ] Identify low/negative correlation hedge assets
- [ ] Structure output as proper JSON response
- [ ] Add FastAPI REST endpoint (`POST /api/analyze`)

### Frontend
- [ ] Initialize Vite + React + TypeScript project
- [ ] Define TypeScript interfaces for API responses
- [ ] Install `react-apexcharts` or `react-chartjs-2`
- [ ] Build reusable Heatmap component
- [ ] Create coin input form (add/remove tags)
- [ ] Set up API client with proper typing

### Integration & Deployment
- [ ] Connect React frontend to FastAPI backend
- [ ] Configure CORS properly
- [ ] Build "AI Insight" card for recommendations
- [ ] Add loading states and error handling
- [ ] Style with modern CSS/Tailwind
- [ ] Deploy backend (Railway/Render)
- [ ] Deploy frontend (Vercel/Netlify)

### Stretch Goals
- [ ] "Simulate Crash" feature: Show portfolio impact if BTC drops 10%
- [ ] Historical backtesting: "If you held this portfolio last year..."
- [ ] Export correlation report as PDF
- [ ] Portfolio rebalancing suggestions based on target correlation

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- CoinGecko API Key (free tier)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt  # Create this file
echo "COIN_GECKO_API_KEY=your_key_here" > .env
python main.py
```

### Frontend Setup (Coming Soon)
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install apexcharts react-apexcharts
npm run dev
```

---

## Learning Objectives

This project is designed to teach:

1. **Machine Learning**: Unsupervised learning (K-Means), feature engineering with financial data
2. **TypeScript**: Working with complex types (2D arrays, interfaces, generics)
3. **Data Visualization**: Building interactive heatmaps from scratch
4. **FinTech Concepts**: Correlation analysis, Modern Portfolio Theory, risk management
5. **Full-Stack Integration**: Type-safe API contracts between Python and TypeScript

---

## API Endpoints (Planned)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze` | Analyze portfolio correlation |
| `GET` | `/api/coins` | Get list of supported coins |
| `GET` | `/api/clusters` | Get current market clusters |

---

## Contributing

This is a learning project. Contributions, suggestions, and questions are welcome!

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Resources

- [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation)
- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Scikit-Learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [ApexCharts Heatmap](https://apexcharts.com/react-chart-demos/heatmaps/basic/)

---

**Status**: 🚧 In Development - Backend ML Engine Phase
