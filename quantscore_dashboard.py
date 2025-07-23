import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time

st.set_page_config(
    page_title="QuantScore™ Live Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 QuantScore™ Live Dashboard")
st.markdown("**Real-time stock screening for high-momentum breakout opportunities**")

st.sidebar.header("⚙️ Configuration")

default_tickers = ["AAPL", "TSLA", "NVDA", "AMD", "MSFT", "GOOGL", "META", "AMZN", "NFLX", "CRM"]

ticker_input = st.sidebar.text_area(
    "📈 Stock Tickers (one per line)",
    value="\n".join(default_tickers),
    height=200
)

tickers = [t.strip().upper() for t in ticker_input.split('\n') if t.strip()]

alpha = st.sidebar.slider("Alpha (Volume exponent)", 0.5, 2.0, 1.3, 0.1)
beta = st.sidebar.slider("Beta (MarketCap exponent)", 0.3, 1.5, 0.7, 0.1) 
change_min = st.sidebar.slider("Minimum Change %", 0.0, 10.0, 2.0, 0.5)

def calculate_simple_rsi(prices, window=14):
    if len(prices) < window + 1:
        return 50
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")
        info = stock.info
        
        if hist.empty or len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        change_pct = ((current_price - prev_close) / prev_close) * 100
        volume = hist['Volume'].iloc[-1]
        market_cap = info.get('marketCap', 1000000000)
        
        rsi = calculate_simple_rsi(hist['Close'])
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'change_pct': change_pct,
            'volume': volume,
            'market_cap': market_cap,
            'rsi': rsi
        }
    except Exception as e:
        st.warning(f"⚠️ Could not fetch data for {ticker}")
        return None

def calculate_quant_score(data, alpha, beta):
    try:
        change_pct = abs(data['change_pct'])
        volume = data['volume']
        market_cap = data['market_cap']
        
        if market_cap <= 0 or volume <= 0:
            return 0
            
        score = (change_pct * (volume ** alpha)) / (market_cap ** beta)
        return score
    except:
        return 0

def format_number(num, is_currency=False, is_percentage=False):
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

if st.sidebar.button("🚀 Run QuantScore Analysis", type="primary"):
    if not tickers:
        st.error("Please enter at least one ticker")
    else:
        st.markdown("---")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for i, ticker in enumerate(tickers):
            status_text.text(f'Analyzing {ticker}...')
            progress_bar.progress((i + 1) / len(tickers))
            
            data = get_stock_data(ticker)
            if data:
                quant_score = calculate_quant_score(data, alpha, beta)
                data['quant_score'] = quant_score
                results.append(data)
            
            time.sleep(0.2)
        
        progress_bar.empty()
        status_text.empty()
        
        if results:
            df = pd.DataFrame(results)
            
            filtered_df = df[
                (df['change_pct'].abs() > change_min) &
                (df['quant_score'] > 0)
            ].sort_values('quant_score', ascending=False)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Stocks Analyzed", len(df))
            with col2:
                st.metric("Passed Filters", len(filtered_df))
            with col3:
                st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
            
            st.markdown("## 🏆 Top QuantScore Rankings")
            
            display_df = filtered_df if not filtered_df.empty else df.sort_values('quant_score', ascending=False)
            
            if display_df.empty:
                st.warning("No data found")
            else:
                formatted_df = display_df.copy()
                formatted_df['Price'] = formatted_df['current_price'].apply(lambda x: format_number(x, is_currency=True))
                formatted_df['Change%'] = formatted_df['change_pct'].apply(lambda x: format_number(x, is_percentage=True))
                formatted_df['Volume'] = formatted_df['volume'].apply(format_number)
                formatted_df['Market Cap'] = formatted_df['market_cap'].apply(format_number)
                formatted_df['RSI'] = formatted_df['rsi'].apply(lambda x: f"{x:.1f}")
                formatted_df['QuantScore'] = formatted_df['quant_score'].apply(lambda x: f"{x:.8f}")
                
                display_cols = ['ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 'Market Cap', 'RSI']
                final_df = formatted_df[display_cols].copy()
                final_df.columns = ['Ticker', 'QuantScore', 'Price', 'Change%', 'Volume', 'Market Cap', 'RSI']
                
                final_df.index = range(1, len(final_df) + 1)
                final_df.index.name = 'Rank'
                
                st.dataframe(final_df, use_container_width=True)
                
                csv = final_df.to_csv()
                st.download_button(
                    "📄 Download Results",
                    csv,
                    file_name=f"quantscore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                if len(final_df) > 0:
                    st.markdown("### 🎯 Top 3 Picks:")
                    for i, (idx, row) in enumerate(final_df.head(3).iterrows()):
                        st.success(f"**#{idx}: {row['Ticker']}** - QuantScore: {row['QuantScore']} | Price: {row['Price']} | Change: {row['Change%']}")
        else:
            st.error("No data retrieved. Check your tickers and try again.")

with st.expander("🧮 QuantScore Formula"):
    st.markdown(f"""
    **Formula:** QuantScore = (|Change%| × Volume^{alpha}) / (MarketCap^{beta})
    
    **Current Settings:**
    - Alpha (Volume exponent): {alpha}
    - Beta (MarketCap exponent): {beta}
    - Minimum Change%: {change_min}%
    
    **Data Source:** Yahoo Finance (Real-time)
    """)

st.markdown("---")
st.info("💡 **Tip:** Higher QuantScore = Better opportunity. Use during market hours for best results.")
st.warning("⚠️ **Disclaimer:** For educational purposes only. Not financial advice.")

current_hour = datetime.now().hour
if 9 <= current_hour <= 16:
    st.success("🟢 **Market Status:** OPEN")
else:
    st.info("🔴 **Market Status:** CLOSED")
