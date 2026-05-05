#!/usr/bin/env python3
"""Scanner utilities for the real stock alert system."""

import argparse
import json
import tempfile
from pathlib import Path

import pandas as pd
import requests


CACHE_DIR = Path(tempfile.gettempdir()) / "real_stock_strategy_cache"
PERIOD1 = 1262304000
PERIOD2 = 4102444800

UNIVERSE = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "AVGO", "TSLA", "NFLX",
    "AMD", "COST", "ADBE", "CRM", "ORCL", "CSCO", "INTC", "QCOM", "TXN", "AMAT",
    "LRCX", "MU", "KLAC", "ADI", "PANW", "CRWD", "DDOG", "ZS", "MDB", "SNOW",
    "SHOP", "UBER", "ABNB", "PLTR", "APP", "ARM", "SMCI", "MRVL", "ASML", "CDNS",
    "SNPS", "INTU", "ISRG", "BKNG", "MELI", "VRTX", "REGN", "AMGN", "GILD", "ADP",
    "MAR", "SBUX", "PEP", "LIN", "WMT",
]


def fetch_yahoo_chart(ticker):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe = ticker.lower().replace("^", "")
    cache_path = CACHE_DIR / f"{safe}_history.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    response = requests.get(
        f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}",
        params={
            "period1": PERIOD1,
            "period2": PERIOD2,
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true",
        },
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    payload = response.json()
    cache_path.write_text(json.dumps(payload))
    return payload


def add_indicators(df):
    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
    df["VOL20"] = df["Volume"].rolling(20).mean()
    df["RET20"] = df["Close"] / df["Close"].shift(20) - 1
    df["RET63"] = df["Close"] / df["Close"].shift(63) - 1
    prev_close = df["Close"].shift(1)
    true_range = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - prev_close).abs(),
            (df["Low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    df["ATR14"] = true_range.rolling(14).mean()
    return df.dropna()


def load_prices(ticker):
    payload = fetch_yahoo_chart(ticker)
    result = payload["chart"]["result"][0]
    timestamps = result.get("timestamp") or []
    if not timestamps:
        raise RuntimeError(f"No data for {ticker}")

    quote = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose")
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(timestamps, unit="s")
            .tz_localize("UTC")
            .tz_convert("America/New_York")
            .date,
            "Open": quote["open"],
            "High": quote["high"],
            "Low": quote["low"],
            "Close": quote["close"],
            "AdjClose": adjclose or quote["close"],
            "Volume": quote["volume"],
        }
    ).dropna()

    factor = df["AdjClose"] / df["Close"]
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = df[col] * factor

    return add_indicators(df[["Date", "Open", "High", "Low", "Close", "Volume"]].set_index("Date"))


def load_universe(tickers):
    data = {}
    errors = []
    for ticker in tickers:
        try:
            data[ticker] = load_prices(ticker)
        except Exception as exc:
            errors.append({"ticker": ticker, "error": str(exc)})
    qqq = load_prices("QQQ")
    return data, qqq, errors


def latest_common_date(data, qqq):
    dates = set(qqq.index)
    for df in data.values():
        dates &= set(df.index)
    if not dates:
        raise RuntimeError("No common market date found")
    return max(dates)


def market_filter(qqq, date):
    row = qqq.loc[date]
    return {
        "close": float(row["Close"]),
        "sma200": float(row["SMA200"]),
        "market_on": bool(row["Close"] > row["SMA200"]),
    }


def initial_stop(close, atr14):
    return max(close * 0.88, close - 2.5 * atr14)


def trailing_stop(highest_high, atr14):
    return max(highest_high * 0.85, highest_high - 3.0 * atr14)


def candidate_for(data, qqq, ticker, date):
    if ticker not in data or date not in data[ticker].index or date not in qqq.index:
        return None

    row = data[ticker].loc[date]
    qrow = qqq.loc[date]
    market_ok = qrow["Close"] > qrow["SMA200"]
    trend_ok = row["Close"] > row["SMA50"] > row["SMA200"]
    liquid = row["Close"] * row["VOL20"] > 50_000_000
    rs63 = row["RET63"] - qrow["RET63"]
    above_sma50 = row["Close"] / row["SMA50"] - 1

    if not (market_ok and trend_ok and liquid and rs63 > 0):
        return None

    score = rs63 * 100 + row["RET20"] * 35 + above_sma50 * 20
    close = float(row["Close"])
    atr14 = float(row["ATR14"])
    return {
        "ticker": ticker,
        "close": close,
        "score": float(score),
        "rs63": float(rs63),
        "ret63": float(row["RET63"]),
        "ret20": float(row["RET20"]),
        "above_sma50": float(above_sma50),
        "sma50": float(row["SMA50"]),
        "sma200": float(row["SMA200"]),
        "atr14": atr14,
        "initial_stop": float(initial_stop(close, atr14)),
        "avg_dollar_volume": float(row["Close"] * row["VOL20"]),
    }


def scan_candidates(data, qqq, date, max_positions=2):
    candidates = []
    for ticker in data:
        signal = candidate_for(data, qqq, ticker, date)
        if signal:
            candidates.append(signal)
    return sorted(candidates, key=lambda item: item["score"], reverse=True)[:max_positions]


def position_exit_status(position, data, qqq, date, top_tickers):
    ticker = position["ticker"]
    if ticker not in data or date not in data[ticker].index:
        return None

    row = data[ticker].loc[date]
    qrow = qqq.loc[date]
    highest_high = max(float(position.get("highest_high_since_entry", position["entry_price"])), float(row["High"]))
    new_stop = max(float(position.get("stop", 0.0)), trailing_stop(highest_high, float(row["ATR14"])))
    reasons = []
    if qrow["Close"] <= qrow["SMA200"]:
        reasons.append("QQQ below SMA200")
    if row["Close"] < row["EMA21"]:
        reasons.append("close below EMA21")
    if row["Close"] < row["SMA50"]:
        reasons.append("close below SMA50")
    if row["Low"] <= new_stop:
        reasons.append("trailing stop hit")
    if top_tickers and ticker not in top_tickers:
        reasons.append("dropped out of weekly top list")

    return {
        "ticker": ticker,
        "date": date.isoformat(),
        "close": float(row["Close"]),
        "ema21": float(row["EMA21"]),
        "sma50": float(row["SMA50"]),
        "highest_high_since_entry": highest_high,
        "stop": float(new_stop),
        "sell": bool(reasons),
        "reasons": reasons,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-positions", type=int, default=2)
    args = parser.parse_args()
    data, qqq, errors = load_universe(UNIVERSE)
    date = latest_common_date(data, qqq)
    candidates = scan_candidates(data, qqq, date, args.max_positions)
    print(f"Scan date: {date}")
    print(f"Data errors: {len(errors)}")
    for idx, candidate in enumerate(candidates, start=1):
        print(
            f"{idx}. {candidate['ticker']} close={candidate['close']:.2f} "
            f"stop={candidate['initial_stop']:.2f} score={candidate['score']:.2f}"
        )


if __name__ == "__main__":
    main()

