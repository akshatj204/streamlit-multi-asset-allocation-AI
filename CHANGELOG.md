# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-29

### Added
- ✨ Initial public release
- 📊 Real-time Signal Dashboard with BUY/HOLD/SELL signals
- 📉 Deep Dive Chart with 9+ technical indicators
- 🗂️ Multi-style India Allocation (Growth, Value, Dividend, Momentum)
- 🌍 Global Asset Allocation dashboard
- 🔀 Combined Portfolio strategy
- 🔍 Live Filters (Signal type, Technical score, Sector) with instant results
- 📈 Macro indicators dashboard (Nifty 50, VIX, USD/INR, G-Sec, Brent Crude)
- ⚡ Signal change detection between data pulls
- 💾 Session state caching for fast switching between tabs
- 🎨 Dark theme with professional styling

### Technical Features
- RSI, MACD, Moving Averages, Bollinger Bands
- ADX, OBV, Volume Analysis, Support/Resistance levels
- Fundamental data: P/E, P/B, ROE, Dividend Yield, Debt-to-Equity
- Analyst consensus and target price tracking
- Market cap classification (Large/Mid/Small cap)

### Data Sources
- Yahoo Finance for stock prices and fundamentals
- NSE India API for index data and macro indicators

### Fixed
- ✅ Resolved KeyError: None when selectbox is empty
- ✅ Replaced deprecated pandas `.applymap()` with `.map()`
- ✅ Improved error handling for delisted stocks
- ✅ Better null validation in dictionary access

---

## Future Releases

### [1.1.0] - Planned
- 🔔 Real-time email/SMS alerts for signal changes
- 📊 Backtesting engine with historical returns
- 🎯 Watchlist feature to save favorite stocks
- 📱 Mobile-responsive design improvements
- ⚙️ Settings panel for indicator customization

### [2.0.0] - Future
- 🤖 Machine Learning predictions
- 📊 Options chain analysis
- 🔥 Advanced heatmaps and correlation matrices
- 🛠️ DIY Screener builder
- 📲 Mobile companion app
- 🌐 International market support (US, EU, Asia)
- 💬 Community stock picks and analysis sharing
- 📈 Portfolio performance tracking and analytics

---

## Version History

### [1.0.0] - 2024-01-29
**Initial Release**
- Core dashboard functionality
- 5 main tabs with comprehensive analysis
- Real-time data from Yahoo Finance and NSE
- 9+ technical indicators
- Multi-style portfolio allocation
- Professional Streamlit UI

---

## Known Issues

### Current Version (1.0.0)
- Some NSE stocks may not have Yahoo Finance data (logged as failures)
- Data pull speed depends on internet and API rate limits
- Colab users may experience longer timeouts
- Analyst data availability varies by stock

### Workarounds
- Use "Top 50" or "Top 100" filter for faster pulls
- Reduce data period to 3-6 months
- Run during off-peak hours
- Check "Failed downloads" in sidebar for details

---

## Deprecation Notices

None currently, but we're monitoring:
- Pandas `.applymap()` → Replaced with `.map()` in v1.0.0
- Yahoo Finance API stability (may need alternative source)
- Streamlit version requirements (maintaining 1.28+)

---

## Upgrade Guide

### From Pre-Release to 1.0.0
1. No database migrations needed
2. Session state format unchanged
3. Data cache structure maintained
4. No API changes

Simply update to the latest version and restart the app.

---

## Development Roadmap

### Q1 2024
- [ ] Add watchlist persistence (localStorage)
- [ ] Implement email notifications
- [ ] Create user settings panel
- [ ] Add data export features (CSV/Excel)

### Q2 2024
- [ ] Backtesting engine v1
- [ ] Options chain basic support
- [ ] International market beta
- [ ] Portfolio tracker

### Q3 2024
- [ ] Machine learning predictions
- [ ] Advanced portfolio analytics
- [ ] Community features
- [ ] Mobile app beta

### Q4 2024
- [ ] Full international support
- [ ] Mobile app release
- [ ] Enterprise features
- [ ] API for third-party integrations

---

## Contributors

### Version 1.0.0
- Original development and dashboard design
- Technical indicator implementation
- Portfolio allocation strategies
- NSE data integration

Special thanks to:
- Yahoo Finance for stock data
- NSE India for market indicators
- Streamlit team for the amazing framework

---

## How to Report Bugs

Found a bug? Please report it on [GitHub Issues](https://github.com/yourusername/nifty500-signal-dashboard/issues)

Include:
- Version number
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

---

## How to Request Features

Have an idea? Create a [GitHub Discussion](https://github.com/yourusername/nifty500-signal-dashboard/discussions)

Include:
- Feature description
- Use case
- Expected behavior
- Why it would be useful

---

## End of Support

- **1.0.0**: Supported until 2.0.0 release (estimated Q3 2024)
- Older versions: No longer supported

---

## Security Policy

See [SECURITY.md](SECURITY.md) for security reporting guidelines.

---

## License

All changes documented here are under the MIT License. See [LICENSE](LICENSE) for details.

---

**Last Updated:** 2024-01-29  
**Maintainer:** [Your Name/Organization]
