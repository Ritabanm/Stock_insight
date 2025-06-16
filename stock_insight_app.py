
import streamlit as st
import requests
from newspaper import Article
from textblob import TextBlob

st.set_page_config(page_title="AI Finance Dashboard", layout="centered")
st.title("📊 AI-Powered Stock & News Insight")

# --------------------------
# TICKER DROPDOWN
# --------------------------
st.subheader("📈 Real-Time Stock Quote")

tickers = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Google": "GOOGL",
    "Meta (Facebook)": "META",
    "Netflix": "NFLX"
}

company = st.selectbox("Choose a stock:", list(tickers.keys()))
symbol = tickers[company]
api_key = "demo"  # Replace with your API key

url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=DT0GK2o268NexFPt2TqAnxenH3H3iRHK"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data:
        quote = data[0]
        st.metric(label="Current Price", value=f"${quote['price']:.2f}", delta=f"{quote['change']} ({quote['changesPercentage']}%)")
        st.write(f"**Day Range:** ${quote['dayLow']} - ${quote['dayHigh']}")
        st.write(f"**Volume:** {quote['volume']}")
        st.write(f"**Market Cap:** ${quote['marketCap']:,}")
    else:
        st.warning("No data found.")
else:
    st.error(f"API call failed (Status Code: {response.status_code})")

# --------------------------
# NEWS IMPACT ANALYSIS
# --------------------------
st.divider()
st.subheader("📰 Analyze News Article Impact")

news_url = st.text_input("Paste a news article URL to estimate stock impact")

if news_url:
    try:
        article = Article(news_url)
        article.download()
        article.parse()
        article.nlp()

        st.markdown("**🧾 Article Summary:**")
        st.write(article.summary)

        # Sentiment analysis
        analysis = TextBlob(article.text)
        polarity = analysis.sentiment.polarity

        if polarity > 0.1:
            sentiment = "📈 Likely Positive Impact"
        elif polarity < -0.1:
            sentiment = "📉 Likely Negative Impact"
        else:
            sentiment = "🔍 Neutral or Unclear Impact"

        st.subheader("📊 Sentiment Analysis")
        st.write(f"**Polarity Score:** `{polarity:.2f}`")
        st.success(sentiment)

    except Exception as e:
        st.error(f"⚠️ Failed to process article: {e}")
