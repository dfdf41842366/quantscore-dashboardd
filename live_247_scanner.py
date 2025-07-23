import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import pytz

# Configure page
st.set_page_config(
    page_title="💎 24/7 Live Small Cap Scanner",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for live trading feel
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .live-indicator {
        background: linear-gradient(90deg, #00ff00, #32cd32);
        padding: 0.5rem;
        border-radius: 0.25rem;
        color: black;
        font-weight: bold;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .session-indicator {
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem 0;
    }
    .pre-market { background-color: #ff9800; color: white; }
    .regular-hours { background-color: #4caf50; color: white; }
    .after-hours { background-color: #2196f3; color: white; }
    .overnight { background-color: #9c27b0; color: white; }
    .stMetric {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Set timezone
ET = pytz.timezone('US/Eastern')
current_time = datetime.now(ET)

def get_trading_session():
    """Determine current trading session"""
    now = datetime.now(ET)
    hour = now.hour
    minute = now.minute
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    # Weekend
    if weekday >= 5:  # Saturday=5, Sunday=6
        return "WEEKEND", "🏠"
    
    # Weekday sessions
    if hour < 4:
        return "OVERNIGHT", "🌙"
    elif 4 <= hour < 9 or (hour == 9 and minute < 30):
        return "PRE-MARKET", "🌅"
    elif (hour == 9 and minute >= 30) or (10 <= hour < 16):
        return "REGULAR HOURS", "🔔"
    elif 16 <= hour < 20:
        return "AFTER-HOURS", "🌆"
    else:
        return "OVERNIGHT", "🌙"

session, session_emoji = get_trading_session()

# Header with live indicator
st.markdown(f"""
<div class="live-indicator">
🌍 LIVE 24/7 SMALL CAP SCANNER - {session} {session_emoji} - {current_time.strftime('%Y-%m-%d %H:%M:%S ET')}
</div>
""", unsafe_allow_html=True)

st.title("💎 Live Small Cap Breakout Scanner")
st.markdown("**🚀 Real-time data across ALL trading sessions | Pre-Market | Regular | After-Hours | Overnight**")

# Display current session prominently
session_class = session.lower().replace(" ", "-").replace("-", "_")
if session == "PRE-MARKET":
    session_class = "pre_market"
elif session == "REGULAR HOURS":
    session_class = "regular_hours"
elif session == "AFTER-HOURS":
    session_class = "after_hours"
elif session == "OVERNIGHT":
    session_class = "overnight"

st.markdown(f"""
<div class="session-indicator {session_class}">
{session_emoji} CURRENT SESSION: {session} | Updates Every 15 Seconds
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header(f"💎 Live Scanner Settings")

# Extended hours small cap tickers
small_cap_tickers = [
    # High-volume small caps with extended trading
    "PHUN", "SNTI", "HUBC", "BBIG", "PROG", "ATER", "SPRT", "IRNT",
    "RDBX", "NILE", "MULN", "GFAI", "BMRA", "RELI", "BGFV", "CLOV",
    "WISH", "WKHS", "RIDE", "GOEV", "ARVL", "NAKD", "SNDL", "EXPR",
    "AMC", "GME", "MMAT", "TRCH", "VERB", "VXRT", "OCGN", "XELA",
    "GNUS", "JAGX", "INPX", "MARK", "UAMY", "TOPS", "SHIP", "GLBS",
    # Add some liquid small caps for extended hours
    "SOFI", "PLTR", "HOOD", "RBLX", "DKNG", "FUBO", "SKLZ", "OPEN"
]

ticker_input = st.sidebar.text_area(
    "💎 Live Tickers (one per line)",
    value="\n".join(small_cap_tickers[:20]),
    height=300,
    help="Enter tickers with extended hours trading"
)

# Parse tickers
tickers = [t.strip().upper() for t in ticker_input.split('\n') if t.strip()]

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Live Formula Settings")
alpha = st.sidebar.slider("Alpha (Volume weight)", 1.0, 2.5, 1.5, 0.1)
beta = st.sidebar.slider("Beta (Market cap weight)", 0.3, 1.0, 0.5, 0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("💎 Live Filters")
price_min = st.sidebar.slider("Min Price ($)", 0.50, 5.0, 1.0, 0.25)
price_max = st.sidebar.slider("Max Price ($)", 2.0, 20.0, 10.0, 0.50)
change_min = st.sidebar.slider("Min Change %", 1.0, 15.0, 3.0, 0.5)
volume_min = st.sidebar.selectbox(
    "Min Volume",
    [50_000, 100_000, 250_000, 500_000, 1_000_000],
    index=2
)
max_float = st.sidebar.selectbox(
    "Max Float",
    [2_000_000, 5_000_000, 10_000_000, 20_000_000],
    index=2
)

# Live update settings
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Live Updates")
auto_refresh = st.sidebar.checkbox("🔴 LIVE MODE (15s refresh)", value=True)
refresh_rate = st.sidebar.selectbox("Refresh Rate", [10, 15, 30, 60], index=1)

# Show extended hours capability
st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Trading Sessions Covered")
st.sidebar.success("✅ Pre-Market (4:00-9:30 AM)")
st.sidebar.success("✅ Regular Hours (9:30-4:00 PM)")  
st.sidebar.success("✅ After-Hours (4:00-8:00 PM)")
st.sidebar.info("🌙 Overnight (Limited Data)")

def get_live_stock_data(ticker):
    """Get comprehensive live stock data including extended hours"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get multiple periods for comprehensive data
        hist_1d = stock.history(period="1d", interval="1m", prepost=True)  # Extended hours
        hist_5d = stock.history(period="5d", interval="1d", prepost=True)
        
        if hist_1d.empty and hist_5d.empty:
            return None
        
        # Use 1-minute data if available, fall back to daily
        if not hist_1d.empty:
            current_price = hist_1d['Close'].iloc[-1]
            current_volume = hist_1d['Volume'].iloc[-1]
            
            # Calculate intraday change
            if len(hist_5d) >= 2:
                prev_close = hist_5d['Close'].iloc[-2]
                change_pct = ((current_price - prev_close) / prev_close) * 100
            else:
                change_pct = 0
                
            # Get today's open for gap calculation
            today_open = hist_1d['Open'].iloc[0] if not hist_1d.empty else current_price
            gap_pct = ((today_open - prev_close) / prev_close) * 100 if len(hist_5d) >= 2 else 0
            
        else:
            # Fall back to daily data
            current_price = hist_5d['Close'].iloc[-1]
            current_volume = hist_5d['Volume'].iloc[-1]
            
            if len(hist_5d) >= 2:
                prev_close = hist_5d['Close'].iloc[-2]
                change_pct = ((current_price - prev_close) / prev_close) * 100
                gap_pct = change_pct
            else:
                change_pct = 0
                gap_pct = 0
        
        # Get company info with error handling
        try:
            info = stock.info
            market_cap = info.get('marketCap', 0)
            float_shares = info.get('floatShares', info.get('sharesOutstanding', 0))
            
            # Fallback calculations if info fails
            if market_cap == 0:
                shares_outstanding = info.get('sharesOutstanding', 50000000)
                market_cap = current_price * shares_outstanding
                
            if float_shares == 0:
                float_shares = market_cap / current_price * 0.8  # Estimate 80% float
                
        except:
            # Emergency fallbacks for live trading
            estimated_shares = 50000000  # 50M shares estimate
            market_cap = current_price * estimated_shares
            float_shares = estimated_shares * 0.7  # 70% float estimate
        
        # Calculate simple RSI from available data
        if len(hist_5d) >= 14:
            closes = hist_5d['Close']
            delta = closes.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_series = 100 - (100 / (1 + rs))
            rsi = rsi_series.iloc[-1] if not pd.isna(rsi_series.iloc[-1]) else 50
        else:
            rsi = 50
        
        # Extended hours detection
        now = datetime.now(ET)
        is_extended_hours = session in ["PRE-MARKET", "AFTER-HOURS"]
        
        return {
            'ticker': ticker,
            'current_price': float(current_price),
            'change_pct': float(change_pct),
            'volume': int(current_volume) if current_volume > 0 else 1,
            'market_cap': int(market_cap) if market_cap > 0 else 1000000,
            'float_shares': int(float_shares) if float_shares > 0 else 1000000,
            'gap_pct': float(gap_pct),
            'rsi': float(rsi),
            'session': session,
            'is_extended_hours': is_extended_hours,
            'last_updated': datetime.now(ET),
            'data_timestamp': hist_1d.index[-1] if not hist_1d.empty else hist_5d.index[-1]
        }
        
    except Exception as e:
        # Return None for failed tickers to skip them
        return None

@st.cache_data(ttl=15)  # 15-second cache for live data
def get_live_market_data(tickers_list):
    """Get live market data for all tickers"""
    results = {}
    
    for ticker in tickers_list:
        data = get_live_stock_data(ticker)
        if data:
            results[ticker] = data
    
    return results

def calculate_live_quant_score(data, alpha, beta):
    """Calculate live QuantScore with extended hours weighting"""
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        float_shares = data['float_shares']
        
        if market_cap <= 0 or volume <= 0 or float_shares <= 0:
            return 0
        
        # Base formula with float factor
        base_score = (change_pct * (volume ** alpha)) / ((market_cap ** beta) * (float_shares ** 0.3))
        
        # Extended hours bonus (lower volume, higher significance)
        if data['is_extended_hours']:
            extended_hours_multiplier = 1.5  # 50% bonus for extended hours moves
            base_score *= extended_hours_multiplier
        
        return base_score
        
    except:
        return 0

def apply_live_filters(df, price_min, price_max, change_min, volume_min, max_float):
    """Apply live trading filters"""
    try:
        filtered = df[
            (df['current_price'] >= price_min) &
            (df['current_price'] <= price_max) &
            (df['float_shares'] <= max_float) &
            (df['change_pct'].abs() >= change_min) &
            (df['volume'] >= volume_min) &
            (df['quant_score'] > 0)
        ].copy()
        
        return filtered.sort_values('quant_score', ascending=False)
    except:
        return df.sort_values('quant_score', ascending=False)

def format_live_number(num, is_currency=False, is_percentage=False):
    """Format numbers for live display"""
    try:
        if pd.isna(num) or num == 0:
            return "N/A"
        
        if is_percentage:
            color = "green" if num > 0 else "red"
            return f"<span style='color: {color}'>{num:+.2f}%</span>"
        elif is_currency:
            return f"${num:.3f}" if num < 10 else f"${num:.2f}"
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

def get_momentum_indicator(change_pct, session):
    """Get momentum indicator with session context"""
    abs_change = abs(change_pct)
    
    if session in ["PRE-MARKET", "AFTER-HOURS"]:
        # Lower thresholds for extended hours
        if abs_change >= 15:
            return "🚀"
        elif abs_change >= 8:
            return "🔥"
        elif abs_change >= 4:
            return "⚡"
        elif abs_change >= 2:
            return "📈"
        else:
            return "📊"
    else:
        # Regular hours thresholds
        if abs_change >= 25:
            return "🚀"
        elif abs_change >= 15:
            return "🔥"
        elif abs_change >= 8:
            return "⚡"
        elif abs_change >= 3:
            return "📈"
        else:
            return "📊"

# Live scanner execution
if st.sidebar.button("🔴 START LIVE SCAN", type="primary") or auto_refresh:
    if not tickers:
        st.error("❌ Please enter at least one ticker symbol")
    else:
        st.markdown("---")
        
        # Live status display
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("🕐 Live Time", current_time.strftime('%H:%M:%S'))
        with col2:
            st.metric("📡 Session", f"{session_emoji} {session}")
        with col3:
            st.metric("🎯 Scanning", f"{len(tickers)} tickers")
        with col4:
            st.metric("💰 Price Range", f"${price_min}-${price_max}")
        with col5:
            st.metric("🔄 Refresh", f"{refresh_rate}s")
        
        # Live data fetch
        with st.spinner(f"🔴 LIVE SCANNING {session}..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            stock_data = {}
            
            for i, ticker in enumerate(tickers):
                status_text.text(f'🔴 LIVE: Scanning {ticker}... ({session})')
                progress_bar.progress((i + 1) / len(tickers))
                
                data = get_live_stock_data(ticker)
                if data:
                    stock_data[ticker] = data
                
                # Very fast scanning for live feel
                time.sleep(0.02)
            
            scan_time = time.time() - start_time
            progress_bar.empty()
            status_text.empty()
        
        if not stock_data:
            st.error("❌ No live data retrieved. Market may be closed or connection issues.")
            st.info("🔄 Trying again in a few seconds...")
        else:
            # Calculate live QuantScores
            results = []
            for ticker, data in stock_data.items():
                quant_score = calculate_live_quant_score(data, alpha, beta)
                
                results.append({
                    'ticker': ticker,
                    'quant_score': quant_score,
                    'current_price': data['current_price'],
                    'change_pct': data['change_pct'],
                    'volume': data['volume'],
                    'market_cap': data['market_cap'],
                    'float_shares': data['float_shares'],
                    'gap_pct': data['gap_pct'],
                    'rsi': data['rsi'],
                    'session': data['session'],
                    'is_extended_hours': data['is_extended_hours'],
                    'data_age': (datetime.now(ET) - data['data_timestamp']).total_seconds() / 60
                })
            
            df = pd.DataFrame(results)
            
            if df.empty:
                st.error("❌ No valid live data found.")
            else:
                # Apply live filters
                filtered_df = apply_live_filters(df, price_min, price_max, change_min, volume_min, max_float)
                
                # Live summary metrics
                st.markdown(f"## 🔴 LIVE {session} SCANNER RESULTS")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    st.metric("📊 Total Scanned", len(df))
                
                with col2:
                    st.metric("🎯 Qualified", len(filtered_df))
                
                with col3:
                    if not filtered_df.empty:
                        avg_change = filtered_df['change_pct'].mean()
                        max_change = filtered_df['change_pct'].max()
                        st.metric("📈 Avg Change", f"{avg_change:.1f}%", f"Max: {max_change:.1f}%")
                    else:
                        st.metric("📈 Avg Change", "N/A")
                
                with col4:
                    if not filtered_df.empty:
                        total_volume = filtered_df['volume'].sum()
                        st.metric("🔊 Total Volume", format_live_number(total_volume))
                    else:
                        st.metric("🔊 Total Volume", "N/A")
                
                with col5:
                    extended_count = len(df[df['is_extended_hours']])
                    st.metric("🌅 Extended Hours", f"{extended_count}/{len(df)}")
                
                with col6:
                    st.metric("⚡ Scan Time", f"{scan_time:.1f}s")
                
                # Live results table
                st.markdown(f"## 🚀 LIVE {session} BREAKOUT ALERTS")
                
                if filtered_df.empty:
                    st.warning("⚠️ No stocks meet current criteria. Showing top unfiltered results:")
                    display_df = df.sort_values('quant_score', ascending=False).head(15)
                else:
                    st.success(f"🎯 {len(filtered_df)} LIVE opportunities detected!")
                    display_df = filtered_df.head(20)  # Top 20 for live trading
                
                # Format live display
                display_formatted = display_df.copy()
                display_formatted['momentum'] = display_formatted.apply(lambda row: get_momentum_indicator(row['change_pct'], row['session']), axis=1)
                display_formatted['session_icon'] = display_formatted['session'].map({
                    'PRE-MARKET': '🌅',
                    'REGULAR HOURS': '🔔', 
                    'AFTER-HOURS': '🌆',
                    'OVERNIGHT': '🌙',
                    'WEEKEND': '🏠'
                })
                
                # Format numbers
                display_formatted['quant_score'] = display_formatted['quant_score'].apply(lambda x: f"{x:.8f}")
                display_formatted['current_price'] = display_formatted['current_price'].apply(lambda x: format_live_number(x, is_currency=True))
                display_formatted['change_pct'] = display_formatted['change_pct'].apply(lambda x: format_live_number(x, is_percentage=True))
                display_formatted['volume'] = display_formatted['volume'].apply(format_live_number)
                display_formatted['market_cap'] = display_formatted['market_cap'].apply(format_live_number)
                display_formatted['float_shares'] = display_formatted['float_shares'].apply(format_live_number)
                display_formatted['gap_pct'] = display_formatted['gap_pct'].apply(lambda x: format_live_number(x, is_percentage=True))
                display_formatted['rsi'] = display_formatted['rsi'].apply(lambda x: f"{x:.0f}")
                display_formatted['data_age'] = display_formatted['data_age'].apply(lambda x: f"{x:.1f}m")
                
                # Select columns for live display
                live_columns = ['momentum', 'session_icon', 'ticker', 'quant_score', 'current_price', 'change_pct', 'volume', 'float_shares', 'gap_pct', 'rsi', 'data_age']
                final_df = display_formatted[live_columns].copy()
                final_df.columns = ['🔥', '📅', 'Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 'Float', 'Gap%', 'RSI', 'Age']
                
                # Add ranking
                final_df.index = range(1, len(final_df) + 1)
                final_df.index.name = 'Rank'
                
                # Display live table
                st.dataframe(
                    final_df,
                    use_container_width=True,
                    height=500
                )
                
                # Live action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    csv = final_df.to_csv()
                    st.download_button(
                        label="📊 Download Live Data",
                        data=csv,
                        file_name=f"live_scan_{session.lower()}_{datetime.now(ET).strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    if st.button("🔄 Refresh Now"):
                        st.cache_data.clear()
                        st.rerun()
                
                with col3:
                    next_refresh = refresh_rate if auto_refresh else "Manual"
                    st.info(f"⏱️ Next: {next_refresh}s")
                
                with col4:
                    live_count = len([x for x in stock_data.values() if (datetime.now(ET) - x['data_timestamp']).total_seconds() < 300])
                    st.metric("🔴 Live Data", f"{live_count}/{len(stock_data)}")
                
                # Live alerts for top picks
                if len(final_df) > 0:
                    st.markdown(f"### 🚨 TOP 5 LIVE {session} ALERTS:")
                    for i, (idx, row) in enumerate(final_df.head(5).iterrows()):
                        momentum = row['🔥']
                        session_icon = row['📅']
                        
                        if i == 0:
                            st.success(f"🥇 **#{idx}: {row['Ticker']}** {momentum} {session_icon} | Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
                        else:
                            priority = "🥈" if i == 1 else "🥉" if i == 2 else "⭐"
                            st.info(f"{priority} **#{idx}: {row['Ticker']}** {momentum} {session_icon} | Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float']}")
        
        # Live methodology
        with st.expander("🔴 Live Trading Methodology & Sessions"):
            st.markdown(f"""
            ### 🌍 24/7 Live QuantScore Formula:
            ```
            QuantScore = (|Change%| × Volume^{alpha}) / (MarketCap^{beta} × Float^0.3)
            Extended Hours Bonus: +50% multiplier for pre/after market moves
            ```
            
            ### 📅 Trading Sessions Covered:
            - **🌅 PRE-MARKET (4:00-9:30 AM ET):** Lower volume, higher impact moves
            - **🔔 REGULAR HOURS (9:30-4:00 PM ET):** Full liquidity and volume
            - **🌆 AFTER-HOURS (4:00-8:00 PM ET):** Earnings reactions, news catalysts
            - **🌙 OVERNIGHT (8:00 PM-4:00 AM ET):** Limited data, futures impact
            - **🏠 WEEKEND:** No trading, analysis mode
            
            ### 🔄 Live Data Sources:
            - **1-minute intervals** during market hours
            - **Extended hours data** included
            - **Real-time price updates** every 15 seconds
            - **Volume and gap tracking** across sessions
            
            ### 🎯 Live Trading Strategy:
            1. **Monitor top 5** ranked stocks continuously
            2. **Watch for session transitions** (gaps at open/close)
            3. **Volume confirmation** especially in extended hours
            4. **News catalyst awareness** for breakouts
            5. **Quick profit taking** on explosive moves
            
            ### ⚠️ Extended Hours Risks:
            - **Lower liquidity** = wider spreads
            - **Higher volatility** = bigger moves
            - **News sensitivity** = overnight gaps
            - **Limited participants** = price manipulation risk
            """)
        
        # Live trading disclaimer
        st.markdown("---")
        st.error(f"""
        🚨 **LIVE TRADING RISK WARNING ({session}):** 
        This is LIVE market data for active trading. Small cap stocks are extremely volatile, especially during 
        extended hours. Prices can move 50%+ instantly on news. Use proper risk management, stop losses, and 
        position sizing. Extended hours trading has additional risks including low liquidity and wide spreads.
        This tool provides data only - NOT trading advice!
        """)

else:
    # Live welcome screen
    st.markdown("## 🔴 Welcome to 24/7 Live Scanner!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌍 Live Coverage:
        - **🌅 Pre-Market** (4:00-9:30 AM ET)
        - **🔔 Regular Hours** (9:30-4:00 PM ET)  
        - **🌆 After-Hours** (4:00-8:00 PM ET)
        - **🌙 Overnight** (Limited data)
        - **🔄 15-second** live updates
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Live Features:
        - **Real-time data** across all sessions
        - **Extended hours** volume tracking
        - **Live momentum** indicators
        - **Instant alerts** for breakouts
        - **Session-specific** filtering
        """)
    
    st.info(f"🔴 **LIVE STATUS:** Currently {session} {session_emoji} | Ready for live scanning!")
    
    # Live sample with session indicators
    st.markdown("### 🔴 Live Scanner Sample:")
    sample_data = {
        'Rank': [1, 2, 3, 4, 5],
        '🔥': ['🚀', '🔥', '⚡', '📈', '📊'],
        '📅': ['🌅', '🌅', '🔔', '🌆', '🌆'],
        'Ticker': ['PHUN', 'SNTI', 'BBIG', 'PROG', 'ATER'],
        'QuantScore': ['0.12345678', '0.09876543', '0.08765432', '0.07654321', '0.06543210'],
        'Price': ['$3.45', '$2.87', '$4.12', '$1.98', '$6.34'],
        'Change%': ['+18.4%', '+12.8%', '+8.2%', '+5.9%', '+4.1%'],
        'Session': ['PRE', 'PRE', 'REG', 'AH', 'AH']
    }
    st.dataframe(pd.DataFrame(sample_data), use_container_width=True)

# Auto-refresh for live mode
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()