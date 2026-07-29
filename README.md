# 📈 Nifty 500 Signal Dashboard

A real-time stock analysis and trading signal dashboard for **Nifty 500** stocks using technical indicators, fundamental analysis, and multi-style portfolio allocation strategies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Features

### 📊 Core Dashboard
- **Real-time Signal Generation** - BUY/HOLD/SELL signals based on 8+ technical indicators
- **Live Macro Dashboard** - Nifty 50, Nifty VIX, USD/INR, G-Sec yields, Brent Crude prices
- **Instant Filtering** - Filter by signal type, technical score, and sector without re-fetching data
- **Signal Change Detection** - Track which stocks flipped signals between data pulls

### 📉 Deep Dive Analysis
- **Interactive Charts** - Candlestick, volume, RSI, MACD, Bollinger Bands, ADX, OBV
- **Technical Indicators** - 9+ built-in indicators with visual overlays
- **Support/Resistance Levels** - Auto-calculated from 20-day rolling highs/lows
- **Valuation Ratios** - P/E, P/B, ROE, Dividend Yield, Debt-to-Equity, and more
- **Analyst Consensus** - Target price, upside/downside, analyst rating distribution

### 🗂️ Smart Allocation
- **4 Investment Styles**
  - **Growth** - High ROE + Low P/E
  - **Value** - Undervalued stocks with strong fundamentals
  - **Dividend** - High yield stocks for income
  - **Momentum** - Technical strength + ADX confirmation
  
- **Multi-Cap Allocation** - Large Cap, Mid Cap, Small Cap distribution
- **Sector Weighting** - Balanced across 11 sectors
- **Risk-Adjusted Scoring** - Style-specific scoring for each stock

### 🌍 Global & Combined Portfolio
- **Global Asset Allocation** - Stocks, Bonds, Commodities, Crypto diversification
- **6-Month Returns Tracking** - Historical performance by asset class
- **Combined Portfolio** - Multi-asset strategy across geographies and styles

---

## 📋 Requirements

### System Requirements
- **Python:** 3.8 or higher
- **OS:** Windows, macOS, Linux
- **RAM:** 2GB minimum (4GB recommended)
- **Internet:** Required for data fetching

### Python Dependencies
```
streamlit>=1.0.0
yfinance>=0.2.0
pandas>=1.3.0
numpy>=1.21.0
plotly>=5.0.0
requests>=2.28.0
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nifty500-signal-dashboard.git
cd nifty500-signal-dashboard
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run nifty500_signals_dashboard.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 💻 Usage Guide

### First Launch

1. **Select Stocks**
   - In the sidebar under "🌐 Universe Settings"
   - Choose quick filter (Top 50, Top 100, etc.) or select manually
   - Default: Top 20 stocks

2. **Configure Data Period**
   - Select historical data period: 1 month to 2 years
   - Default: 6 months (good balance of data vs. speed)

3. **Include Valuation Data (Optional)**
   - Enable "Include Valuation Ratios" for P/E, ROE, dividend yields
   - Adds ~1.5 seconds per stock (worth it for fundamental analysis)

4. **Pull Universe Data**
   - Click "🔄 Pull Universe Data"
   - Wait for completion (2-5 minutes depending on count and internet)
   - Data is cached in session state (won't refetch unless you click Refresh)

5. **Apply Instant Filters**
   - After data loads, filters work instantly
   - Signal type: BUY, HOLD, SELL
   - Min Technical Score: 0.0 - 10.0
   - Sector: Filter by industry group

### Dashboard Tabs

#### 📊 Signal Dashboard
- Overview of all stocks with signals
- Sub-tabs: BUY stocks, SELL stocks, Volume spikes, Top 12 by score
- Click on any stock name for details
- Color-coded by signal strength

#### 📉 Deep Dive Chart
- Detailed technical analysis for individual stocks
- Interactive Plotly chart with multiple indicators
- Valuation ratios and analyst consensus
- Support/resistance levels overlay
- Volume profile analysis

#### 🗂️ India Allocation
- Multi-style portfolio construction
- Set allocation % for each style (Growth, Value, Dividend, Momentum)
- View sector-wise and cap-wise distribution
- See top 5 stocks per style
- Check 6-month backtest returns

#### 🌍 Global Allocation
- Asset class diversification (Stocks, Bonds, Commodities, Crypto)
- Set your risk tolerance (Conservative to Aggressive)
- View geographic allocation
- Historical returns by asset class

#### 🔀 Combined Portfolio
- Merge India and Global strategies
- Set India/Global allocation ratio
- View final portfolio composition
- See expected returns and volatility

---

## 🔧 Configuration

### Sidebar Settings

```
Universe Settings
├── Quick Filter: All, Top 50, Top 100, Top 200, Custom
├── Stocks to pull: Multi-select from 500 stocks
├── Data Period: 1mo, 3mo, 6mo, 1y, 2y
├── Include Valuation Ratios: Yes/No
└── Pull Universe Data: Button

Live Filters (Applied Instantly)
├── Signal: BUY, HOLD, SELL
├── Min Tech Score: 0.0 - 10.0
└── Sector: Multi-select from 11 sectors
```

---

## 📊 Technical Indicators Explained

### Signal Scoring System (0-10 scale)

Each indicator contributes points:

| Indicator | Bullish | Neutral | Bearish |
|-----------|---------|---------|---------|
| RSI < 30 | +2 | — | -2 if > 70 |
| MACD Crossover | +2 | +0.5 | -2 |
| MA50 > MA200 | +2 | +1 | -2 |
| Bollinger Bands | +1 if <5% | 0 | -1 if >95% |
| ADX > 25 | +1 | 0 | -1 |
| OBV Trend | +1 | 0 | -1 |
| Volume Spike | +0.5 | 0 | -0.5 |
| Support/Resistance | +0.5 | 0 | -0.5 |

**Final Signal:**
- BUY: Score ≥ 2.5
- HOLD: -2.5 < Score < 2.5
- SELL: Score ≤ -2.5

### Indicators Used

1. **RSI (Relative Strength Index)** - Momentum oscillator, overbought/oversold detection
2. **MACD** - Trend following momentum indicator
3. **Moving Averages (50/200)** - Trend identification
4. **Bollinger Bands** - Volatility and mean reversion
5. **ADX** - Trend strength measurement
6. **OBV (On-Balance Volume)** - Volume confirmation
7. **Support/Resistance** - Pivot levels from 20-day range

---

## 📈 Data Sources

| Data Type | Source | Update Frequency | Delay |
|-----------|--------|-------------------|-------|
| Stock Prices | Yahoo Finance | Daily | 15 minutes |
| Fundamentals | Yahoo Finance | Quarterly | Real-time |
| Nifty 50 Index | NSE India API | Real-time | Live |
| Nifty VIX | NSE India API | Real-time | Live |
| USD/INR | Yahoo Finance | Real-time | 15 min |
| G-Sec 10Y | Yahoo Finance | Real-time | 15 min |
| Brent Crude | Yahoo Finance | Real-time | 15 min |

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install streamlit yfinance plotly pandas numpy requests
```

#### 2. "No data found, symbol may be delisted"
- Some stocks in NSE may have delisted or have no Yahoo Finance data
- These are automatically logged as failures
- Check sidebar for "⚠️ X failed" message
- Pull data again to update the list

#### 3. "Session state does not function when running without `streamlit run`"
- Don't run the script with `python script.py`
- Must use: `streamlit run nifty500_signals_dashboard.py`

#### 4. Port 8501 Already in Use
```bash
# Use a different port
streamlit run nifty500_signals_dashboard.py --server.port=8502
```

#### 5. Slow Data Pull
- Network issue or Yahoo Finance rate limiting
- Wait a few minutes and try again
- Reduce number of stocks if persistently slow
- Colab users: Use shorter periods (1-3 months)

#### 6. "AttributeError: 'Styler' object has no attribute 'applymap'"
- Using old version of the dashboard with new pandas (2.1+)
- **Solution:** Use `nifty500_signals_dashboard_FIXED.py` from releases

---

## 📊 Performance Tips

### For Faster Data Pulls
1. Start with **Top 50** stocks instead of all 500
2. Use **3-month** data period instead of 2 years
3. Uncheck "Include Valuation Ratios" if not needed (saves 30-40%)
4. Run during off-market hours (reduced server load)

### For Faster Filtering
- Filters apply instantly (no refetch)
- Use Signal type + Score filters to narrow down
- Sector filter helps focus on specific industries

### For Better Charts
- Close other apps to free up RAM
- Limit to 100-200 stocks in deep dive tab
- Colab users: Refresh session periodically (max 12 hours)

---

## 🔄 Deployment

### Local Machine
```bash
streamlit run nifty500_signals_dashboard.py
```

### Streamlit Cloud
1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from your GitHub repository
4. Set secrets for any API keys (if needed)

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run nifty500_signals_dashboard.py
```

```bash
docker build -t nifty500-dashboard .
docker run -p 8501:8501 nifty500-dashboard
```

---

## 📝 Project Structure

```
nifty500-signal-dashboard/
├── nifty500_signals_dashboard.py    # Main application
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── LICENSE                           # MIT License
└── docs/
    ├── TECHNICAL_INDICATORS.md      # Indicator explanations
    ├── ALLOCATION_STRATEGIES.md      # Portfolio construction
    └── API_REFERENCE.md              # Function documentation
```

---

## 🎓 Learning Resources

### Understanding Technical Analysis
- [Investopedia - RSI](https://www.investopedia.com/terms/r/rsi.asp)
- [Investopedia - MACD](https://www.investopedia.com/terms/m/macd.asp)
- [Bollinger Bands Guide](https://www.investopedia.com/terms/b/bollingerbands.asp)

### Nifty 500 & NSE
- [NSE India Website](https://www.nseindia.com)
- [Nifty 500 Index](https://www.nseindia.com/products/content/indices/index_smoke_tests.htm)
- [Market Data](https://www.nseindia.com/market-data/live-equity-market)

### Streamlit Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Components](https://streamlit.io/components)

---

## ⚠️ Disclaimer

**This is for educational and research purposes only. Not financial advice.**

- Past performance does not guarantee future results
- Stock market investments carry risk
- Always consult with a financial advisor before trading
- Test strategies with paper trading first
- This tool should not be your only decision-making source

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- [ ] Additional technical indicators
- [ ] International stock support
- [ ] Machine learning predictions
- [ ] Real-time notifications
- [ ] Mobile app version
- [ ] Additional portfolio strategies
- [ ] Performance optimizations

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data:** Yahoo Finance, NSE India API
- **Framework:** Streamlit, Plotly
- **Libraries:** Pandas, NumPy

---

## 📞 Support & Contact

### Issues & Bug Reports
- Open an issue on [GitHub Issues](https://github.com/yourusername/nifty500-signal-dashboard/issues)
- Include Python version, OS, and error message
- Attach screenshots if helpful

### Feature Requests
- Create a new GitHub Discussion
- Describe the use case and expected behavior

### Email
- support@example.com

---

## 🚀 Roadmap

### v1.1 (Next Release)
- [ ] Real-time data updates
- [ ] Email/SMS alerts for signals
- [ ] Portfolio backtesting engine
- [ ] Advanced charting (3D, heatmaps)

### v2.0 (Future)
- [ ] Machine learning predictions
- [ ] Options chain analysis
- [ ] Correlation matrices
- [ ] Screener builder interface
- [ ] Mobile companion app

---

## 📊 Quick Start Command

```bash
# Clone, install, and run in one go
git clone https://github.com/yourusername/nifty500-signal-dashboard.git
cd nifty500-signal-dashboard
pip install -r requirements.txt
streamlit run nifty500_signals_dashboard.py
```

---

## 📈 Sample Output

After first data pull, you'll see:
- ✅ Universe with X stocks loaded
- 🕐 Data timestamp
- ⚠️ Count of failed downloads (if any)
- Interactive dashboard with live signals
- Macro indicators in real-time

---

**Happy Trading! 📊🚀**

*Note: This is a learning tool. Always trade responsibly and manage your risk.*
