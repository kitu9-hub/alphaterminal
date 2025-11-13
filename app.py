# app.py — Real, working AlphaTerminal (v1.1)
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 🎨 Page config
st.set_page_config(
    page_title="AlphaTerminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌓 Dark theme toggle
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5b/Bloomberg_logo.svg", width=120)
    st.title("🚀 AlphaTerminal")
    st.caption("Elite Investing OS — v1.1")
    theme = st.radio("Theme", ["Dark", "Light"], index=0)
    if theme == "Dark":
        st.markdown("""
        <style>
        :root { color-scheme: dark; }
        .stApp { background-color: #0e1117; color: white; }
        </style>
        """, unsafe_allow_html=True)

# 📊 Market Data
st.header("🌐 Market Pulse")
cols = st.columns(4)

indices = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "VIX": "^VIX",
    "10Y Treasury": "^TNX"
}

for col, (name, ticker) in zip(cols, indices.items()):
    try:
        data = yf.Ticker(ticker).history(period="2d")["Close"]
        if len(data) >= 2:
            current = data.iloc[-1]
            prev = data.iloc[-2]
            change = (current - prev) / prev * 100
            col.metric(
                name,
                f"{current:.2f}" if "Treasury" not in name else f"{current:.2f}%",
                f"{change:+.2f}%"
            )
        else:
            col.metric(name, "—", "")
    except:
        col.metric(name, "ERR", "")

# 📈 Watchlist Chart
st.subheader("📈 Live Chart")
watchlist = st.multiselect(
    "Add tickers (e.g., NVDA, BTC-USD, TLT)",
    ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "BTC-USD", "GLD", "TLT"],
    default=["SPY", "QQQ"]
)

timeframe = st.selectbox("Timeframe", ["1d", "5d", "1mo", "3mo", "1y"], index=2)

if watchlist:
    data = yf.download(watchlist, period=timeframe)
    if len(watchlist) == 1:
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close']
        )])
        fig.update_layout(title=watchlist[0], xaxis_rangeslider_visible=False)
    else:
        fig = go.Figure()
        for ticker in watchlist:
            if ('Close', ticker) in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Close'][ticker],
                    mode='lines',
                    name=ticker
                ))
        fig.update_layout(title="Comparison")

    st.plotly_chart(fig, use_container_width=True)

# 💡 Edge Tip
st.info("💡 Pro Tip: The top 0.00001% focus on *free cash flow yield*, not P/E. Try screening for FCF/EV > 8%.")

# 🔗 Footer
st.markdown("---")
st.caption(f"✅ Running live • Updated: {datetime.now():%Y-%m-%d %H:%M} UTC • [GitHub](https://github.com/yourname/alphaterminal)")
