
import yfinance as yf
import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def analyze_stock(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="5y")
        if hist.empty:
            return None

        close = hist["Close"]
        price = close.iloc[-1]
        rsi = calculate_rsi(close).iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]
        sma200 = close.rolling(200).mean().iloc[-1]

        info = ticker.info
        score = 0
        if price > sma50: score += 20
        if sma50 > sma200: score += 20
        if rsi < 30: score += 20
        if info.get("returnOnEquity", 0) > 0.15: score += 20
        if info.get("debtToEquity", 2) < 1: score += 20

        return {
            "ticker": ticker_symbol,
            "price": round(price, 2),
            "dayChange": round(info.get("regularMarketChangePercent", 0), 2),
            "sector": info.get("sector", "Unknown"),
            "score": min(score, 100)
        }
    except Exception:
        return None
