# 🚀 QuantScore™ Live Dashboard

A real-time stock screening system that ranks equities using a proprietary quantitative formula, designed to identify high-momentum breakout opportunities.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 📊 What It Does

QuantScore™ analyzes stocks in real-time using a mathematical formula that combines:
- **Price momentum** (percentage change)
- **Volume dynamics** (trading activity) 
- **Market capitalization** (company size)

The result is a ranked list of stocks with the highest breakout potential.

## 🧮 The QuantScore Formula

```
QuantScore = (|Change%| × Volume^1.3) / (MarketCap^0.7)
```

**Higher QuantScore = Better Opportunity**

## ✨ Key Features

- 📈 **Real-time stock analysis** using Yahoo Finance data
- 🎯 **Smart filtering** by RSI, change%, and float size
- 📊 **Interactive dashboard** with live updates
- 📄 **Export results** to CSV for further analysis
- 📱 **Mobile-friendly** responsive design
- 🔄 **Auto-refresh** every 60 seconds during market hours
- 🥇 **Top picks highlighting** with medal rankings
- 💡 **Built-in documentation** and methodology

## 🚀 Live Demo

**Try it now:** [QuantScore™ Dashboard](https://your-app-name.streamlit.app)

## 📋 How to Use

### Quick Start
1. **Visit the live dashboard** (link above)
2. **Click "Run QuantScore Analysis"** in the sidebar
3. **Wait 30-60 seconds** for data processing
4. **Review the ranked results** - higher scores are better
5. **Export your picks** using the download button

### Customization
- **Add your own stocks:** Enter tickers in the sidebar (one per line)
- **Adjust filters:** Change RSI minimum, change% requirements, etc.
- **Fine-tune formula:** Modify Alpha and Beta parameters
- **Set refresh:** Enable auto-update during market hours

## 📊 Understanding Results

| Column | Meaning |
|--------|---------|
| **Rank** | Position in QuantScore ranking (1 = best) |
| **Ticker** | Stock symbol |
| **QuantScore** | Proprietary ranking score |
| **Price** | Current stock price |
| **Change%** | Daily price movement |
| **Volume** | Trading volume |
| **Market Cap** | Company valuation |
| **RSI** | Relative Strength Index (momentum indicator) |

## 🎯 Best For

### Day Traders
- Identify high-momentum stocks during market hours
- Find volume-confirmed breakouts
- Screen for gap-up opportunities

### Swing Traders  
- Discover stocks with strong technical momentum
- Filter by RSI for trend confirmation
- Export picks for fundamental analysis

### Researchers
- Quantitative screening of large stock universes
- Educational tool for market dynamics
- Backtesting momentum strategies

## 🔧 Technical Details

### Built With
- **Streamlit** - Web framework
- **Yahoo Finance API** - Real-time market data
- **Pandas/NumPy** - Data processing
- **Python** - Core programming language

### Data Sources
- **Stock prices & volume:** Yahoo Finance
- **Market capitalization:** Real-time company valuations
- **Technical indicators:** Built-in RSI calculations
- **Update frequency:** Every 60 seconds during market hours

## 📚 Quality Filters

The dashboard applies several filters to ensure high-quality picks:

- **RSI > 55** - Confirms upward momentum
- **Change% > 2%** - Ensures significant movement
- **Float < 100M shares** - Focuses on smaller, more volatile stocks
- **Volume > 0** - Requires active trading

## ⏰ Best Usage Times

- **Market Hours:** 9:30 AM - 4:00 PM EST (most accurate data)
- **Pre-Market:** 4:00 AM - 9:30 AM EST (limited data)
- **After-Hours:** 4:00 PM - 8:00 PM EST (limited data)

## 💡 Pro Tips

1. **Focus on Top 5-10** ranked stocks for best opportunities
2. **Use during market hours** for most accurate real-time data
3. **Combine with your research** - QuantScore is technical analysis only
4. **Monitor volume confirmation** before taking positions
5. **Export results** to track historical performance
6. **Look for medal rankings** 🥇🥈🥉 for top picks

## 🚨 Important Disclaimers

**⚠️ This tool is for educational and informational purposes only.**

- **Not financial advice** - Always consult qualified financial advisors
- **Past performance ≠ future results** - Markets are unpredictable
- **All investments carry risk** - You can lose money
- **Do your own research** - Use QuantScore as one factor among many

## 🛠️ Local Installation

Want to run it on your computer? Here's how:

```bash
# Clone the repository
git clone https://github.com/your-username/quantscore-dashboardd.git
cd quantscore-dashboardd

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## 📄 Files in This Repository

- **app.py** - Main dashboard application (complete QuantScore system)
- **requirements.txt** - Python dependencies with exact versions
- **README.md** - This documentation file

## 🔧 System Requirements

- **Python 3.7+**
- **Internet connection** for real-time data
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 📈 Sample Results

Here's what you might see:

| Rank | Ticker | QuantScore | Price | Change% | Volume | RSI |
|------|--------|------------|-------|---------|---------|-----|
| 🥇 1 | TSLA | 0.00123456 | $245.67 | +3.45% | 45.2M | 67.8 |
| 🥈 2 | NVDA | 0.00098765 | $892.34 | +2.87% | 28.1M | 59.3 |
| 🥉 3 | AMD | 0.00087654 | $178.90 | +4.12% | 35.7M | 71.2 |

## 🧮 Formula Explained

The QuantScore formula weighs three key factors:

1. **|Change%|** - Absolute price movement (momentum)
2. **Volume^1.3** - Trading activity with exponential weighting
3. **MarketCap^0.7** - Company size with dampening factor

**Result:** Higher scores indicate stocks with strong momentum, high volume, and reasonable size for explosive potential.

## 🎪 Dashboard Features

### Main Interface
- **Live rankings table** with sortable columns
- **Summary metrics** showing analysis overview
- **Top 3 picks** with medal highlighting 🥇🥈🥉
- **Real-time market status** indicator
- **Progress tracking** during data fetching

### Advanced Features
- **Auto-refresh capability** for live monitoring
- **CSV export** with timestamps
- **Interactive filtering** by multiple criteria
- **Built-in formula documentation**
- **Error handling** for robust performance
- **Mobile-responsive** design

## 🤝 Contributing

Found a bug or have an improvement idea?

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- **Issues:** Create a GitHub issue for bugs or feature requests
- **Questions:** Use GitHub Discussions for general questions
- **Updates:** Watch this repository for new releases

## 🏆 Acknowledgments

- **Yahoo Finance** for providing free, reliable market data
- **Streamlit** for the amazing web framework
- **Python community** for excellent open-source libraries
- **Trading community** for feedback and testing

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Version History

- **v1.0** - Initial release with core QuantScore functionality
- **v1.1** - Added auto-refresh and improved error handling
- **v1.2** - Enhanced UI with medal rankings and better mobile support

---

**Built with ❤️ for traders and investors worldwide**

*Last updated: July 2025*

---

## 🔗 Quick Links

- [Live Dashboard](https://your-app-name.streamlit.app)
- [GitHub Repository](https://github.com/your-username/quantscore-dashboardd)
- [Issues & Support](https://github.com/your-username/quantscore-dashboardd/issues)
- [Discussions](https://github.com/your-username/quantscore-dashboardd/discussions)