# 🚀 Quick Start Guide

Get the Nifty 500 Signal Dashboard running in **5 minutes**.

---

## ⚡ 30-Second Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/nifty500-signal-dashboard.git
cd nifty500-signal-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run nifty500_signals_dashboard.py
```

✅ Opens automatically at `http://localhost:8501`

---

## 📋 Requirements

- **Python:** 3.8+
- **OS:** Windows, macOS, Linux
- **RAM:** 2GB minimum
- **Internet:** Required

---

## 🎯 First Run Walkthrough

### Step 1: Start the App (1 min)
```bash
streamlit run nifty500_signals_dashboard.py
```
Browser opens automatically to `http://localhost:8501`

### Step 2: Select Stocks (1 min)
In the left sidebar:
1. Choose **Quick Filter**: "Top 50" (good for beginners)
2. Keep **Data Period**: "6mo" (default)
3. Keep **Include Valuation Ratios**: Checked (✓)

### Step 3: Pull Data (2-3 min)
Click **"🔄 Pull Universe Data"** button
- Status bar shows progress
- Wait for completion (~2-5 minutes)
- You'll see: ✅ 50 stocks loaded

### Step 4: Explore (1 min)
Once data loads:
- 📊 **Signal Dashboard**: See all stocks with buy/sell signals
- 📉 **Deep Dive Chart**: Click any stock for detailed analysis
- 🗂️ **India Allocation**: View portfolio by investment style
- 🌍 **Global Allocation**: See asset allocation
- 🔀 **Combined Portfolio**: Merge strategies

---

## 🎮 Interactive Features

### Instant Filters (No Re-fetch!)
Use sidebar filters to instantly narrow results:
- **Signal**: BUY, HOLD, SELL
- **Min Score**: 0-10 scale
- **Sector**: Industry filter

### Click on Any Stock
In Signal Dashboard → Click stock name → Get detailed analysis

### Customize Allocations
Click sliders in India/Global tabs to adjust allocation %

---

## 🔍 Key Tabs Explained

| Tab | What to Do |
|-----|-----------|
| 📊 Signal Dashboard | See all signals, identify BUY candidates |
| 📉 Deep Dive Chart | Detailed technical + fundamental analysis |
| 🗂️ India Allocation | Build multi-style portfolio (Growth/Value/Dividend) |
| 🌍 Global Allocation | Add international diversification |
| 🔀 Combined Portfolio | Final portfolio composition |

---

## 💡 Tips for Beginners

### 1. Understand the Signals
- **BUY (🟢)**: Score ≥ 2.5 - Strong technical confirmation
- **HOLD (🟡)**: -2.5 to 2.5 - Mixed signals
- **SELL (🔴)**: Score ≤ -2.5 - Weak outlook

### 2. Technical Score (0-10)
Higher = Stronger signal. Components:
- RSI (momentum)
- MACD (trend)
- Moving Averages (direction)
- Bollinger Bands (volatility)
- + 5 more indicators

### 3. Valuation Matters
Don't just follow signals! Check:
- **P/E Ratio**: Lower is better for value investing
- **ROE**: Higher is better
- **Dividend Yield**: Good for income
- **Sector**: Diversify across industries

### 4. Watch Macro Indicators
At the top of dashboard:
- **Nifty 50**: Market trend
- **Nifty VIX**: Fear gauge (low = calm, high = volatile)
- **USD/INR**: Currency impact
- **Brent Crude**: Commodity cycle

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: Only Looking at Signals
✅ **Fix**: Cross-check with valuation ratios and fundamentals

### ❌ Mistake 2: Ignoring Sector Diversification
✅ **Fix**: Use India Allocation tab to balance sectors

### ❌ Mistake 3: Paper Trading on First Day
✅ **Fix**: Test strategies for 1-2 weeks first

### ❌ Mistake 4: Pulling All 500 Stocks
✅ **Fix**: Start with Top 50-100 for faster data pulls

### ❌ Mistake 5: Not Checking Failed Downloads
✅ **Fix**: Look for ⚠️ warning in sidebar, re-pull data

---

## 🔧 Troubleshooting

### "Port 8501 already in use"
```bash
# Use different port
streamlit run nifty500_signals_dashboard.py --server.port=8502
```

### "ModuleNotFoundError"
```bash
# Install dependencies
pip install -r requirements.txt
```

### "No data found for symbol X"
- Some stocks may have no Yahoo Finance data
- Check ⚠️ count in sidebar
- This is normal and automatically handled

### "Very slow data pull"
- Use fewer stocks (Top 50 instead of all 500)
- Reduce data period (3mo instead of 1y)
- Run during off-market hours (higher API limits)

### "Data shows as loading forever"
- Your internet might be slow
- Yahoo Finance API might be rate-limited
- Close and restart the app

---

## 📊 Example Workflow

### Scenario: Find Growth Stocks

1. **Pull Data**
   - Select Top 100
   - Data Period: 6 months
   - Include Fundamentals: Yes

2. **Apply Filters**
   - Signal: BUY
   - Min Score: 7.0
   - Sector: Technology

3. **Analyze Results**
   - Deep Dive Chart on top 3
   - Check P/E < 40
   - Check ROE > 15%

4. **Build Allocation**
   - India Allocation tab
   - Adjust Growth style to 60%
   - Check sector balance

5. **Add Diversification**
   - Global Allocation tab
   - Add US stocks 30%
   - Commodities 10%

6. **Final Check**
   - Combined Portfolio tab
   - Review allocation
   - Ready for paper trading!

---

## 📚 Learning More

### Understanding Indicators
- RSI < 30 = Oversold (potentially BUY)
- RSI > 70 = Overbought (potentially SELL)
- MACD crossover = Trend change
- MA50 > MA200 = Uptrend

### Stock Picking Strategy
1. Technical signal (BUY/SELL)
2. Validate with P/E and ROE
3. Check sector and cap allocation
4. Ensure diversification
5. Paper trade first!

### When to Trade
- Market hours: 9:15 AM - 3:30 PM IST (Monday-Friday)
- Best liquidity: 10 AM - 3 PM
- Avoid: First 15 min (volatile opening)

---

## 🎓 Next Steps

### Week 1: Learn
- [ ] Run dashboard daily
- [ ] Understand each indicator
- [ ] Practice reading charts
- [ ] Paper trade (no real money)

### Week 2: Experiment
- [ ] Try different filters
- [ ] Build 3-4 portfolios
- [ ] Compare allocations
- [ ] Track performance

### Week 3+: Execute
- [ ] Create watchlist
- [ ] Use alerts (when available)
- [ ] Small real trades
- [ ] Keep learning

---

## 🚀 Advanced Features (After Basics)

Once comfortable, explore:
- 🔔 Signal change detection (compare pulls)
- 📈 6-month returns tracking
- 🎨 Custom allocations
- 📊 Sector weighting
- 💹 Backtesting

---

## ❓ FAQs

**Q: Is this free?**  
A: Yes! Open source MIT license.

**Q: Do I need to pay for data?**  
A: No! Uses free Yahoo Finance and NSE APIs.

**Q: Can I get real-time alerts?**  
A: Not yet, but coming in v1.1 🔜

**Q: Can I use this for options?**  
A: Currently stocks only. Options support coming soon.

**Q: How often is data updated?**  
A: You control it. Click "Pull" anytime. Data has 15-min delay.

**Q: Can I deploy online?**  
A: Yes! Use Streamlit Cloud (free tier available).

**Q: Is this financial advice?**  
A: No! Educational tool only. Consult advisor before trading.

---

## 💬 Need Help?

- 📖 Read full [README.md](README.md)
- 🐛 Report bugs on [GitHub Issues](https://github.com/yourusername/nifty500-signal-dashboard/issues)
- 💡 Ask questions in [Discussions](https://github.com/yourusername/nifty500-signal-dashboard/discussions)
- 📧 Email: support@example.com

---

## 📈 Success Checklist

- [ ] App running locally
- [ ] First data pull completed
- [ ] Explored all 5 tabs
- [ ] Applied custom filters
- [ ] Built a test portfolio
- [ ] Understood all indicators
- [ ] Started paper trading

✅ You're ready to go!

---

## ⚡ Power Tips

1. **Bookmark the app** - Easy access
2. **Use Sector filter** - Focus on industries you know
3. **Check Macro first** - Understand market mood (VIX)
4. **Paper trade 2 weeks** - Validate signals before real money
5. **Diversify always** - Don't go all-in on one stock
6. **Set stop losses** - Protect your capital
7. **Review weekly** - Pull fresh data every week

---

**Happy Trading! 📊🚀**

*Remember: This is educational. Always trade responsibly.*

---

**Last Updated:** 2024-01-29  
[← Back to README](README.md)
