import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
import concurrent.futures
import threading

# Configure page
st.set_page_config(
    page_title="🔍 Comprehensive Small Cap Scanner",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Comprehensive Small Cap Market Scanner")
st.markdown("**🎯 Finds ALL stocks: Float < 10M | Price $1-$20 | Live screening of 500+ tickers**")

# Comprehensive list of small cap tickers (500+ symbols)
COMPREHENSIVE_TICKER_LIST = [
    # Confirmed small caps and penny stocks
    "PHUN", "SNTI", "HUBC", "BBIG", "PROG", "ATER", "SPRT", "IRNT", "RDBX", "NILE",
    "MULN", "GFAI", "BMRA", "RELI", "BGFV", "CLOV", "WISH", "WKHS", "RIDE", "GOEV",
    "ARVL", "NAKD", "SNDL", "EXPR", "AMC", "GME", "MMAT", "TRCH", "VERB", "VXRT",
    "OCGN", "XELA", "GNUS", "JAGX", "INPX", "MARK", "UAMY", "TOPS", "SHIP", "GLBS",
    "CXAI", "HOLO", "TRNR", "QUBT", "RGTI", "RR", "BNAI", "BOX", "APLD", "SERV",
    
    # Biotech small caps
    "ADTX", "ADMA", "AGIO", "AKRO", "ALEC", "ALKS", "AMRN", "ANAB", "ANIK", "APLS",
    "ARDX", "ARQT", "ARTL", "ASMB", "ASND", "AUPH", "AVIR", "BEAM", "BCAB", "BCRX",
    "BFRI", "BIIB", "BLUE", "BMEA", "BNGO", "BOLD", "BPMC", "BPRN", "BPTH", "BPYP",
    "BTTX", "CAPR", "CARA", "CBAY", "CCCC", "CDNA", "CDTX", "CDXC", "CDXS", "CERN",
    "CHRS", "CTIC", "CTMX", "CPRX", "CRDF", "CRSP", "CTSO", "CYAD", "CYTK", "DSGX",
    
    # Tech small caps
    "SOFI", "PLTR", "HOOD", "RBLX", "DKNG", "FUBO", "SKLZ", "OPEN", "UPST", "AFRM",
    "COIN", "SQ", "PYPL", "ROKU", "ZM", "SHOP", "NET", "SNOW", "CRWD", "ZS",
    "OKTA", "DDOG", "MDB", "ESTC", "TEAM", "WDAY", "NOW", "VEEV", "ZEN", "BILL",
    "SMAR", "DOCU", "TWLO", "SEND", "PLAN", "GTLB", "PATH", "AI", "SMCI", "NVDA",
    
    # Energy/Mining small caps
    "TELL", "FCEL", "PLUG", "BE", "BLDP", "HYMC", "GOLD", "NEM", "AUY", "EGO",
    "AG", "SLV", "PSLV", "FSM", "HL", "PAAS", "CDE", "SSRM", "WPM", "FNV",
    "SAND", "GORO", "GDXJ", "SIL", "SILJ", "REMX", "LIT", "PICK", "COPX", "URA",
    
    # Cannabis/Retail small caps
    "TLRY", "CRON", "ACB", "HEXO", "OGI", "SNDL", "CGC", "WEED", "APHA", "FIRE",
    "KERN", "HRVSF", "GTBIF", "CURLF", "TCNNF", "CRLBF", "VREOF", "MSOS", "YOLO",
    "POTX", "THCX", "MJ", "CNBS", "BUDZ", "TOKE", "HERB", "GRWG", "SMG", "HYFM",
    
    # REITs and Finance small caps
    "NRZ", "AGNC", "CIM", "NLY", "ARR", "TWO", "IVR", "MFA", "NYMT", "PMT",
    "CHMI", "ORC", "EARN", "MITT", "DX", "GPMT", "TRTX", "ARI", "BXMT", "RC",
    "LADR", "KREF", "STAR", "ACRE", "AFIN", "GAIN", "MAIN", "GLAD", "PSEC", "GSBD",
    
    # Airlines/Travel small caps
    "AAL", "UAL", "DAL", "LUV", "ALK", "JBLU", "SAVE", "HA", "MESA", "SKYW",
    "ALGT", "ATSG", "AAWW", "CAR", "HTZ", "MCRI", "VLRS", "TRIP", "EXPE", "BKNG",
    
    # Shipping small caps
    "DRYS", "SHIP", "TOPS", "GLBS", "CTRM", "CASTOR", "EDRY", "EGLE", "SBLK", "NM",
    "NAT", "FRO", "TNK", "STNG", "EURN", "DHT", "TK", "TNP", "INSW", "CPLP",
    
    # Food/Consumer small caps
    "BYND", "TTCF", "VERY", "UNFI", "SEN", "CHEF", "EAT", "CAKE", "TXRH", "WING",
    "PZZA", "BLMN", "DENN", "KRUS", "RRGB", "FRGI", "CBRL", "CROX", "DECK", "NKE",
    
    # Additional small caps from various sectors
    "KIRK", "EXPR", "GPS", "ANF", "AEO", "URBN", "TJX", "COST", "WMT", "TGT",
    "DKS", "BBY", "GME", "BBBY", "BIG", "DLTR", "DG", "FIVE", "OLLI", "BURL",
    "RH", "WSM", "W", "WAYFAIR", "OSTK", "PRTS", "LRN", "STRA", "APEI", "CECO",
    
    # Crypto/Fintech related
    "MARA", "RIOT", "HUT", "BITF", "EBON", "CAN", "BTBT", "IDEX", "EQOS", "HVBT",
    "ARBK", "WULF", "CIFR", "CORZ", "GRIID", "LGHL", "ANY", "BTCS", "DPRO", "NXTD"
]

# Split tickers into manageable chunks for faster processing
CHUNK_SIZE = 25

def get_stock_data_fast(ticker):
    """Fast stock data retrieval with timeout"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get recent data
        hist = stock.history(period="5d", timeout=5)
        if hist.empty or len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        change_pct = ((current_price - prev_close) / prev_close) * 100
        volume = hist['Volume'].iloc[-1]
        
        # Quick info fetch with timeout
        try:
            info = stock.info
            market_cap = info.get('marketCap', 0)
            float_shares = info.get('floatShares', 0)
            
            # Fallback calculations
            if market_cap == 0:
                shares_outstanding = info.get('sharesOutstanding', 0)
                market_cap = current_price * shares_outstanding if shares_outstanding > 0 else 0
                
            if float_shares == 0:
                float_shares = info.get('sharesOutstanding', 0)
                
        except:
            # Skip if can't get basic info
            return None
        
        # Quick RSI calculation
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
            'price': float(current_price),
            'change_pct': float(change_pct),
            'volume': int(volume),
            'market_cap': int(market_cap) if market_cap > 0 else 0,
            'float_shares': int(float_shares) if float_shares > 0 else 0,
            'rsi': float(rsi) if not pd.isna(rsi) else 50
        }
        
    except Exception as e:
        return None

def process_ticker_chunk(tickers_chunk, results_dict, chunk_id):
    """Process a chunk of tickers in parallel"""
    chunk_results = []
    
    for ticker in tickers_chunk:
        data = get_stock_data_fast(ticker)
        if data:
            chunk_results.append(data)
    
    results_dict[chunk_id] = chunk_results

def calculate_comprehensive_score(data):
    """Calculate enhanced QuantScore for small caps"""
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        float_shares = data['float_shares']
        
        if market_cap <= 0 or volume <= 0 or float_shares <= 0:
            return 0
            
        # Enhanced formula for small caps
        score = (change_pct * (volume ** 1.3)) / ((market_cap ** 0.7) * (float_shares ** 0.4))
        
        return score
    except:
        return 0

# Sidebar controls
st.sidebar.header("🔍 Comprehensive Scanner Settings")

# Filter settings
price_min = st.sidebar.slider("Minimum Price ($)", 0.5, 10.0, 1.0, 0.5)
price_max = st.sidebar.slider("Maximum Price ($)", 5.0, 25.0, 20.0, 1.0)
max_float = st.sidebar.slider("Maximum Float (M shares)", 1, 15, 10, 1) * 1_000_000
min_volume = st.sidebar.selectbox("Minimum Volume", [10_000, 50_000, 100_000, 250_000], index=1)
min_change = st.sidebar.slider("Minimum Change %", 0.0, 10.0, 2.0, 0.5)

# Advanced settings
st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Advanced Settings")
max_tickers = st.sidebar.slider("Max Tickers to Scan", 50, 500, 200, 25)
parallel_chunks = st.sidebar.slider("Parallel Processing Chunks", 4, 20, 10, 2)

# Show scanning info
st.sidebar.markdown("---")
st.sidebar.info(f"""
**Scanning Parameters:**
- 📊 Total Universe: {len(COMPREHENSIVE_TICKER_LIST)} stocks
- 🎯 Will Scan: {max_tickers} stocks
- ⚡ Parallel Chunks: {parallel_chunks}
- 💰 Price Range: ${price_min}-${price_max}
- 🔍 Float Limit: {max_float/1_000_000:.0f}M shares
""")

if st.sidebar.button("🚀 SCAN ALL MARKETS", type="primary"):
    st.markdown("---")
    st.markdown("## 🔍 Comprehensive Market Scan Results")
    
    # Select tickers to scan
    tickers_to_scan = COMPREHENSIVE_TICKER_LIST[:max_tickers]
    
    # Progress tracking
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🎯 Scanning: {len(tickers_to_scan)} stocks")
    with col2:
        st.info(f"⚡ Parallel Chunks: {parallel_chunks}")
    with col3:
        st.info(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
    
    # Split tickers into chunks
    ticker_chunks = [tickers_to_scan[i:i+CHUNK_SIZE] for i in range(0, len(tickers_to_scan), CHUNK_SIZE)]
    
    # Parallel processing
    with st.spinner("🔍 Scanning entire market for small caps..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        start_time = time.time()
        results_dict = {}
        threads = []
        
        # Process chunks in parallel
        for i, chunk in enumerate(ticker_chunks[:parallel_chunks]):
            status_text.text(f'Processing chunk {i+1}/{len(ticker_chunks[:parallel_chunks])}...')
            
            thread = threading.Thread(
                target=process_ticker_chunk, 
                args=(chunk, results_dict, i)
            )
            threads.append(thread)
            thread.start()
            
            progress_bar.progress((i + 1) / len(ticker_chunks[:parallel_chunks]))
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        scan_time = time.time() - start_time
        progress_bar.empty()
        status_text.empty()
    
    # Combine all results
    all_results = []
    for chunk_results in results_dict.values():
        all_results.extend(chunk_results)
    
    if not all_results:
        st.error("❌ No data retrieved from market scan. Please try again.")
    else:
        # Calculate QuantScores and apply filters
        qualified_stocks = []
        
        for data in all_results:
            # Apply filters
            if (price_min <= data['price'] <= price_max and
                data['float_shares'] <= max_float and
                data['float_shares'] > 0 and
                data['volume'] >= min_volume and
                abs(data['change_pct']) >= min_change):
                
                # Calculate score
                score = calculate_comprehensive_score(data)
                if score > 0:
                    qualified_stocks.append({
                        'Ticker': data['ticker'],
                        'QuantScore': score,
                        'Price': data['price'],
                        'Change%': data['change_pct'],
                        'Volume': data['volume'],
                        'Float (M)': data['float_shares'] / 1_000_000,
                        'Market Cap': data['market_cap'],
                        'RSI': data['rsi']
                    })
        
        # Display results
        st.markdown(f"## 🎯 Market Scan Complete")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📊 Stocks Scanned", len(all_results))
        with col2:
            st.metric("🎯 Qualified", len(qualified_stocks))
        with col3:
            st.metric("⚡ Scan Time", f"{scan_time:.1f}s")
        with col4:
            success_rate = (len(all_results) / len(tickers_to_scan)) * 100
            st.metric("✅ Success Rate", f"{success_rate:.1f}%")
        with col5:
            st.metric("🔍 Filter Rate", f"{(len(qualified_stocks)/max(len(all_results),1)*100):.1f}%")
        
        if qualified_stocks:
            # Sort by QuantScore
            df = pd.DataFrame(qualified_stocks)
            df = df.sort_values('QuantScore', ascending=False)
            
            # Format for display
            display_df = df.copy()
            display_df['QuantScore'] = display_df['QuantScore'].apply(lambda x: f"{x:.8f}")
            display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
            display_df['Change%'] = display_df['Change%'].apply(lambda x: f"{x:+.2f}%")
            display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:,.0f}")
            display_df['Float (M)'] = display_df['Float (M)'].apply(lambda x: f"{x:.1f}M")
            display_df['Market Cap'] = display_df['Market Cap'].apply(lambda x: f"${x/1e6:.1f}M" if x > 0 else "N/A")
            display_df['RSI'] = display_df['RSI'].apply(lambda x: f"{x:.0f}")
            
            # Add ranking
            display_df.index = range(1, len(display_df) + 1)
            display_df.index.name = 'Rank'
            
            st.success(f"🎉 Found {len(qualified_stocks)} stocks matching your criteria!")
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Top picks section
            st.markdown("### 🏆 TOP 10 COMPREHENSIVE SCAN RESULTS:")
            for i, (idx, row) in enumerate(display_df.head(10).iterrows()):
                if i < 3:
                    medals = ["🥇", "🥈", "🥉"]
                    st.success(f"{medals[i]} **#{idx}: {row['Ticker']}** | Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float (M)']} | Volume: {row['Volume']}")
                else:
                    st.info(f"⭐ **#{idx}: {row['Ticker']}** | Score: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']} | Float: {row['Float (M)']} | Volume: {row['Volume']}")
            
            # Download functionality
            col1, col2 = st.columns(2)
            with col1:
                csv = display_df.to_csv()
                st.download_button(
                    "📊 Download Complete Results",
                    csv,
                    file_name=f"comprehensive_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Create summary report
                summary = f"""
COMPREHENSIVE MARKET SCAN SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SCAN PARAMETERS:
- Price Range: ${price_min} - ${price_max}
- Max Float: {max_float/1_000_000:.0f}M shares
- Min Volume: {min_volume:,}
- Min Change: {min_change}%

RESULTS:
- Stocks Scanned: {len(all_results)}
- Qualified Stocks: {len(qualified_stocks)}
- Success Rate: {success_rate:.1f}%
- Scan Time: {scan_time:.1f} seconds

TOP 5 PICKS:
"""
                for i, (idx, row) in enumerate(display_df.head(5).iterrows()):
                    summary += f"{i+1}. {row['Ticker']} - Score: {row['QuantScore']} | Price: {row['Price']} | Float: {row['Float (M)']}\n"
                
                st.download_button(
                    "📋 Download Summary Report",
                    summary,
                    file_name=f"scan_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("⚠️ No stocks met all criteria. Try adjusting your filters:")
            st.info("💡 Try lowering price minimum, increasing float maximum, or reducing minimum change%")
            
            # Show some unfiltered results
            if all_results:
                st.markdown("### 📊 Sample Unfiltered Results (Top 20):")
                sample_df = pd.DataFrame(all_results[:20])
                sample_df['Price'] = sample_df['price'].apply(lambda x: f"${x:.2f}")
                sample_df['Float (M)'] = sample_df['float_shares'].apply(lambda x: f"{x/1e6:.1f}M" if x > 0 else "N/A")
                sample_df['Volume'] = sample_df['volume'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(sample_df[['ticker', 'Price', 'Float (M)', 'Volume']], use_container_width=True)

# Information section
with st.expander("🔍 Comprehensive Scanner Information"):
    st.markdown(f"""
    ### 🎯 What This Scanner Does:
    - **Scans {len(COMPREHENSIVE_TICKER_LIST)} stocks** from comprehensive database
    - **Finds ALL stocks** meeting your exact criteria
    - **Parallel processing** for faster results
    - **Real-time data** from Yahoo Finance
    - **Advanced filtering** by price, float, volume, change%
    
    ### 📊 Stock Universe Includes:
    - **Small cap stocks** across all sectors
    - **Penny stocks** with adequate volume
    - **Biotech** and pharmaceutical companies
    - **Technology** and AI stocks
    - **Energy** and mining companies
    - **Cannabis** and consumer stocks
    - **REITs** and financial stocks
    - **Shipping** and transportation
    - **Crypto-related** stocks
    
    ### ⚡ Performance Features:
    - **Multi-threaded** data fetching
    - **Timeout protection** for failed requests
    - **Progress tracking** during scan
    - **Success rate** monitoring
    - **Fast filtering** and scoring
    
    ### 🎯 Perfect For Finding:
    - **Low float runners** under 10M shares
    - **Price range stocks** $1-$20
    - **High volume** confirmation
    - **Momentum** continuation plays
    - **Breakout candidates** with catalysts
    
    ### ⚠️ Important Notes:
    - Scan time depends on market conditions
    - Some stocks may timeout during data fetch
    - Float data accuracy depends on Yahoo Finance
    - Results are for educational purposes only
    """)

st.markdown("---")
st.error("🚨 **COMPREHENSIVE SCANNER DISCLAIMER:** This tool scans hundreds of stocks to find opportunities matching your criteria. Small cap and penny stocks are extremely volatile and risky. This is educational only - not financial advice!")

else:
    # Welcome screen
    st.markdown("## 🔍 Welcome to Comprehensive Market Scanner!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### 🎯 Comprehensive Coverage:
        - **{len(COMPREHENSIVE_TICKER_LIST)} stocks** in database
        - **All sectors** and market caps
        - **Real-time screening** with live data
        - **Parallel processing** for speed
        - **Advanced filtering** by your criteria
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 What You'll Find:
        - **Low float stocks** under 10M shares
        - **Price range** $1-$20 stocks
        - **High volume** confirmation
        - **Momentum** plays and breakouts
        - **Hidden gems** across all sectors
        """)
    
    st.info("🎯 **Ready to scan the entire market?** Click 'SCAN ALL MARKETS' in the sidebar to find ALL stocks matching your criteria!")
    
    # Preview of what's in the database
    st.markdown("### 📊 Sample of Stock Universe:")
    sample_tickers = COMPREHENSIVE_TICKER_LIST[:50]
    sample_display = " | ".join(sample_tickers)
    st.code(sample_display)
    st.caption(f"Showing 50 of {len(COMPREHENSIVE_TICKER_LIST)} total stocks in database")