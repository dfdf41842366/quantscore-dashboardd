# 🚀 QuantScore™ Live Dashboard

A real-time stock screening system that ranks equities using a proprietary quantitative formula, specifically designed to identify high-momentum breakout opportunities.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 📊 Overview

QuantScore™ combines price momentum, volume dynamics, and market capitalization to create a comprehensive scoring system for stock selection. The dashboard provides real-time analysis with interactive filtering and professional-grade visualizations.

### Key Features

- **Real-time stock analysis** using Yahoo Finance data
- **Proprietary QuantScore formula** for ranking opportunities
- **Interactive filtering** by RSI, change percentage, and other metrics
- **Live dashboard** with auto-refresh capabilities
- **Export functionality** for further analysis
- **Mobile-responsive design**

## 🧮 QuantScore Formula

```
QuantScore = (|Change%| × Volume^α) / (MarketCap^β)
```

**Default Parameters:**
- α (Alpha) = 1.3 - Volume exponent for liquidity weighting
- β (Beta) = 0.7 - Market cap exponent for size adjustment

**Quality Filters:**
- RSI > 55 (momentum confirmation)
- Change% > 2% (movement threshold)
- Float Shares < 100M (focus on smaller caps)
- Volume > 0 (active trading required)

## 🚀 Quick Start

### Live Demo
Visit the live dashboard: [QuantScore™ Dashboard](https://your-app-name.streamlit.app)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/quantscore-dashboard.git
cd quantscore-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📈 How to Use

### Getting Started
1. **Launch the dashboard** using the link above
2. **Review default tickers** in the sidebar (pre-loaded with popular stocks)
3. **Click "Run QuantScore Analysis"** to start screening
4. **Wait 30-60 seconds** for data to load and process

### Customization
- **Add your tickers:** Enter stock symbols in the sidebar (one per line)
- **Adjust parameters:** Fine-tune Alpha and Beta values
- **Set filters:** Modify RSI minimum, Change minimum based on your strategy
- **Export results:** Download CSV files for further analysis

### Reading Results
- **Higher QuantScore = Better opportunity**
- **Rank 1** = Top pick according to the formula
- **Green metrics** = Positive performance indicators
- **Focus on top 5-10** ranked stocks for best results

## 🔧 Technical Architecture

### Backend Components
- **Streamlit framework** for web interface
- **Yahoo Finance API** for real-time market data
- **Built-in RSI calculations** for technical analysis
- **Pandas/NumPy** for data processing

### Data Sources
- **Stock prices:** Yahoo Finance (yfinance)
- **Volume data:** Real-time trading volume
- **Market cap:** Live market capitalization
- **Technical indicators:** RSI, price changes, momentum

### Performance Features
- **Caching system** (60-second TTL) to prevent API rate limiting
- **Progress tracking** during data fetching
- **Error handling** for missing/invalid data
- **Responsive design** for mobile and desktop

## 📊 Dashboard Features

### Main Interface
- **Live rankings table** with sortable columns
- **Summary metrics** showing analysis overview
- **Top picks highlighting** for quick reference
- **Real-time updates** with market status indicator

### Export & Analysis
- **CSV downloads** with timestamp
- **Formula documentation** built-in
- **Filter customization** for different strategies
- **Sample data preview** for new users

## 🎯 Use Cases

### Day Trading
- Identify high-momentum stocks during market hours
- Screen for breakout opportunities
- Monitor volume-confirmed moves

### Swing Trading
- Find stocks with strong technical momentum
- Filter by RSI for trend confirmation
- Export picks for further fundamental analysis

### Research & Analysis
- Quantitative screening of large stock universes
- Educational tool for understanding market dynamics
- Backtesting framework for momentum strategies

## 📋 Requirements

### System Requirements
- Python 3.7+
- Internet connection for real-time data
- Modern web browser

### Dependencies
```
streamlit>=1.28.0
yfinance>=0.2.18
pandas>=1.5.0
numpy>=1.24.0
```

## 🔒 Data & Privacy

- **No personal data stored** - analysis is performed in real-time
- **Public market data only** - no proprietary information
- **Client-side processing** - your stock picks remain private
- **No registration required** - completely free to use

## 📚 Educational Resources

### Understanding QuantScore
- **Volume weighting** rewards liquid, actively traded stocks
- **Size adjustment** prevents large-cap bias
- **Momentum factor** captures price acceleration
- **Quality filters** ensure technical strength

### Best Practices
- **Use during market hours** (9:30 AM - 4:00 PM EST) for best data
- **Combine with fundamental analysis** - QuantScore is technical only
- **Monitor for volume confirmation** before taking positions
- **Diversify selections** - don't rely on single stock picks

## 🚨 Important Disclaimers

**This tool is for educational and informational purposes only.**

- **Not financial advice** - Always consult with qualified financial advisors
- **Past performance doesn't guarantee future results**
- **Market risks apply** - All investments carry risk of loss
- **Do your own research** - Combine QuantScore with other analysis methods

## 🛠️ Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues:** Create a GitHub issue for bugs or feature requests
- **Questions:** Use GitHub Discussions for general questions
- **Updates:** Watch the repository for new releases

## 🏆 Acknowledgments

- Yahoo Finance for providing free market data
- Streamlit team for the excellent framework
- The open-source Python community

---

**Built with ❤️ for the trading community**

*Last updated: July 2025*