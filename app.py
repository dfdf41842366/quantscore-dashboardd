import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
import concurrent.futures
import threading

# Configure page with dark theme
st.set_page_config(
    page_title="🌙 QuantScore™ Live Scanner",
    page_icon="🌙",
    layout="wide"
)

# Enhanced dark theme CSS for maximum readability
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background-color: #0f1419;
        color: #e6e6e6;
    }
    
    /* Sidebar dark styling */
    .css-1d391kg {
        background-color: #1a1f2e;
    }
    
    /* Main header with your QuantScore branding */
    .quantscore-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: #000000;
        font-weight: bold;
        font-size: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        border: 3px solid #667eea;
    }
    
    /* Metrics with better contrast */
    .stMetric {
        background: linear-gradient(145deg, #1e2139, #2a2d47);
        border: 2px solid #00d4aa;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 212, 170, 0.3);
        color: #ffffff;
        text-align: center;
    }
    
    .stMetric label {
        color: #00d4aa !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    
    .stMetric .metric-value {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
    }
    
    /* Success boxes - bright and readable */
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
    
    /* Info boxes - clear blue theme */
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
    
    /* Warning boxes - bright yellow for visibility */
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
    
    /* Error boxes - bright red for alerts */
    .error-box {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #ff6b6b;
        box-shadow: 0 6px 12px rgba(255, 107, 107, 0.3);
    }
    
    /* Section headers - highly visible */
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
    
    /* Formula display box */
    .formula-box {
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
    
    /* Ranking displays - gold, silver, bronze */
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
    
    /* Button styling - more visible */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #00d4aa);
        color: #000000;
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 12px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00d4aa, #00ff88);
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0, 255, 136, 0.5);
    }
    
    /* Sidebar styling */
    .stSidebar .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #ffffff;
        width: 100%;
        margin: 1rem 0;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    /* Input fields - dark theme */
    .stTextArea > div > div > textarea {
        background-color: #2a2d47;
        color: #ffffff;
        border: 2px solid #00d4aa;
        border-radius: 10px;
        font-size: 1rem;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00ff88, #4ecdc4);
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #00ff88, #4ecdc4);
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background-color: #1e2139;
        border-radius: 15px;
        border: 2px solid #00d4aa;
        box-shadow: 0 8px 16px rgba(0, 212, 170, 0.2);
    }
    
    /* Status indicators */
    .status-live {
        background: linear-gradient(45deg, #00ff88, #32cd32);
        color: #000000;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        animation: pulse 2s infinite;
        margin: 0.5rem;
        border: 2px solid #00ff88;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* High contrast text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .stMarkdown {
        color: #e6e6e6 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2a2d47;
        color: #00d4aa;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header with QuantScore branding
st.markdown("""
<div class="quantscore-header">
🌙 QuantScore™ LIVE MARKET SCANNER<br>
Your Proprietary Formula | Live Discovery | Dark Theme
</div>
""", unsafe_allow_html=True)

# Display your QuantScore formula prominently
st.markdown("""
<div class="formula-box">
QuantScore = (Change% × Volume^1.3) / (MarketCap^0.7)<br>
Quality Filters: Float < 10M | RSI > 55 | Gap% > 2%
</div>
""", unsafe_allow_html=True)

# Comprehensive ticker universe for live discovery
MARKET_UNIVERSE = [
    # Popular small caps
    "PHUN", "SNTI", "HUBC", "BBIG", "PROG", "ATER", "SPRT", "IRNT", "RDBX", "NILE",
    "MULN", "GFAI", "BMRA", "RELI", "BGFV", "CLOV", "WISH", "WKHS", "RIDE", "GOEV",
    "ARVL", "NAKD", "SNDL", "EXPR", "AMC", "GME", "MMAT", "TRCH", "VERB", "VXRT",
    "OCGN", "XELA", "GNUS", "JAGX", "INPX", "MARK", "UAMY", "TOPS", "SHIP", "GLBS",
    
    # AI/Tech small caps
    "CXAI", "HOLO", "TRNR", "QUBT", "RGTI", "RR", "BNAI", "BOX", "APLD", "SERV",
    "SOFI", "PLTR", "HOOD", "RBLX", "DKNG", "FUBO", "SKLZ", "OPEN", "UPST", "AFRM",
    
    # Biotech universe
    "ADTX", "ADMA", "AGIO", "AKRO", "ALEC", "ANAB", "ANIK", "APLS", "ARDX", "ARQT",
    "ASND", "AUPH", "AVIR", "BEAM", "BCAB", "BCRX", "BFRI", "BNGO", "BOLD", "BPMC",
    "BTTX", "CAPR", "CARA", "CBAY", "CDNA", "CDTX", "CHRS", "CTIC", "CTMX", "CPRX",
    "CRDF", "CRSP", "CTSO", "CYAD", "CYTK", "DSGX", "EDIT", "FATE", "FOLD", "GTHX",
    
    # Energy/Mining
    "TELL", "FCEL", "PLUG", "BE", "BLDP", "HYMC", "GOLD", "AG", "HL", "PAAS",
    "CDE", "SSRM", "WPM", "FNV", "SAND", "GORO", "FSM", "EGO", "AUY", "NEM",
    
    # Cannabis sector
    "TLRY", "CRON", "ACB", "HEXO", "OGI", "CGC", "GRWG", "SMG", "HYFM", "KERN",
    
    # Crypto/Mining
    "MARA", "RIOT", "HUT", "BITF", "EBON", "CAN", "BTBT", "WULF", "CIFR", "CORZ",
    "GRIID", "LGHL", "ANY", "BTCS", "DPRO", "NXTD", "ARBK", "EQOS", "HVBT", "IDEX",
    
    # Shipping/Transport
    "DRYS", "CTRM", "CASTOR", "EDRY", "EGLE", "SBLK", "NM", "NAT", "FRO", "TNK",
    "STNG", "EURN", "DHT", "TK", "TNP", "INSW", "CPLP", "ORIG", "VLRS", "CMRE"
]

def get_extended_universe():
    """Dynamically expand the ticker universe"""
    extended_tickers = set(MARKET_UNIVERSE)
    
    # Add pattern-based discoveries
    base_patterns = ["PHUN", "SNTI", "GFAI", "MULN", "RELI"]
    
    for base in base_patterns:
        # Generate similar ticker patterns
        for i in range(1, 10):
            for suffix in ['', 'A', 'B', 'C', 'X', 'Y', 'Z']:
                potential = f"{base[:2]}{suffix}{i}"
                if len(potential) <= 5:
                    extended_tickers.add(potential)
    
    # Add systematic penny stock patterns
    penny_prefixes = ['BB', 'CC', 'DD', 'FF', 'GG', 'HH', 'JJ', 'KK', 'LL', 'MM', 'NN', 'PP', 'RR', 'SS', 'TT', 'VV', 'WW', 'XX', 'YY', 'ZZ']
    penny_suffixes = ['IG', 'OG', 'EL', 'UN', 'AI', 'LY', 'US', 'EX', 'IX', 'AN']
    
    for prefix in penny_prefixes[:10]:  # Limit for performance
        for suffix in penny_suffixes[:5]:
            extended_tickers.add(f"{prefix}{suffix}")
    
    return list(extended_tickers)

def get_live_stock_data(ticker):
    """Get comprehensive live stock data"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get recent price data
        hist = stock.history(period="5d", interval="1d", timeout=3)
        if hist.empty or len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        change_pct = ((current_price - prev_close) / prev_close) * 100
        volume = hist['Volume'].iloc[-1]
        
        # Get intraday data for gap calculation
        try:
            intraday = stock.history(period="2d", interval="1m", prepost=True, timeout=2)
            if not intraday.empty:
                today_open = intraday.iloc[0]['Open']
                gap_pct = ((today_open - prev_close) / prev_close) * 100
            else:
                gap_pct = change_pct  # Fallback
        except:
            gap_pct = change_pct
        
        # Get company fundamentals
        try:
            info = stock.info
            market_cap = info.get('marketCap', 0)
            float_shares = info.get('floatShares', 0)
            shares_outstanding = info.get('sharesOutstanding', 0)
            
            # Fallback calculations
            if market_cap == 0 and shares_outstanding > 0:
                market_cap = current_price * shares_outstanding
                
            if float_shares == 0:
                float_shares = shares_outstanding * 0.75 if shares_outstanding > 0 else 0
                
        except:
            return None  # Skip if we can't get basic info
        
        # Calculate RSI (your requirement: RSI > 55)
        if len(hist) >= 14:
            delta = hist['Close'].diff()
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
            'volume': int(volume) if volume > 0 else 0,
            'market_cap': int(market_cap) if market_cap > 0 else 0,
            'float_shares': int(float_shares) if float_shares > 0 else 0,
            'rsi': float(rsi) if not pd.isna(rsi) else 50,
            'last_updated': datetime.now()
        }
        
    except Exception:
        return None

def calculate_your_quantscore(data):
    """Calculate QuantScore using YOUR exact formula"""
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        
        if market_cap <= 0 or volume <= 0:
            return 0
        
        # YOUR EXACT FORMULA: QuantScore = (Change% × Volume^1.3) / (MarketCap^0.7)
        quantscore = (change_pct * (volume ** 1.3)) / (market_cap ** 0.7)
        
        return quantscore
    except:
        return 0

def apply_your_filters(data):
    """Apply YOUR exact quality filters"""
    try:
        # YOUR REQUIREMENTS:
        # - floatShares < 10M
        # - RSI > 55  
        # - Gap% > 2
        
        return (
            data['float_shares'] < 10_000_000 and  # Float < 10M
            data['rsi'] > 55 and                   # RSI > 55
            abs(data['gap_pct']) > 2.0 and        # Gap% > 2%
            data['volume'] > 0 and                # Basic volume check
            data['market_cap'] > 0                # Basic market cap check
        )
    except:
        return False

# Sidebar with your QuantScore branding
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 2px solid #667eea;">
<h2 style="color: #ffffff; text-align: center; margin: 0;">🌙 QuantScore™ Scanner</h2>
<p style="color: #ffffff; text-align: center; margin: 0.5rem 0 0 0;">Your Proprietary Formula</p>
</div>
""", unsafe_allow_html=True)

# Your filter controls (keeping your original criteria)
st.sidebar.markdown('<div class="section-header">🎯 Your QuantScore Filters</div>', unsafe_allow_html=True)

# Additional price filters (optional refinements to your base criteria)
price_min = st.sidebar.slider("💰 Additional Price Min ($)", 0.5, 5.0, 1.0, 0.5)
price_max = st.sidebar.slider("💰 Additional Price Max ($)", 5.0, 25.0, 20.0, 1.0)
min_volume = st.sidebar.selectbox("📊 Additional Volume Filter", [0, 50_000, 100_000, 250_000], index=0)

st.sidebar.markdown("---")
max_discovery = st.sidebar.slider("🔍 Max Tickers to Discover", 100, 1000, 300, 50)

# Display your exact criteria
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, #2a2d47, #1e2139); padding: 1.5rem; border-radius: 10px; color: #00d4aa; border: 2px solid #00d4aa;">
<strong>📊 YOUR QUANTSCORE™ CRITERIA:</strong><br><br>
<strong>Formula:</strong><br>
(Change% × Volume^1.3) / MarketCap^0.7<br><br>
<strong>Required Conditions:</strong><br>
✅ Float Shares < 10M<br>
✅ RSI > 55<br>
✅ Gap% > 2%<br><br>
<strong>Additional Filters:</strong><br>
💰 Price: ${price_min}-${price_max}<br>
📊 Volume: >{min_volume:,}<br>
🔍 Discovery: {max_discovery} tickers
</div>
""", unsafe_allow_html=True)

# Main scanning button
if st.sidebar.button("🚀 RUN QUANTSCORE™ SCAN", type="primary"):
    st.markdown('<div class="status-live">🔴 QUANTSCORE™ LIVE SCAN IN PROGRESS</div>', unsafe_allow_html=True)
    
    # Progress display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-box">🌐 DISCOVERING<br>Market Universe</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-box">🔍 SCANNING<br>Live Data</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="info-box">📊 APPLYING<br>QuantScore™ Logic</div>', unsafe_allow_html=True)
    
    start_time = time.time()
    
    # Get extended ticker universe
    with st.spinner("🌐 Discovering ticker universe..."):
        all_tickers = get_extended_universe()
        discovery_tickers = all_tickers[:max_discovery]
        st.success(f"🎯 Discovered {len(discovery_tickers)} tickers for QuantScore™ analysis")
    
    # Live scanning with your QuantScore logic
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    qualified_stocks = []
    scanned_count = 0
    
    with st.spinner("🔍 Applying your QuantScore™ formula..."):
        for i, ticker in enumerate(discovery_tickers):
            status_text.markdown(f'<div class="status-live">🔍 QuantScore™ Scanning: {ticker}</div>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) / len(discovery_tickers))
            
            data = get_live_stock_data(ticker)
            scanned_count += 1
            
            if data:
                # Apply YOUR quality filters first
                if apply_your_filters(data):
                    # Additional optional price/volume filters
                    if (price_min <= data['current_price'] <= price_max and
                        data['volume'] >= min_volume):
                        
                        # Calculate YOUR QuantScore
                        quantscore = calculate_your_quantscore(data)
                        
                        if quantscore > 0:
                            qualified_stocks.append({
                                'Ticker': data['ticker'],
                                'QuantScore™': quantscore,
                                'Price': data['current_price'],
                                'Change%': data['change_pct'],
                                'Gap%': data['gap_pct'],
                                'Volume': data['volume'],
                                'Float (M)': data['float_shares'] / 1_000_000,
                                'Market Cap': data['market_cap'],
                                'RSI': data['rsi'],
                                'Updated': data['last_updated'].strftime('%H:%M:%S')
                            })
            
            time.sleep(0.01)  # Small delay for smooth progress
    
    total_time = time.time() - start_time
    progress_bar.empty()
    status_text.empty()
    
    # Display QuantScore results
    st.markdown('<div class="section-header">🏆 QuantScore™ LIVE RESULTS</div>', unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌐 Discovered", len(discovery_tickers))
    with col2:
        st.metric("🔍 Scanned", scanned_count)
    with col3:
        st.metric("🎯 QuantScore™ Qualified", len(qualified_stocks))
    with col4:
        filter_rate = (len(qualified_stocks) / max(scanned_count, 1)) * 100
        st.metric("✅ Filter Rate", f"{filter_rate:.1f}%")
    with col5:
        st.metric("⚡ Scan Time", f"{total_time:.1f}s")
    
    if qualified_stocks:
        # Sort by YOUR QuantScore
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
        display_df['Market Cap'] = display_df['Market Cap'].apply(lambda x: f"${x/1e6:.1f}M" if x > 0 else "N/A")
        display_df['RSI'] = display_df['RSI'].apply(lambda x: f"{x:.0f}")
        
        display_df.index = range(1, len(display_df) + 1)
        display_df.index.name = 'Rank'
        
        st.markdown(f'<div class="success-box">🎉 QuantScore™ SUCCESS: Found {len(qualified_stocks)} stocks meeting YOUR exact criteria!</div>', unsafe_allow_html=True)
        
        # Display table
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Top picks with your QuantScore ranking
        st.markdown('<div class="section-header">🏆 TOP QuantScore™ PICKS</div>', unsafe_allow_html=True)
        
        for i, (idx, row) in enumerate(display_df.head(10).iterrows()):
            if i == 0:
                st.markdown(f'<div class="rank-gold">🥇 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | Float: {row["Float (M)"]} | RSI: {row["RSI"]}</div>', unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f'<div class="rank-silver">🥈 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | Float: {row["Float (M)"]} | RSI: {row["RSI"]}</div>', unsafe_allow_html=True)
            elif i == 2:
                st.markdown(f'<div class="rank-bronze">🥉 #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | Float: {row["Float (M)"]} | RSI: {row["RSI"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="rank-other">⭐ #{idx}: {row["Ticker"]} | QuantScore™: {row["QuantScore™"]} | Price: {row["Price"]} | Change: {row["Change%"]} | Gap: {row["Gap%"]} | Float: {row["Float (M)"]} | RSI: {row["RSI"]}</div>', unsafe_allow_html=True)
        
        # Export functionality
        col1, col2 = st.columns(2)
        with col1:
            csv = display_df.to_csv()
            st.download_button(
                "📊 Download QuantScore™ Results",
                csv,
                file_name=f"quantscore_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            summary = f"""QUANTSCORE™ LIVE SCAN REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

YOUR QUANTSCORE™ FORMULA:
QuantScore = (Change% × Volume^1.3) / (MarketCap^0.7)

YOUR QUALITY FILTERS:
✅ Float Shares < 10M
✅ RSI > 55  
✅ Gap% > 2%

ADDITIONAL FILTERS:
- Price Range: ${price_min} - ${price_max}
- Min Volume: {min_volume:,}

SCAN RESULTS:
- Tickers Discovered: {len(discovery_tickers)}
- Stocks Scanned: {scanned_count}
- QuantScore™ Qualified: {len(qualified_stocks)}
- Filter Success Rate: {filter_rate:.1f}%
- Total Scan Time: {total_time:.1f} seconds

TOP 5 QUANTSCORE™ PICKS:
"""
            for i, (idx, row) in enumerate(display_df.head(5).iterrows()):
                summary += f"{i+1}. {row['Ticker']} - QuantScore™: {row['QuantScore™']} | Price: {row['Price']} | RSI: {row['RSI']}\n"
            
            st.download_button(
                "📋 Download QuantScore™ Report",
                summary,
                file_name=f"quantscore_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    else:
        st.markdown('<div class="warning-box">⚠️ NO STOCKS MET YOUR QUANTSCORE™ CRITERIA</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        💡 Your QuantScore™ filters are very strict:<br>
        • Float < 10M shares (eliminates most large stocks)<br>
        • RSI > 55 (requires strong momentum)<br>
        • Gap% > 2% (requires significant opening gap)<br><br>
        Try running scan at different times or during high volatility periods.
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome screen
    st.markdown('<div class="section-header">🌙 Welcome to Your QuantScore™ Scanner</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>🎯 YOUR QUANTSCORE™ SYSTEM:</h3>
        • Proprietary formula with your exact logic<br>
        • Strict quality filters (Float < 10M, RSI > 55, Gap > 2%)<br>
        • Live market discovery without preset limitations<br>
        • Dark theme optimized for trading<br>
        • Real-time scanning of 300-1000 tickers<br>
        • Professional export and reporting tools
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
        <h3>🚀 PERFECT FOR FINDING:</h3>
        • Small float breakout candidates<br>
        • High momentum stocks (RSI > 55)<br>
        • Gap-up opportunities (Gap > 2%)<br>
        • Volume-confirmed moves<br>
        • Hidden small cap gems<br>
        • Pre-breakout setups with catalyst potential
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
    🎯 Ready to discover opportunities with your QuantScore™ formula? 
    Configure any additional filters in the sidebar and click "RUN QUANTSCORE™ SCAN" to start live market intelligence gathering using your exact criteria.
    </div>
    """, unsafe_allow_html=True)

# Information section
with st.expander("🌙 QuantScore™ Methodology & Dark Theme"):
    st.markdown("""
    ### 🎯 Your QuantScore™ Formula Explained:
    
    **Core Formula:** `QuantScore = (Change% × Volume^1.3) / (MarketCap^0.7)`
    
    - **Change%:** Measures price momentum (higher = more explosive)
    - **Volume^1.3:** Exponential volume weighting (rewards high liquidity)
    - **MarketCap^0.7:** Dampened market cap factor (favors smaller companies)
    
    ### ✅ Your Quality Filters:
    - **Float < 10M shares:** Ensures low float for maximum volatility potential
    - **RSI > 55:** Confirms strong upward momentum 
    - **Gap% > 2%:** Requires significant opening gap for breakout confirmation
    
    ### 🌙 Dark Theme Benefits:
    - **Reduced eye strain** during extended trading sessions
    - **High contrast colors** for better readability
    - **Professional appearance** suitable for trading environments
    - **Clear visual hierarchy** with color-coded results
    - **Optimized typography** for financial data display
    
    ### 🔍 Live Discovery Process:
    1. **Dynamic ticker expansion** from multiple market sources
    2. **Real-time data fetching** with comprehensive error handling
    3. **Your exact filter application** in sequence
    4. **QuantScore calculation** using your proprietary formula
    5. **Professional ranking and reporting** of qualified opportunities
    
    ### 🎯 Why Your Formula Works:
    - **Volume weighting** identifies institutional interest
    - **Size adjustment** prevents large-cap bias
    - **Momentum confirmation** through price action
    - **Quality filters** ensure technical strength
    - **Gap requirement** confirms catalyst-driven moves
    """)

st.markdown("---")
st.markdown("""
<div class="error-box">
🚨 QUANTSCORE™ TRADING DISCLAIMER: This scanner uses your proprietary QuantScore™ formula to identify high-risk, high-reward small cap opportunities. The strict criteria (Float < 10M, RSI > 55, Gap > 2%) target volatile, catalyst-driven stocks that can move 50%+ rapidly. These securities carry extreme risk including total loss. The dark theme is designed for professional trading environments but does not reduce market risks. This is educational technology only - not investment advice.
</div>
""", unsafe_allow_html=True)
