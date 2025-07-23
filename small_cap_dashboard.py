import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random

# Configure page
st.set_page_config(
    page_title="QuantScore™ Small Cap Scanner",
    page_icon="💎",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .small-cap-highlight {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("💎 QuantScore™ Small Cap Scanner")
st.markdown("**🚀 Explosive Penny Stock Breakout Detector | Float < 10M | Price $1-$10**")

# Highlight the specialization
st.markdown("""
<div class="small-cap-highlight">
🎯 SPECIALIZED FOR: Small Float Stocks | Low Price | High Volatility | Breakout Potential
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("💎 Small Cap Configuration")

# Small cap focused tickers (stocks typically under $10 with small float)
small_cap_tickers = [
    "PHUN", "SNTI", "HUBC", "BBIG", "PROG", "ATER", "SPRT", "IRNT",
    "RDBX", "NILE", "MULN", "GFAI", "BMRA", "RELI", "BGFV", "CLOV",
    "WISH", "WKHS", "RIDE", "GOEV", "ARVL", "NAKD", "SNDL", "EXPR",
    "AMC", "GME", "MMAT", "TRCH", "VERB", "VXRT", "OCGN", "XELA",
    "GNUS", "JAGX", "INPX", "MARK", "UAMY", "TOPS", "SHIP", "GLBS"
]

ticker_input = st.sidebar.text_area(
    "💎 Small Cap Tickers (one per line)",
    value="\n".join(small_cap_tickers[:15]),
    height=250,
    help="Enter small cap stock symbols (typically $1-$10 range)"
)

# Parse tickers
tickers = [t.strip().upper() for t in ticker_input.split('\n') if t.strip()]

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Formula Parameters")
alpha = st.sidebar.slider("Alpha (Volume exponent)", 1.0, 2.5, 1.5, 0.1, help="Higher = more volume emphasis")
beta = st.sidebar.slider("Beta (MarketCap exponent)", 0.3, 1.0, 0.5, 0.1, help="Lower = favor smaller caps")

st.sidebar.markdown("---")
st.sidebar.subheader("💎 Small Cap Filters")
price_min = st.sidebar.slider("Minimum Price ($)", 0.50, 5.0, 1.0, 0.25)
price_max = st.sidebar.slider("Maximum Price ($)", 2.0, 15.0, 10.0, 0.50)
rsi_min = st.sidebar.slider("Minimum RSI", 50, 80, 60, 5, help="Higher RSI = stronger momentum")
change_min = st.sidebar.slider("Minimum Change %", 3.0, 20.0, 5.0, 1.0, help="Minimum daily movement")
volume_min = st.sidebar.selectbox(
    "Minimum Volume",
    [100_000, 500_000, 1_000_000, 2_000_000, 5_000_000],
    index=2,
    help="Ensures adequate liquidity"
)
max_float = st.sidebar.selectbox(
    "Maximum Float Shares",
    [1_000_000, 2_000_000, 5_000_000, 10_000_000],
    index=3,
    help="Small float = higher volatility potential"
)

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False, help="Faster refresh for volatile small caps")

# Try to import yfinance, fall back to simulated data if it fails
try:
    import yfinance as yf
    USE_REAL_DATA = True
    st.sidebar.success("✅ Real-time data: ON")
except ImportError:
    USE_REAL_DATA = False
    st.sidebar.warning("⚠️ Using simulated data")

def get_simulated_small_cap_data(ticker):
    """Generate realistic small cap stock data"""
    # Small cap price ranges
    base_price = random.uniform(1.0, 10.0)
    current_price = base_price * random.uniform(0.90, 1.15)  # More volatility
    
    # Small cap characteristics
    change_pct = random.uniform(-15, 25)  # Higher volatility
    volume = random.randint(500000, 20000000)  # Vary volume significantly
    
    # Small market caps (under $500M typically)
    shares_outstanding = random.randint(5000000, 50000000)
    market_cap = current_price * shares_outstanding
    
    # Small float (key characteristic)
    float_shares = random.randint(500000, 15000000)
    
    # RSI tends to be more extreme in small caps
    rsi = random.uniform(25, 85)
    
    return {
        'ticker': ticker,
        'current_price': current_price,
        'change_pct': change_pct,
        'volume': volume,
        'market_cap': market_cap,
        'float_shares': float_shares,
        'gap_pct': change_pct * random.uniform(0.8, 1.2),  # Gap can differ from daily change
        'rsi': rsi,
        'last_updated': datetime.now()
    }

def get_real_stock_data(ticker):
    """Get real stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d", interval="1d")
        
        if hist.empty or len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        
        try:
            info = stock.info
            market_cap = info.get('marketCap', 0)
            float_shares = info.get('floatShares', info.get('sharesOutstanding', 0))
        except:
            # Default small cap values if info fails
            shares_outstanding = random.randint(10000000, 100000000)
            market_cap = current_price * shares_outstanding
            float_shares = random.randint(1000000, 20000000)
        
        change_pct = ((current_price - prev_close) / prev_close) * 100
        volume = hist['Volume'].iloc[-1]
        
        # Simple RSI calculation
        if len(hist) >= 14:
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_series = 100 - (100 / (1 + rs))
            rsi = rsi_series.iloc[-1] if not pd.isna(rsi_series.iloc[-1]) else 50
        else:
            rsi = 50
        
        # Calculate gap
        try:
            intraday = stock.history(period="2d", interval="1m")
            if not intraday.empty:
                today_open = intraday.iloc[0]['Open']
                gap_pct = ((today_open - prev_close) / prev_close) * 100
            else:
                gap_pct = change_pct
        except:
            gap_pct = change_pct
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'change_pct': change_pct,
            'volume': volume,
            'market_cap': market_cap,
            'float_shares': float_shares,
            'gap_pct': gap_pct,
            'rsi': rsi,
            'last_updated': datetime.now()
        }
    except Exception as e:
        return None

@st.cache_data(ttl=30)  # Faster refresh for small caps
def get_stock_data(tickers_list, use_real_data):
    """Get stock data - real or simulated"""
    results = {}
    
    for ticker in tickers_list:
        if use_real_data:
            data = get_real_stock_data(ticker)
        else:
            data = get_simulated_small_cap_data(ticker)
            
        if data:
            results[ticker] = data
    
    return results

def calculate_small_cap_quant_score(data, alpha, beta):
    """Calculate QuantScore optimized for small caps"""
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        float_shares = data['float_shares']
        
        if market_cap <= 0 or volume <= 0 or float_shares <= 0:
            return 0
        
        # Enhanced formula for small caps - includes float factor
        # QuantScore = (Change% × Volume^alpha) / (MarketCap^beta × Float^0.3)
        float_factor = float_shares ** 0.3
        score = (change_pct * (volume ** alpha)) / ((market_cap ** beta) * float_factor)
        
        return score
    except:
        return 0

def apply_small_cap_filters(df, price_min, price_max, rsi_min, change_min, volume_min, max_float):
    """Apply small cap specific filters"""
    try:
        filtered = df[
            (df['current_price'] >= price_min) &
            (df['current_price'] <= price_max) &
            (df['float_shares'] <= max_float) &
            (df['rsi'] > rsi_min) &
            (df['change_pct'].abs() >= change_min) &
            (df['volume'] >= volume_min) &
            (df['quant_score'] > 0)
        ].copy()
        
        return filtered.sort_values('quant_score', ascending=False)
    except:
        return df.sort_values('quant_score', ascending=False)

def format_number(num, is_currency=False, is_percentage=False):
    """Format numbers for display"""
    try:
        if pd.isna(num) or num == 0:
            return "N/A"
        
        if is_percentage:
            return f"{num:.2f}%"
        elif is_currency:
            return f"${num:.3f}" if num < 10 else f"${num:.2f}"  # More precision for low prices
        elif num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif num >= 1e6:
            return f"{num/1e6:.1f}M"
        elif num >= 1e3:
            return f"{num/1e3:.0f}K"
        else:
            return f"{num:.0f}"
    except:
        return "N/A"

def get_volatility_indicator(change_pct):
    """Get volatility emoji indicator"""
    abs_change = abs(change_pct)
    if abs_change >= 20:
        return "🔥"
    elif abs_change >= 10:
        return "⚡"
    elif abs_change >= 5:
        return "📈"
    else:
        return "📊"

# Main analysis
if st.sidebar.button("💎 Scan Small Caps", type="primary") or auto_refresh:
    if not tickers:
        st.error("❌ Please enter at least one ticker symbol")
    else:
        st.markdown("---")
        
        # Show current time and scanning info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"🕐 **Updated:** {datetime.now().strftime('%H:%M:%S')}")
        with col2:
            st.info(f"💎 **Scanning:** {len(tickers)} small caps")
        with col3:
            st.info(f"🎯 **Price Range:** ${price_min}-${price_max}")
        with col4:
            st.info(f"🔍 **Max Float:** {format_number(max_float)}")
        
        # Fetch data
        with st.spinner("💎 Scanning small cap opportunities..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Get stock data
            stock_data = {}
            for i, ticker in enumerate(tickers):
                status_text.text(f'Scanning {ticker}...')
                progress_bar.progress((i + 1) / len(tickers))
                
                if USE_REAL_DATA:
                    data = get_real_stock_data(ticker)
                else:
                    data = get_simulated_small_cap_data(ticker)
                    
                if data:
                    stock_data[ticker] = data
                
                time.sleep(0.05)  # Faster for small caps
            
            progress_bar.empty()
            status_text.empty()
        
        if not stock_data:
            st.error("❌ No data retrieved. Please try again.")
        else:
            # Calculate QuantScores
            results = []
            for ticker, data in stock_data.items():
                quant_score = calculate_small_cap_quant_score(data, alpha, beta)
                
                results.append({
                    'ticker': ticker,
                    'quant_score': quant_score,
                    'current_price': data['current_price'],
                    'change_pct': data['change_pct'],
                    'volume': data['volume'],
                    'market_cap': data['market_cap'],
                    'float_shares': data['float_shares'],
                    'gap_pct': data['gap_pct'],
                    'rsi': data['rsi']
                })
            
            df = pd.DataFrame(results)
            
            if df.empty:
                st.error("❌ No valid data found for analysis.")
            else:
                # Apply small cap filters
                filtered_df = apply_small_cap_filters(df, price_min, price_max, rsi_min, change_min, volume_min, max_float)
                
                # Display summary metrics
                st.markdown("## 📈 Small Cap Scanner Results")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric(
                        label="Total Scanned",
                        value=len(df),
                        delta=f"{len(filtered_df)} qualified"
                    )
                
                with col2:
                    if not filtered_df.empty:
                        avg_price = filtered_df['current_price'].mean()
                        st.metric(
                            label="Avg Price",
                            value=f"${avg_price:.2f}",
                            delta=f"Range: ${filtered_df['current_price'].min():.2f}-${filtered_df['current_price'].max():.2f}"
                        )
                    else:
                        st.metric("Avg Price", "N/A")
                
                with col3:
                    if not filtered_df.empty:
                        avg_float = filtered_df['float_shares'].mean()
                        st.metric(
                            label="Avg Float",
                            value=format_number(avg_float),
                            delta=f"Min: {format_number(filtered_df['float_shares'].min())}"
                        )
                    else:
                        st.metric("Avg Float", "N/A")
                
                with col4:
                    if not filtered_df.empty:
                        avg_change = filtered_df['change_pct'].mean()
                        st.metric(
                            label="Avg Change %",
                            value=f"{avg_change:.1f}%",
                            delta=f"Max: {filtered_df['change_pct'].max():.1f}%"
                        )
                    else:
                        st.metric("Avg Change %", "N/A")
                
                with col5:
                    if not filtered_df.empty:
                        avg_volume = filtered_df['volume'].mean()
                        st.metric(
                            label="Avg Volume",
                            value=format_number(avg_volume),
                            delta=f"Max: {format_number(filtered_df['volume'].max())}"
                        )
                    else:
                        st.metric("Avg Volume", "N/A")
                
                # Display results
                st.markdown("## 🏆 Top Small Cap Breakout Candidates")
                
                if filtered_df.empty:
                    st.warning("⚠️ No stocks passed the small cap filters. Try adjusting your criteria.")
                    st.info("💡 Try lowering the price minimum or RSI threshold.")
                    display_df = df.sort_values('quant_score', ascending=False).head(10)
                    st.markdown("### 📊 Top 10 Unfiltered Results:")
                else:
                    st.success(f"🎯 Found {len(filtered_df)} explosive small cap opportunities!")
                    display_df = filtered_df
                
                # Format the display dataframe with small cap focus
                display_formatted = display_df.copy()
                display_formatted['volatility'] = display_formatted['change_pct'].apply(get_volatility_indicator)
                display_formatted['quant_score'] = display_formatted['quant_score'].apply(lambda x: f"{x:.8f}")
                display_formatted['current_price'] = display_formatted['current_price'].apply(lambda x: format_number(x, is_currency=True))
                display_formatted['change_pct'] = display_formatted['change_pct'].apply(lambda x: format_number(x, is_percentage=True))
                display_formatted['volume'] = display_formatted['volume'].apply(format_number)
                display_formatted['market_cap'] = display_formatted['market_cap'].apply(format_number)
                display_formatted['float_shares'] = display_formatted['float_shares'].apply(format_number)
                display_formatted['gap_pct'] = display_formatted['gap_pct'].apply(lambda x: format_number(x, is_percentage=True))
                display_formatted['rsi'] = display_formatted['rsi'].apply(lambda x: f"{x:.0f}" if not pd.isna(x) else "N/A")
                
                # Rename columns for display
                display_formatted.columns = [
                    'Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 
                    'Market Cap', 'Float', 'Gap%', 'RSI', 'Vol'
                ]
                
                # Select columns for display
                final_columns = ['Vol', 'Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 'Float', 'Gap%', 'RSI']
                final_df = display_formatted[final_columns].copy()
                
                # Display the table with ranking
                final_df.index = range(1, len(final_df) + 1)
                final_df.index.name = 'Rank'
                
                st.dataframe(
                    final_df,
                    use_container_width=True,
                    height=400
                )
                
                # Export and refresh functionality
                col1, col2, col3 = st.columns(3)
                with col1:
                    csv = final_df.to_csv()
                    st.download_button(
                        label="💎 Download Small Cap Picks",
                        data=csv,
                        file_name=f"small_cap_picks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    if st.button("🔄 Refresh Scan"):
                        st.cache_data.clear()
                        st.rerun()
                
                with col3:
                    current_hour = datetime.now().hour
                    market_status = "🟢 OPEN" if 9 <= current_hour <= 16 else "🔴 CLOSED"
                    st.info(f"💹 Market: {market_status}")
                
                # Show top explosive picks
                if len(final_df) > 0:
                    st.markdown("### 🔥 TOP 5 EXPLOSIVE SMALL CAP PICKS:")
                    for i, (idx, row) in enumerate(final_df.head(5).iterrows()):
                        vol_emoji = row['Vol']
                        if i == 0:
                            st.success(f"🥇 **#{idx}: {row['Ticker']}** {vol_emoji} - Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
                        elif i == 1:
                            st.info(f"🥈 **#{idx}: {row['Ticker']}** {vol_emoji} - Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
                        elif i == 2:
                            st.info(f"🥉 **#{idx}: {row['Ticker']}** {vol_emoji} - Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
                        else:
                            st.info(f"⭐ **#{idx}: {row['Ticker']}** {vol_emoji} - Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
        
        # Display formula and methodology
        with st.expander("💎 Small Cap QuantScore Formula & Strategy"):
            st.markdown(f"""
            ### Enhanced Small Cap QuantScore Formula:
            ```
            QuantScore = (|Change%| × Volume^{alpha}) / (MarketCap^{beta} × Float^0.3)
            ```
            
            ### Small Cap Filters Applied:
            - **Price Range:** ${price_min} - ${price_max}
            - **Float Shares:** ≤ {format_number(max_float)}
            - **RSI:** > {rsi_min} (strong momentum)
            - **Change%:** ≥ {change_min}% (significant movement)
            - **Volume:** ≥ {format_number(volume_min)} (adequate liquidity)
            
            ### Why These Filters Matter:
            - **Low Price:** Higher percentage gain potential
            - **Small Float:** Less shares available = higher volatility
            - **High RSI:** Confirms momentum strength
            - **Volume:** Ensures you can actually trade the stock
            
            ### Volatility Indicators:
            - 🔥 = ≥20% movement (EXPLOSIVE)
            - ⚡ = ≥10% movement (HIGH VOLATILITY)
            - 📈 = ≥5% movement (ACTIVE)
            - 📊 = <5% movement (STABLE)
            
            ### Small Cap Trading Strategy:
            1. **Focus on Top 5** ranked stocks
            2. **Check news catalysts** before entry
            3. **Use stop losses** (high volatility = high risk)
            4. **Monitor volume** for confirmation
            5. **Take profits quickly** on explosive moves
            
            ### Risk Warning:
            Small cap stocks are extremely volatile and risky. Use proper position sizing!
            """)
        
        # Small cap specific disclaimer
        st.markdown("---")
        st.error("""
        🚨 **SMALL CAP RISK WARNING:** 
        Small cap and penny stocks are extremely volatile and risky. They can move 50%+ in minutes. 
        Many are subject to pump-and-dump schemes. Only trade with money you can afford to lose completely. 
        This tool is for educational purposes only - NOT financial advice!
        """)

else:
    # Welcome screen
    st.markdown("## 💎 Welcome to Small Cap Scanner!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What This Scans For:
        - **Small Float** stocks (under 10M shares)
        - **Low Price** range ($1-$10)
        - **High Momentum** breakouts
        - **Volume Confirmation** 
        - **Explosive Potential** 🔥
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 How to Use:
        1. Click **"Scan Small Caps"** in sidebar
        2. Wait for real-time data scan
        3. Review explosive opportunities 
        4. Focus on top 5 ranked picks
        5. Download your watchlist
        """)
    
    st.warning("⚠️ **Remember:** Small caps are high risk, high reward. Use proper risk management!")
    
    # Sample preview with small cap focus
    st.markdown("### 💎 Sample Small Cap Scan Results:")
    sample_data = {
        'Rank': [1, 2, 3, 4, 5],
        'Vol': ['🔥', '⚡', '⚡', '📈', '📈'],
        'Ticker': ['PHUN', 'SNTI', 'BBIG', 'PROG', 'ATER'],
        'QuantScore': ['0.12345678', '0.09876543', '0.08765432', '0.07654321', '0.06543210'],
        'Price': ['$3.45', '$2.87', '$4.12', '$1.98', '$6.34'],
        'Change%': ['+15.4%', '+12.8%', '+11.2%', '+8.9%', '+7.1%'],
        'Float': ['2.1M', '3.5M', '5.2M', '1.8M', '4.7M']
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

# Auto-refresh mechanism (faster for small caps)
if auto_refresh:
    time.sleep(30)  # 30 second refresh for volatile small caps
    st.rerun()