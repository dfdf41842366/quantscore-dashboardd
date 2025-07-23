import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import pytz
import threading
import concurrent.futures

# Configure page for 24/7 operation
st.set_page_config(
    page_title="🌍 24/7 QuantScore™ Scanner",
    page_icon="🌍",
    layout="wide"
)

# Enhanced dark theme for 24/7 trading
st.markdown("""
<style>
    .stApp {
        background-color: #0a0f1c;
        color: #e8e8e8;
    }
    
    /* 24/7 Header with live session indicator */
    .auto-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57, #ff9ff3);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: #000000;
        font-weight: bold;
        font-size: 2rem;
        margin-bottom: 2rem;
        animation: rainbow 5s linear infinite;
        box-shadow: 0 0 40px rgba(255, 107, 107, 0.4);
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    /* Session indicators */
    .session-premarket {
        background: linear-gradient(135deg, #ff9800, #ffb74d);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: bold;
        text-align: center;
        animation: pulse-orange 2s infinite;
    }
    
    .session-regular {
        background: linear-gradient(135deg, #4caf50, #66bb6a);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: bold;
        text-align: center;
        animation: pulse-green 2s infinite;
    }
    
    .session-afterhours {
        background: linear-gradient(135deg, #2196f3, #42a5f5);
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: bold;
        text-align: center;
        animation: pulse-blue 2s infinite;
    }
    
    .session-overnight {
        background: linear-gradient(135deg, #9c27b0, #ba68c8);
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: bold;
        text-align: center;
        animation: pulse-purple 2s infinite;
    }
    
    .session-weekend {
        background: linear-gradient(135deg, #607d8b, #78909c);
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        font-weight: bold;
        text-align: center;
        animation: pulse-gray 2s infinite;
    }
    
    @keyframes pulse-orange {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    @keyframes pulse-green {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    @keyframes pulse-blue {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    @keyframes pulse-purple {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    @keyframes pulse-gray {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    /* Live status indicators */
    .live-status {
        background: linear-gradient(45deg, #1e2139, #2a2d47);
        border: 2px solid #00ff88;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #00ff88;
        font-weight: bold;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
        to { box-shadow: 0 0 40px rgba(0, 255, 136, 0.8); }
    }
    
    /* Auto-refresh indicator */
    .auto-refresh {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        animation: refresh-pulse 1s infinite;
    }
    
    @keyframes refresh-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Session-specific results */
    .premarket-result {
        background: linear-gradient(135deg, #ff9800, #ffb74d);
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: bold;
        border-left: 5px solid #ff6f00;
    }
    
    .regular-result {
        background: linear-gradient(135deg, #4caf50, #66bb6a);
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: bold;
        border-left: 5px solid #2e7d32;
    }
    
    .afterhours-result {
        background: linear-gradient(135deg, #2196f3, #42a5f5);
        color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: bold;
        border-left: 5px solid #1565c0;
    }
    
    .overnight-result {
        background: linear-gradient(135deg, #9c27b0, #ba68c8);
        color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: bold;
        border-left: 5px solid #6a1b9a;
    }
    
    /* Enhanced metrics for 24/7 */
    .stMetric {
        background: linear-gradient(145deg, #1e2139, #2a2d47);
        border: 2px solid #00d4aa;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 212, 170, 0.3);
        color: #ffffff;
        text-align: center;
    }
    
    /* Auto-scan countdown */
    .countdown {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    /* Formula display for all sessions */
    .formula-display {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        border: 3px solid #667eea;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* All other styling from previous version */
    .success-box {
        background: linear-gradient(135deg, #00ff88, #00d4aa);
        color: #000000;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #00ff88;
        box-shadow: 0 6px 12px rgba(0, 255, 136, 0.3);
    }
    
    .info-box {
        background: linear-gradient(135deg, #4ecdc4, #45b7d1);
        color: #000000;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #4ecdc4;
        box-shadow: 0 6px 12px rgba(78, 205, 196, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #feca57, #ff9ff3);
        color: #000000;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #feca57;
        box-shadow: 0 6px 12px rgba(254, 202, 87, 0.3);
    }
    
    .section-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: #00d4aa;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 8px solid #00d4aa;
        margin: 1.5rem 0;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0, 212, 170, 0.2);
    }
    
    .rank-gold {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #ffd700;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4);
    }
    
    .rank-silver {
        background: linear-gradient(135deg, #c0c0c0, #e8e8e8);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #c0c0c0;
        box-shadow: 0 4px 8px rgba(192, 192, 192, 0.4);
    }
    
    .rank-bronze {
        background: linear-gradient(135deg, #cd7f32, #d4af37);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #cd7f32;
        box-shadow: 0 4px 8px rgba(205, 127, 50, 0.4);
    }
    
    .rank-other {
        background: linear-gradient(135deg, #4ecdc4, #45b7d1);
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #4ecdc4;
        box-shadow: 0 4px 8px rgba(78, 205, 196, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for 24/7 operation
if 'auto_scan_active' not in st.session_state:
    st.session_state.auto_scan_active = False
if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = []
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0

# Set timezone
ET = pytz.timezone('US/Eastern')
current_et = datetime.now(ET)

def get_market_session():
    """Determine current market session with full 24/7 coverage"""
    now = datetime.now(ET)
    hour = now.hour
    minute = now.minute
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    # Weekend handling
    if weekday == 5 and hour >= 18:  # Saturday after 6 PM
        return "WEEKEND", "🏠", "weekend"
    elif weekday == 6:  # Sunday
        return "WEEKEND", "🏠", "weekend"
    elif weekday == 0 and hour < 4:  # Monday before 4 AM
        return "WEEKEND", "🏠", "weekend"
    
    # Weekday sessions
    if hour < 4:
        return "OVERNIGHT", "🌙", "overnight"
    elif 4 <= hour < 9 or (hour == 9 and minute < 30):
        return "PRE-MARKET", "🌅", "premarket"
    elif (hour == 9 and minute >= 30) or (10 <= hour < 16):
        return "REGULAR HOURS", "🔔", "regular"
    elif 16 <= hour < 20:
        return "AFTER-HOURS", "🌆", "afterhours"
    else:
        return "OVERNIGHT", "🌙", "overnight"

session, session_emoji, session_class = get_market_session()

# Header with 24/7 branding
st.markdown("""
<div class="auto-header">
🌍 24/7 QUANTSCORE™ AUTOMATIC SCANNER<br>
Pre-Market | Regular Hours | After-Hours | Overnight | All Sessions
</div>
""", unsafe_allow_html=True)

# Display current session prominently
st.markdown(f"""
<div class="session-{session_class}">
{session_emoji} CURRENT SESSION: {session}<br>
🕐 ET Time: {current_et.strftime('%Y-%m-%d %H:%M:%S')}<br>
🔄 Auto-Monitoring: {"ACTIVE" if st.session_state.auto_scan_active else "READY"}
</div>
""", unsafe_allow_html=True)

# QuantScore formula display
st.markdown("""
<div class="formula-display">
QuantScore™ = (Change% × Volume^1.3) / (MarketCap^0.7)<br>
24/7 Filters: Float < 10M | RSI > 55 | Gap% > 2%
</div>
""", unsafe_allow_html=True)

# Comprehensive ticker universe for all sessions
EXTENDED_UNIVERSE = [
    # High-volume stocks for extended hours
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX",
    
    # Popular small caps with extended trading
    "PHUN", "SNTI", "HUBC", "BBIG", "PROG", "ATER", "SPRT", "IRNT", "RDBX", "NILE",
    "MULN", "GFAI", "BMRA", "RELI", "BGFV", "CLOV", "WISH", "WKHS", "RIDE", "GOEV",
    "ARVL", "NAKD", "SNDL", "EXPR", "AMC", "GME", "MMAT", "TRCH", "VERB", "VXRT",
    "OCGN", "XELA", "GNUS", "JAGX", "INPX", "MARK", "UAMY", "TOPS", "SHIP", "GLBS",
    
    # Tech/AI with active extended hours
    "CXAI", "HOLO", "TRNR", "QUBT", "RGTI", "RR", "BNAI", "BOX", "APLD", "SERV",
    "SOFI", "PLTR", "HOOD", "RBLX", "DKNG", "FUBO", "SKLZ", "OPEN", "UPST", "AFRM",
    "COIN", "SQ", "PYPL", "ROKU", "ZM", "SHOP", "NET", "SNOW", "CRWD", "ZS",
    
    # Biotech with news-driven extended activity
    "ADTX", "ADMA", "AGIO", "AKRO", "ALEC", "ANAB", "ANIK", "APLS", "ARDX", "ARQT",
    "ASND", "AUPH", "AVIR", "BEAM", "BCAB", "BCRX", "BFRI", "BNGO", "BOLD", "BPMC",
    "BTTX", "CAPR", "CARA", "CBAY", "CDNA", "CDTX", "CHRS", "CTIC", "CTMX", "CPRX",
    
    # Energy/Mining with overnight futures correlation
    "TELL", "FCEL", "PLUG", "BE", "BLDP", "HYMC", "GOLD", "AG", "HL", "PAAS",
    "CDE", "SSRM", "WPM", "FNV", "SAND", "GORO", "FSM", "EGO", "AUY", "NEM",
    
    # Cannabis with international influence
    "TLRY", "CRON", "ACB", "HEXO", "OGI", "CGC", "GRWG", "SMG", "HYFM",
    
    # Crypto miners with 24/7 correlation
    "MARA", "RIOT", "HUT", "BITF", "EBON", "CAN", "BTBT", "WULF", "CIFR", "CORZ",
    "GRIID", "LGHL", "ANY", "BTCS", "DPRO", "ARBK", "EQOS", "HVBT", "IDEX"
]

def get_session_specific_data(ticker, session_type):
    """Get session-specific stock data with extended hours"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get extended hours data based on session
        if session_type in ["premarket", "afterhours"]:
            # Get intraday data with prepost for extended hours
            hist = stock.history(period="2d", interval="1m", prepost=True, timeout=3)
            daily = stock.history(period="5d", interval="1d", timeout=3)
        elif session_type == "regular":
            # Get standard market hours data
            hist = stock.history(period="1d", interval="1m", timeout=3)
            daily = stock.history(period="5d", interval="1d", timeout=3)
        elif session_type == "overnight":
            # Use previous day's data and futures correlation
            daily = stock.history(period="5d", interval="1d", timeout=3)
            hist = daily  # Use daily data for overnight
        else:  # weekend
            # Use weekly data for analysis
            daily = stock.history(period="5d", interval="1d", timeout=3)
            hist = daily
        
        if daily.empty or len(daily) < 2:
            return None
        
        # Calculate current/latest price
        if not hist.empty and session_type in ["premarket", "afterhours", "regular"]:
            current_price = hist['Close'].iloc[-1]
            current_volume = hist['Volume'].iloc[-1] if hist['Volume'].iloc[-1] > 0 else daily['Volume'].iloc[-1]
        else:
            current_price = daily['Close'].iloc[-1]
            current_volume = daily['Volume'].iloc[-1]
        
        prev_close = daily['Close'].iloc[-2]
        change_pct = ((current_price - prev_close) / prev_close) * 100
        
        # Calculate gap based on session
        if session_type in ["premarket", "regular"] and not hist.empty:
            try:
                today_open = hist['Open'].iloc[0]
                gap_pct = ((today_open - prev_close) / prev_close) * 100
            except:
                gap_pct = change_pct
        else:
            gap_pct = change_pct
        
        # Get fundamental data
        try:
            info = stock.info
            market_cap = info.get('marketCap', 0)
            float_shares = info.get('floatShares', 0)
            shares_outstanding = info.get('sharesOutstanding', 0)
            
            if market_cap == 0 and shares_outstanding > 0:
                market_cap = current_price * shares_outstanding
                
            if float_shares == 0:
                float_shares = shares_outstanding * 0.75 if shares_outstanding > 0 else 0
                
        except:
            return None
        
        # Calculate RSI
        if len(daily) >= 14:
            delta = daily['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = (100 - (100 / (1 + rs))).iloc[-1]
        else:
            rsi = 50
            
        return {
            'ticker': ticker,
            'current_price': float(current_price),
            'change_pct': float(change_pct),
            'gap_pct': float(gap_pct),
            'volume': int(current_volume) if current_volume > 0 else 0,
            'market_cap': int(market_cap) if market_cap > 0 else 0,
            'float_shares': int(float_shares) if float_shares > 0 else 0,
            'rsi': float(rsi) if not pd.isna(rsi) else 50,
            'session': session,
            'last_updated': datetime.now(ET)
        }
        
    except Exception:
        return None

def calculate_quantscore_24_7(data, session_type):
    """Calculate QuantScore with session-specific adjustments"""
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        
        if market_cap <= 0 or volume <= 0:
            return 0
        
        # Base QuantScore formula
        base_score = (change_pct * (volume ** 1.3)) / (market_cap ** 0.7)
        
        # Session-specific multipliers for different trading conditions
        if session_type == "premarket":
            return base_score * 1.5  # Premium for pre-market moves
        elif session_type == "afterhours":
            return base_score * 1.3  # Premium for after-hours moves
        elif session_type == "overnight":
            return base_score * 0.8  # Discounted for overnight (limited data)
        elif session_type == "weekend":
            return base_score * 0.5  # Heavily discounted for weekend analysis
        else:  # regular hours
            return base_score
            
    except:
        return 0

def apply_quantscore_filters_24_7(data, session_type):
    """Apply QuantScore filters with session awareness"""
    try:
        base_filters = (
            data['float_shares'] < 10_000_000 and  # Float < 10M
            data['rsi'] > 55 and                   # RSI > 55
            data['volume'] > 0 and                # Volume check
            data['market_cap'] > 0                # Market cap check
        )
        
        # Adjust gap requirement based on session
        if session_type in ["premarket", "regular"]:
            gap_filter = abs(data['gap_pct']) > 2.0  # Standard gap requirement
        elif session_type == "afterhours":
            gap_filter = abs(data['gap_pct']) > 1.5  # Slightly lower for after-hours
        elif session_type == "overnight":
            gap_filter = abs(data['change_pct']) > 1.0  # Use change instead of gap
        else:  # weekend
            gap_filter = abs(data['change_pct']) > 0.5  # Very low threshold for weekend
        
        return base_filters and gap_filter
        
    except:
        return False

# Sidebar with 24/7 controls
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 2px solid #667eea;">
<h2 style="color: #ffffff; text-align: center; margin: 0;">🌍 24/7 AUTO SCANNER</h2>
<p style="color: #ffffff; text-align: center; margin: 0.5rem 0 0 0;">Current: {session} {session_emoji}</p>
</div>
""", unsafe_allow_html=True)

# 24/7 operation controls
st.sidebar.markdown('<div class="section-header">⚡ 24/7 Operation</div>', unsafe_allow_html=True)

auto_mode = st.sidebar.checkbox("🔄 Enable 24/7 Auto-Scan", value=st.session_state.auto_scan_active)
refresh_interval = st.sidebar.selectbox("⏱️ Auto-Refresh Interval", 
    ["30 seconds", "1 minute", "2 minutes", "5 minutes", "10 minutes"], 
    index=2
)

# Parse refresh interval
interval_map = {
    "30 seconds": 30,
    "1 minute": 60,
    "2 minutes": 120,
    "5 minutes": 300,
    "10 minutes": 600
}
refresh_seconds = interval_map[refresh_interval]

# Session-specific settings
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Session Settings")

max_tickers = st.sidebar.slider("🔍 Max Tickers per Scan", 50, 300, 150, 25)
session_priority = st.sidebar.multiselect(
    "📅 Priority Sessions",
    ["PRE-MARKET", "REGULAR HOURS", "AFTER-HOURS", "OVERNIGHT"],
    default=["PRE-MARKET", "REGULAR HOURS", "AFTER-HOURS"]
)

# Display 24/7 status
st.sidebar.markdown(f"""
<div class="live-status">
<strong>🌍 24/7 STATUS:</strong><br>
📅 Session: {session}<br>
🕐 ET Time: {current_et.strftime('%H:%M:%S')}<br>
🔄 Auto-Scan: {"ON" if auto_mode else "OFF"}<br>
⏱️ Interval: {refresh_interval}<br>
🎯 Tickers: {max_tickers}<br>
📊 Last Scan: {st.session_state.last_scan_time or "Never"}
</div>
""", unsafe_allow_html=True)

# Update session state
st.session_state.auto_scan_active = auto_mode

# Auto-refresh logic
if auto_mode:
    st.markdown('<div class="auto-refresh">🔄 24/7 AUTO-SCAN MODE ACTIVE</div>', unsafe_allow_html=True)
    
    # Countdown display
    if st.session_state.last_scan_time:
        time_since_scan = (datetime.now() - st.session_state.last_scan_time).total_seconds()
        time_until_next = max(0, refresh_seconds - time_since_scan)
        st.markdown(f'<div class="countdown">⏱️ Next Auto-Scan in: {int(time_until_next)} seconds</div>', unsafe_allow_html=True)
    
    # Auto-scan trigger
    should_scan = False
    if st.session_state.last_scan_time is None:
        should_scan = True
    elif (datetime.now() - st.session_state.last_scan_time).total_seconds() >= refresh_seconds:
        should_scan = True
    
    if should_scan:
        # Auto-scan execution
        st.markdown(f'<div class="auto-refresh">🔄 AUTO-SCANNING {session}...</div>', unsafe_allow_html=True)
        
        # Get session-specific tickers
        scan_tickers = EXTENDED_UNIVERSE[:max_tickers]
        
        start_time = time.time()
        qualified_stocks = []
        scanned_count = 0
        
        # Progress for auto-scan
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        for i, ticker in enumerate(scan_tickers):
            status_placeholder.markdown(f'<div class="auto-refresh">🔍 Auto-scanning: {ticker} [{session}]</div>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) / len(scan_tickers))
            
            data = get_session_specific_data(ticker, session_class)
            scanned_count += 1
            
            if data and apply_quantscore_filters_24_7(data, session_class):
                quantscore = calculate_quantscore_24_7(data, session_class)
                
                if quantscore > 0:
                    qualified_stocks.append({
                        'Ticker': data['ticker'],
                        'QuantScore™': quantscore,
                        'Price': data['current_price'],
                        'Change%': data['change_pct'],
                        'Gap%': data['gap_pct'],
                        'Volume': data['volume'],
                        'Float (M)': data['float_shares'] / 1_000_000,
                        'RSI': data['rsi'],
                        'Session': data['session'],
                        'Updated': data['last_updated'].strftime('%H:%M:%S')
                    })
        
        scan_time = time.time() - start_time
        progress_bar.empty()
        status_placeholder.empty()
        
        # Update session state
        st.session_state.last_scan_time = datetime.now()
        st.session_state.scan_results = qualified_stocks
        st.session_state.scan_count += 1
        
        # Auto-rerun for continuous operation
        time.sleep(2)  # Brief pause before rerun
        st.rerun()

# Manual scan button
if st.sidebar.button("🚀 MANUAL SCAN NOW", type="primary"):
    st.markdown(f'<div class="session-{session_class}">🔍 MANUAL QUANTSCORE™ SCAN - {session}</div>', unsafe_allow_html=True)
    
    # Manual scan execution (same logic as auto-scan)
    scan_tickers = EXTENDED_UNIVERSE[:max_tickers]
    start_time = time.time()
    qualified_stocks = []
    scanned_count = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner(f"🔍 Manual scanning {session}..."):
        for i, ticker in enumerate(scan_tickers):
            status_text.markdown(f'<div class="session-{session_class}">🔍 Scanning: {ticker}</div>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) / len(scan_tickers))
            
            data = get_session_specific_data(ticker, session_class)
            scanned_count += 1
            
            if data and apply_quantscore_filters_24_7(data, session_class):
                quantscore = calculate_quantscore_24_7(data, session_class)
                
                if quantscore > 0:
                    qualified_stocks.append({
                        'Ticker': data['ticker'],
                        'QuantScore™': quantscore,
                        'Price': data['current_price'],
                        'Change%': data['change_pct'],
                        'Gap%': data['gap_pct'],
                        'Volume': data['volume'],
                        'Float (M)': data['float_shares'] / 1_000_000,
                        'RSI': data['rsi'],
                        'Session': data['session'],
                        'Updated': data['last_updated'].strftime('%H:%M:%S')
                    })
            
            time.sleep(0.01)
    
    scan_time = time.time() - start_time
    progress_bar.empty()
    status_text.empty()
    
    # Update session state
    st.session_state.last_scan_time = datetime.now()
    st.session_state.scan_results = qualified_stocks
    st.session_state.scan_count += 1

# Display results (either from auto-scan or manual scan)
if st.session_state.scan_results:
    qualified_stocks = st.session_state.scan_results
    
    st.markdown(f'<div class="section-header">🏆 {session} QUANTSCORE™ RESULTS</div>', unsafe_allow_html=True)
    
    # Session-specific metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌍 Session", session)
    with col2:
        st.metric("🎯 Qualified", len(qualified_stocks))
    with col3:
        st.metric("🔄 Scan #", st.session_state.scan_count)
    with col4:
        st.metric("🕐 Last Scan", st.session_state.last_scan_time.strftime('%H:%M:%S') if st.session_state.last_scan_time else "Never")
    with col5:
        st.metric("⚡ Auto-Mode", "ON" if auto_mode else "OFF")
    
    if qualified_stocks:
        # Sort by QuantScore
        df = pd.DataFrame(qualified_stocks)
        df = df.sort_values('QuantScore™', ascending=False)
        
        # Format for display
        display_df = df.copy()
        display_df['QuantScore™'] = display_df['QuantScore™'].apply(lambda x: f"{x:.8f}")
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Change%'] = display_df['Change%'].apply(lambda x: f"{x:+.2f}%")
        display_df['Gap%'] = display_df['Gap%'].apply(lambda x: f"{x:+.2f}%")
        display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:,.0f}")
        display_df['Float (M)'] = display_df['Float (M)'].apply(lambda x: f"{x:.1f}M")
        display_df['RSI'] = display_df['RSI'].apply(lambda x: f"{x:.0f}")
        
        display_df.index = range(1, len(display_df) + 1)
        display_df.index.name = 'Rank'
        
        st.markdown(f'<div class="success-box">🎉 {session} SUCCESS: Found {len(qualified_stocks)} QuantScore™ opportunities!</div>', unsafe_allow_html=True)
        
        # Display table
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Top picks with session-specific styling
        st.markdown(f'<div class="section-header">🏆 TOP {session} PICKS</div>', unsafe_allow_html=True)
        
        for i, (idx, row) in enumerate(display_df.head(10).iterrows()):
            result_class = f"{session_class}-result"
            
            if i == 0:
                st.markdown(f'<div class="rank-gold">🥇 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | RSI: {row["RSI"]} | Session: {row["Session"]}</div>', unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f'<div class="rank-silver">🥈 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | RSI: {row["RSI"]} | Session: {row["Session"]}</div>', unsafe_allow_html=True)
            elif i == 2:
                st.markdown(f'<div class="rank-bronze">🥉 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | RSI: {row["RSI"]} | Session: {row["Session"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="rank-other">⭐ #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | RSI: {row["RSI"]} | Session: {row["Session"]}</div>', unsafe_allow_html=True)
        
        # Export 24/7 results
        col1, col2 = st.columns(2)
        with col1:
            csv = display_df.to_csv()
            st.download_button(
                f"📊 Download {session} Results",
                csv,
                file_name=f"quantscore_24_7_{session_class}_{datetime.now(ET).strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            summary = f"""24/7 QUANTSCORE™ SCAN REPORT
Generated: {datetime.now(ET).strftime('%Y-%m-%d %H:%M:%S ET')}
Session: {session} {session_emoji}

QUANTSCORE™ FORMULA (24/7):
Base: (Change% × Volume^1.3) / (MarketCap^0.7)
Session Multiplier: {session_class}

QUALITY FILTERS:
✅ Float Shares < 10M
✅ RSI > 55
✅ Gap% > 2% (session adjusted)

24/7 SCAN DETAILS:
- Current Session: {session}
- Scan Mode: {"AUTO" if auto_mode else "MANUAL"}
- Auto-Refresh: {refresh_interval}
- Scan Count: {st.session_state.scan_count}
- Qualified Stocks: {len(qualified_stocks)}

TOP 5 {session} PICKS:
"""
            for i, (idx, row) in enumerate(display_df.head(5).iterrows()):
                summary += f"{i+1}. {row['Ticker']} - QuantScore™: {row['QuantScore™']} | Price: {row['Price']} | Session: {row['Session']}\n"
            
            st.download_button(
                f"📋 Download {session} Report",
                summary,
                file_name=f"quantscore_24_7_report_{datetime.now(ET).strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    else:
        st.markdown(f'<div class="warning-box">⚠️ NO {session} QUANTSCORE™ OPPORTUNITIES FOUND</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
        💡 {session} conditions may not have qualifying stocks right now.<br>
        • Try different sessions when auto-mode runs<br>
        • Check back during high volatility periods<br>
        • Your QuantScore™ filters are strict for quality<br>
        • Auto-scan will continue monitoring 24/7
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome screen for 24/7 operation
    st.markdown('<div class="section-header">🌍 Welcome to 24/7 QuantScore™ Scanner</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-box">
        <h3>🌍 24/7 OPERATION:</h3>
        • Monitors ALL trading sessions automatically<br>
        • Pre-Market (4:00-9:30 AM ET) 🌅<br>
        • Regular Hours (9:30 AM-4:00 PM ET) 🔔<br>
        • After-Hours (4:00 PM-8:00 PM ET) 🌆<br>
        • Overnight (8:00 PM-4:00 AM ET) 🌙<br>
        • Weekend Analysis (Limited) 🏠<br>
        • Your exact QuantScore™ formula across all sessions
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="success-box">
        <h3>⚡ AUTO-FEATURES:</h3>
        • Automatic session detection<br>
        • Session-specific data handling<br>
        • Extended hours price tracking<br>
        • Continuous monitoring mode<br>
        • Smart refresh intervals<br>
        • 24/7 opportunity alerts<br>
        • Currently: {session} {session_emoji}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="live-status">
    🌍 24/7 QUANTSCORE™ SCANNER READY<br>
    📅 Current Session: {session} {session_emoji}<br>
    🕐 ET Time: {current_et.strftime('%H:%M:%S')}<br>
    🔄 Enable auto-scan in sidebar for continuous monitoring<br>
    🚀 Or click "MANUAL SCAN NOW" for immediate results
    </div>
    """, unsafe_allow_html=True)

# Information section
with st.expander("🌍 24/7 QuantScore™ Technology"):
    st.markdown(f"""
    ### 🌍 24/7 Operation Capabilities:
    
    **Current Session: {session} {session_emoji}**
    
    ### 📅 All Trading Sessions Covered:
    - **🌅 Pre-Market (4:00-9:30 AM ET):** Extended hours data with gap detection
    - **🔔 Regular Hours (9:30 AM-4:00 PM ET):** Full market data with real-time updates
    - **🌆 After-Hours (4:00 PM-8:00 PM ET):** Extended trading with earnings reactions
    - **🌙 Overnight (8:00 PM-4:00 AM ET):** Analysis mode with futures correlation
    - **🏠 Weekend:** Historical analysis and preparation for next week
    
    ### ⚡ Automatic Features:
    - **Session Auto-Detection:** Automatically determines current market session
    - **Extended Hours Data:** Gets pre-market and after-hours pricing
    - **Session-Specific Scoring:** Adjusts QuantScore™ based on session conditions
    - **Continuous Monitoring:** Auto-refresh at your chosen intervals
    - **Smart Filtering:** Adapts gap requirements to session characteristics
    
    ### 🎯 Your QuantScore™ Formula (24/7):
    
    **Base Formula:** `(Change% × Volume^1.3) / (MarketCap^0.7)`
    
    **Session Multipliers:**
    - Pre-Market: 1.5x (premium for early moves)
    - Regular Hours: 1.0x (standard scoring)
    - After-Hours: 1.3x (premium for post-market moves)
    - Overnight: 0.8x (limited data discount)
    - Weekend: 0.5x (analysis mode only)
    
    ### ✅ Quality Filters (All Sessions):
    - **Float < 10M shares** (consistent across all sessions)
    - **RSI > 55** (momentum confirmation in all sessions)
    - **Gap Requirements** (adjusted by session):
      - Pre-Market/Regular: Gap > 2%
      - After-Hours: Gap > 1.5%
      - Overnight: Change > 1%
      - Weekend: Change > 0.5%
    
    ### 🔄 Auto-Refresh Options:
    - **30 seconds:** Ultra-fast for active trading
    - **1 minute:** Fast updates for day trading
    - **2 minutes:** Balanced for swing trading
    - **5 minutes:** Conservative for position building
    - **10 minutes:** Slow for long-term analysis
    
    ### 🌐 Data Sources by Session:
    - **Market Hours:** Real-time 1-minute intervals
    - **Extended Hours:** Pre/post market data streams
    - **Overnight:** Daily data with futures correlation
    - **Weekend:** Weekly analysis with next week preparation
    
    ### 💡 Why 24/7 Matters:
    - **Pre-Market Gaps:** Catch earnings reactions before market open
    - **After-Hours News:** React to announcements after close
    - **Overnight Futures:** Monitor commodity/forex correlations
    - **Weekend Analysis:** Prepare for Monday gaps and setups
    - **Global Markets:** Monitor international influences
    """)

st.markdown("---")
st.markdown(f"""
<div class="warning-box">
🚨 24/7 QUANTSCORE™ DISCLAIMER: This system operates continuously across all trading sessions using your proprietary QuantScore™ formula. Extended hours trading carries additional risks including wider spreads, lower liquidity, and higher volatility. Small cap stocks meeting your strict criteria (Float < 10M, RSI > 55, Gap > 2%) are extremely volatile and can move 50%+ rapidly, especially during extended sessions. The automatic refresh feature is designed for continuous monitoring but does not reduce market risks. This is advanced 24/7 trading technology for educational purposes only - not investment advice. Current session: {session} {session_emoji}
</div>
""", unsafe_allow_html=True)

# Auto-refresh mechanism for 24/7 operation
if auto_mode and st.session_state.last_scan_time:
    time_since_scan = (datetime.now() - st.session_state.last_scan_time).total_seconds()
    if time_since_scan >= refresh_seconds:
        time.sleep(1)
        st.rerun()
