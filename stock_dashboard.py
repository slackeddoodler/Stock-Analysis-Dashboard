import streamlit as st
import pandas as pd
from openbb import obb
import yfinance as yf
from datetime import datetime, timezone, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta


st.set_page_config(
    page_title="Complete Stock Dashboard",
    page_icon="⭐",
    layout="wide"
)

st.title("Complete Stock Analysis Dashboard")
st.markdown("Powered by OpenBB and yfinance. Compare stocks with Price, Indicators, and Fundamental Data.")


def format_timestamp_distance(ts):
    
    if not ts or pd.isna(ts):
        return "Date not available"
    try:
        
        article_date = pd.to_datetime(ts)
        now = datetime.now(timezone.utc)
        delta = now - article_date

        if delta < timedelta(minutes=1):
            return "Just now"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            return article_date.strftime('%d-%b-%Y')
    except Exception:
        return "Invalid date format"


def display_company_profile(ticker_symbol):
    st.subheader("Company Profile & Key Metrics", anchor=False)
    try:
        
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        st.write(f"**{info.get('longName', 'N/A')}** ({info.get('sector', 'N/A')})")
        st.info(info.get('longBusinessSummary', 'No description available.'))

        col1, col2, col3, col4 = st.columns(4)

        def format_large_number(num):
            if num is None or pd.isna(num): return "N/A"
            if num >= 1_000_000_000_000: return f"${num/1_000_000_000_000:.2f}T"
            if num >= 1_000_000_000: return f"${num/1_000_000_000:.2f}B"
            return f"${num/1_000_000:.2f}M"

        col1.metric("Market Cap", format_large_number(info.get('marketCap')))
        col2.metric("P/E Ratio", f"{info.get('trailingPE'):.2f}" if info.get('trailingPE') else "N/A")
        col3.metric("EPS (TTM)", f"{info.get('trailingEps'):.2f}" if info.get('trailingEps') else "N/A")
        col4.metric("52-Week High", f"${info.get('fiftyTwoWeekHigh'):.2f}" if info.get('fiftyTwoWeekHigh') else "N/A")
    except Exception:
        st.warning(f"Could not retrieve company profile data for {ticker_symbol}.")

def display_recent_news(ticker_symbol):
    
    st.subheader("Recent News", anchor=False)
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        if news:
            with st.expander("View Recent News", expanded=True):
                for article in news[:5]:
                    
                    content = article.get('content', {})
                    if not content:
                        continue

                    title = content.get('title', 'No Title Available')
                    
                    canonical_url = content.get('canonicalUrl', {})
                    link = canonical_url.get('url')

                    publish_time = content.get('pubDate')
                    publish_time_formatted = format_timestamp_distance(publish_time)
                    
                    if link:
                        st.write(f"**[{title}]({link})**")
                    else:
                        st.write(f"**{title}**")
                    st.caption(f"Published: {publish_time_formatted}")
    except Exception:
        st.warning(f"Could not retrieve or parse news for {ticker_symbol}.")


def create_stock_chart(ticker_symbol, start_date, end_date, indicator_choice):
    st.subheader("Price Action and Indicators", anchor=False)
    with st.spinner(f'Loading chart data for {ticker_symbol}...'):
        try:
            openbb_data = obb.equity.price.historical(symbol=ticker_symbol, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'), provider='yfinance')
            data = openbb_data.to_df()
            data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

            if data.empty:
                st.error(f"No price data found for {ticker_symbol}.")
                return

            data.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)
            data.ta.rsi(close='Close', length=14, append=True)

            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.6, 0.2, 0.2])
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price', increasing_line_color='#00b0b9', decreasing_line_color='#d1d4dc'), row=1, col=1)
            bar_colors = ['#00b0b9' if row['Close'] >= row['Open'] else '#d1d4dc' for index, row in data.iterrows()]
            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=bar_colors), row=2, col=1)

            if indicator_choice == 'MACD':
                macd_col, macd_hist_col, macd_signal_col = 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'
                hist_colors = ['#26a69a' if val >= 0 else '#ef5350' for val in data[macd_hist_col]]
                fig.add_trace(go.Bar(x=data.index, y=data[macd_hist_col], name='MACD Hist', marker_color=hist_colors), row=3, col=1)
                fig.add_trace(go.Scatter(x=data.index, y=data[macd_col], name='MACD', mode='lines', line=dict(color='#2962FF', width=1.5)), row=3, col=1)
                fig.add_trace(go.Scatter(x=data.index, y=data[macd_signal_col], name='Signal', mode='lines', line=dict(color='#FF6D00', width=1.5)), row=3, col=1)
                fig.update_yaxes(title_text="MACD", row=3, col=1)
            elif indicator_choice == 'RSI':
                rsi_col = 'RSI_14'
                fig.add_trace(go.Scatter(x=data.index, y=data[rsi_col], name='RSI', mode='lines', line=dict(color='#FFD700', width=1.5)), row=3, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", line_width=1, row=3, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", line_width=1, row=3, col=1)
                fig.update_yaxes(title_text="RSI", row=3, col=1)

            fig.update_layout(height=600, template='plotly_dark', showlegend=False, xaxis_rangeslider_visible=False, yaxis_title='Price (USD)', yaxis2_title='Volume')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred while processing chart for {ticker_symbol}: {e}")

st.sidebar.header('Chart Controls')
ticker_1 = st.sidebar.text_input('Stock Ticker 1', 'AAPL').upper()
ticker_2 = st.sidebar.text_input('Stock Ticker 2', 'MSFT').upper()
indicator_choice = st.sidebar.selectbox('Choose a Secondary Indicator:', ('MACD', 'RSI'))
default_start_date = datetime(2024, 1, 1)
start_date = st.sidebar.date_input('Start Date', default_start_date)
end_date = st.sidebar.date_input('End Date', datetime.now())

if 'chart_generated' not in st.session_state:
    st.session_state.chart_generated = False
if st.sidebar.button('Generate Analysis'):
    st.session_state.chart_generated = True

if st.session_state.chart_generated:
    st.header(f"Analysis for {ticker_1}", divider='rainbow')
    display_company_profile(ticker_1)
    display_recent_news(ticker_1)
    create_stock_chart(ticker_1, start_date, end_date, indicator_choice)

    st.divider()

    st.header(f"Analysis for {ticker_2}", divider='rainbow')
    display_company_profile(ticker_2)
    display_recent_news(ticker_2)
    create_stock_chart(ticker_2, start_date, end_date, indicator_choice)