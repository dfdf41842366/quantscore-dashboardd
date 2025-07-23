import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="QuantScore™ Live Dashboard",
    page_icon="🚀",
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
</style>
""", unsafe_allow_html=True)

st.title("🚀 QuantScore™ Live Dashboard")
st.markdown("**Real-time stock screening for high-momentum breakout opportunities**")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Default tickers
default_tickers = [
    "AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "META", "AMZN",
    "NFLX", "CRM", "ADBE", "PYPL", "SQ", "ROKU", "ZM", "SHOP",
    "PLTR", "RBLX", "U", "NET", "SNOW", "CRWD", "ZS", "OKTA"
]

ticker_input = st.sidebar.text_area(
    "📈 Stock Tickers (one per line)",
    value="\n".join(default_tickers[:12]),
    height=200,
    help="Enter stock symbols like AAPL, TSLA, NVDA"
)

# Parse tickers
tickers = [t.strip().upper() for t in ticker_input.split('\n') if t.strip()]

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Formula Parameters")
alpha = st.sidebar.slider("Alpha (Volume exponent)", 0.5, 2.0, 1.3, 0.1)
beta = st.sidebar.slider("Beta (MarketCap exponent)", 0.3, 1.5, 0.7, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Quality Filters")
rsi_min = st.sidebar.slider("Minimum RSI", 30, 80, 55, 5)
change_min = st.sidebar.slider("Minimum Change %", 0.0, 10.0, 2.0, 0.5)
max_float = st.sidebar.selectbox(
    "Maximum Float Shares",
    [5_000_000, 10_000_000, 20_000_000, 50_000_000, 100_000_000],
    index=4
)

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (60s)", value=False)

def calculate_simple_rsi(prices, window=14):
    """Calculate RSI without external library"""
    if len(prices) < window + 1:
        return 50  # Default value
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_stock_data(ticker):
    """Get stock data for a single ticker"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get current data
        hist = stock.history(period="30d", interval="1d")
        if hist.empty or len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        
        # Get additional info
        info = stock.info
        
        # Calculate metrics
        change_pct = ((current_price - prev_close) / prev_close) * 100
        volume = hist['Volume'].iloc[-1]
        market_cap = info.get('marketCap', 0)
        float_shares = info.get('floatShares', info.get('sharesOutstanding', 0))
        
        # Calculate gap percentage (simplified as daily change)
        gap_pct = change_pct
        
        # Calculate RSI
        rsi = calculate_simple_rsi(hist['Close'])
        
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
        st.warning(f"⚠️ Could not fetch data for {ticker}")
        return None

def calculate_quant_score(data, alpha, beta):
    """Calculate QuantScore using the proprietary formula"""
    try:
        change_pct = abs(data['change_pct'])  # Use absolute value for momentum
        volume = data['volume']
        market_cap = data['market_cap']
        
        if market_cap <= 0 or volume <= 0:
            return 0
        
        # QuantScore = (Change% × Volume^alpha) / (MarketCap^beta)
        score = (change_pct * (volume ** alpha)) / (market_cap ** beta)
        return score
    except:
        return 0

def apply_filters(df, rsi_min, change_min, max_float):
    """Apply quality filters to the dataset"""
    filtered = df[
        (df['float_shares'] < max_float) &
        (df['rsi'] > rsi_min) &
        (df['change_pct'].abs() > change_min) &
        (df['quant_score'] > 0)
    ].copy()
    
    return filtered.sort_values('quant_score', ascending=False)

def format_number(num, is_currency=False, is_percentage=False):
    """Format numbers for display"""
    if pd.isna(num) or num == 0:
        return "N/A"
    
    if is_percentage:
        return f"{num:.2f}%"
    elif is_currency:
        return f"${num:.2f}"
    elif num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif num >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"

# Main analysis
if st.sidebar.button("🚀 Run QuantScore Analysis", type="primary") or auto_refresh:
    if not tickers:
        st.error("❌ Please enter at least one ticker symbol")
    else:
        st.markdown("---")
        
        # Show current time
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"🕐 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
        with col2:
            st.info(f"📊 **Analyzing:** {len(tickers)} stocks")
        with col3:
            st.info(f"🔍 **Float Limit:** {format_number(max_float)}")
        
        # Fetch data
        with st.spinner("🔄 Fetching real-time market data..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for i, ticker in enumerate(tickers):
                status_text.text(f'Fetching data for {ticker}...')
                progress_bar.progress((i + 1) / len(tickers))
                
                data = get_stock_data(ticker)
                if data:
                    quant_score = calculate_quant_score(data, alpha, beta)
                    data['quant_score'] = quant_score
                    results.append(data)
                
                time.sleep(0.1)  # Small delay
            
            progress_bar.empty()
            status_text.empty()
        
        if not results:
            st.error("❌ No data retrieved. Please check your ticker symbols and try again.")
            st.info("💡 Try popular stocks like: AAPL, TSLA, NVDA, MSFT")
        else:
            df = pd.DataFrame(results)
            
            # Apply filters
            filtered_df = apply_filters(df, rsi_min, change_min, max_float)
            
            # Display summary metrics
            st.markdown("## 📈 Summary Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Stocks Analyzed",
                    value=len(df),
                    delta=f"{len(filtered_df)} passed filters"
                )
            
            with col2:
                if not filtered_df.empty:
                    avg_score = filtered_df['quant_score'].mean()
                    st.metric(
                        label="Avg QuantScore",
                        value=f"{avg_score:.6f}",
                        delta=f"Max: {filtered_df['quant_score'].max():.6f}"
                    )
                else:
                    st.metric("Avg QuantScore", "N/A")
            
            with col3:
                if not filtered_df.empty:
                    avg_rsi = filtered_df['rsi'].mean()
                    st.metric(
                        label="Avg RSI",
                        value=f"{avg_rsi:.1f}",
                        delta=f"Range: {filtered_df['rsi'].min():.1f}-{filtered_df['rsi'].max():.1f}"
                    )
                else:
                    st.metric("Avg RSI", "N/A")
            
            with col4:
                if not filtered_df.empty:
                    avg_change = filtered_df['change_pct'].mean()
                    st.metric(
                        label="Avg Change %",
                        value=f"{avg_change:.2f}%",
                        delta=f"Max: {filtered_df['change_pct'].max():.2f}%"
                    )
                else:
                    st.metric("Avg Change %", "N/A")
            
            # Display results
            st.markdown("## 🏆 Top QuantScore Rankings")
            
            if filtered_df.empty:
                st.warning("⚠️ No stocks passed the quality filters. Showing all analyzed stocks below.")
                st.info("💡 Try lowering the RSI minimum or Change minimum to see more results.")
                display_df = df.sort_values('quant_score', ascending=False)
            else:
                st.success(f"✅ Found {len(filtered_df)} high-quality opportunities!")
                display_df = filtered_df
            
            # Format the display dataframe
            display_formatted = display_df.copy()
            display_formatted['quant_score'] = display_formatted['quant_score'].apply(lambda x: f"{x:.8f}")
            display_formatted['current_price'] = display_formatted['current_price'].apply(lambda x: format_number(x, is_currency=True))
            display_formatted['change_pct'] = display_formatted['change_pct'].apply(lambda x: format_number(x, is_percentage=True))
            display_formatted['volume'] = display_formatted['volume'].apply(format_number)
            display_formatted['market_cap'] = display_formatted['market_cap'].apply(format_number)
            display_formatted['float_shares'] = display_formatted['float_shares'].apply(format_number)
            display_formatted['rsi'] = display_formatted['rsi'].apply(lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A")
            
            # Rename columns for display
            display_formatted.columns = [
                'Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 
                'Market Cap', 'Float Shares', 'Gap%', 'RSI', 'Last Updated'
            ]
            
            # Select columns for display
            final_columns = ['Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 'Market Cap', 'RSI']
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
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"quantscore_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                if st.button("🔄 Refresh Data"):
                    st.cache_data.clear()
                    st.rerun()
            
            with col3:
                current_hour = datetime.now().hour
                market_status = "🟢 OPEN" if 9 <= current_hour <= 16 else "🔴 CLOSED"
                st.info(f"💹 Market: {market_status}")
            
            # Show top picks
            if len(final_df) > 0:
                st.markdown("### 🎯 Top 3 Picks:")
                for i, (idx, row) in enumerate(final_df.head(3).iterrows()):
                    st.success(f"**#{idx}: {row['Ticker']}** - QuantScore: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']}")
        
        # Display formula and methodology
        with st.expander("🧮 QuantScore Formula & Methodology"):
            st.markdown(f"""
            ### QuantScore Formula:
            ```
            QuantScore = (|Change%| × Volume^{alpha}) / (MarketCap^{beta})
            ```
            
            ### Quality Filters Applied:
            - **Float Shares:** < {format_number(max_float)} shares
            - **RSI:** > {rsi_min} (momentum indicator)
            - **Change%:** > {change_min}% (movement threshold)
            - **Volume:** > 0 (active trading)
            
            ### How to Read Results:
            - **Higher QuantScore** = Better opportunity
            - **Rank 1** = Best pick according to the formula
            - **Focus on top 5-10** ranked stocks
            
            ### Data Sources:
            - Yahoo Finance API (real-time quotes)
            - Built-in RSI calculations
            - Market data updated every 60 seconds
            
            ### Best Practices:
            - Use during market hours (9:30 AM - 4:00 PM EST)
            - Combine with your own research
            - Monitor for volume confirmation
            """)
        
        # Trading disclaimer
        st.markdown("---")
        st.warning("⚠️ **Disclaimer:** This tool is for educational and informational purposes only. Not financial advice. Always do your own research before making investment decisions.")

else:
    # Welcome screen when no analysis is running
    st.markdown("## 👋 Welcome to QuantScore™!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What This Does:
        - **Ranks stocks** by breakout potential
        - **Real-time analysis** using quantitative formula
        - **Quality filters** for high-momentum picks
        - **Visual analytics** and data export
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 How to Start:
        1. Click **"Run QuantScore Analysis"** in sidebar
        2. Wait for data to load (30-60 seconds)
        3. Review ranked results
        4. Export your picks as CSV
        """)
    
    st.info("💡 **Tip:** Enable auto-refresh to keep data current during market hours!")
    
    # Sample preview
    st.markdown("### 📈 Sample Analysis Preview:")
    sample_data = {
        'Rank': [1, 2, 3, 4, 5],
        'Ticker': ['TSLA', 'NVDA', 'AMD', 'AAPL', 'MSFT'],
        'QuantScore': ['0.00123456', '0.00098765', '0.00087654', '0.00076543', '0.00065432'],
        'Price': ['$245.67', '$892.34', '$178.90', '$189.45', '$367.12'],
        'Change%': ['+3.45%', '+2.87%', '+4.12%', '+1.98%', '+2.34%'],
        'RSI': ['67.8', '59.3', '71.2', '56.7', '62.1']
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

# Auto-refresh mechanism
if auto_refresh:
    time.sleep(60)
    st.rerun()
