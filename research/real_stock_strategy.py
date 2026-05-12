#!/usr/bin/env python3
"""Scanner utilities for the real stock alert system."""

import argparse
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
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

EXPANDED_GROWTH_UNIVERSE = sorted(set(UNIVERSE + [
    "AFRM", "AI", "ALAB", "ALGN", "ANET", "APLD", "ARKK", "ASTS", "AXON", "BABA",
    "BIDU", "BILI", "BILL", "BMBL", "BROS", "CAVA", "CELH", "CHWY", "COIN", "DASH",
    "DOCU", "DUOL", "ELF", "ENPH", "ETSY", "FSLR", "FUTU", "GME", "HOOD", "HIMS",
    "IONQ", "IOT", "JOBY", "LCID", "MARA", "MNDY", "NET", "NIO", "OKTA", "ON",
    "PATH", "PINS", "RBLX", "RDDT", "RIVN", "ROKU", "SE", "SEDG", "S", "SOFI",
    "SOUN", "SPOT", "TOST", "TTD", "TWLO", "UPST", "VRT", "WBD", "WDC", "XYZ",
    "XPEV", "ZM",
]))

EXPANDED_WITH_ETFS_UNIVERSE = sorted(set(EXPANDED_GROWTH_UNIVERSE + [
    "ARKG", "ARKW", "BOTZ", "CIBR", "IBB", "IGV", "IWM", "KWEB", "QQQ", "SMH",
    "SOXL", "TAN", "TECL", "TQQQ", "URA", "XBI", "XLE", "XLF", "XLK", "XLV",
]))

SECTOR_GROUPS = {
    "semis": {
        "NVDA", "AMD", "AVGO", "INTC", "QCOM", "TXN", "AMAT", "LRCX", "MU", "KLAC",
        "ADI", "MRVL", "ASML", "ARM", "SMCI", "ON", "WDC",
    },
    "software": {
        "MSFT", "ADBE", "CRM", "ORCL", "PANW", "CRWD", "DDOG", "ZS", "MDB", "SNOW",
        "PLTR", "APP", "CDNS", "SNPS", "INTU", "SHOP", "NET", "OKTA", "MNDY", "IOT",
    },
    "internet": {
        "GOOGL", "GOOG", "META", "AMZN", "NFLX", "UBER", "ABNB", "BKNG", "MELI",
        "RDDT", "DASH", "SPOT", "PINS", "ROKU", "SE",
    },
}


@dataclass
class BacktestPosition:
    ticker: str
    shares: float
    entry_price: float
    entry_date: object
    highest_high: float
    stop: float


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


def fetch_yahoo_intraday_snapshot(ticker):
    response = requests.get(
        f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}",
        params={
            "range": "1d",
            "interval": "1m",
            "includePrePost": "false",
        },
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    payload = response.json()
    result = (payload.get("chart", {}).get("result") or [None])[0]
    if not result or not result.get("timestamp"):
        return None

    quote = result["indicators"]["quote"][0]
    rows = pd.DataFrame(
        {
            "DateTime": pd.to_datetime(result["timestamp"], unit="s")
            .tz_localize("UTC")
            .tz_convert("America/New_York"),
            "Open": quote["open"],
            "High": quote["high"],
            "Low": quote["low"],
            "Close": quote["close"],
            "Volume": quote["volume"],
        }
    ).dropna()
    if rows.empty:
        return None

    latest = rows.iloc[-1]
    return {
        "date": latest["DateTime"].date(),
        "timestamp": latest["DateTime"].isoformat(),
        "open": float(rows["Open"].iloc[0]),
        "high": float(rows["High"].max()),
        "low": float(rows["Low"].min()),
        "close": float(latest["Close"]),
        "volume": float(rows["Volume"].sum()),
    }


def add_indicators(df):
    df = df.copy()
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
    df["VOL20"] = df["Volume"].rolling(20).mean()
    df["RET20"] = df["Close"] / df["Close"].shift(20) - 1
    df["RET63"] = df["Close"] / df["Close"].shift(63) - 1
    delta = df["Close"].diff()
    gains = delta.clip(lower=0).rolling(14).mean()
    losses = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gains / losses.replace(0, np.nan)
    df["RSI14"] = 100 - (100 / (1 + rs))
    df["RSI14"] = df["RSI14"].fillna(100)
    prev_close = df["Close"].shift(1)
    df["PREV_CLOSE"] = prev_close
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
    df["AdjFactor"] = factor

    return add_indicators(df[["Date", "Open", "High", "Low", "Close", "Volume", "AdjFactor"]].set_index("Date"))


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


def apply_intraday_snapshot(df, snapshot):
    if not snapshot:
        return df

    df = df.copy()
    snap_date = snapshot["date"]
    adj_factor = float(df["AdjFactor"].dropna().iloc[-1]) if "AdjFactor" in df else 1.0
    adjusted_snapshot = {
        **snapshot,
        "open": snapshot["open"] * adj_factor,
        "high": snapshot["high"] * adj_factor,
        "low": snapshot["low"] * adj_factor,
        "close": snapshot["close"] * adj_factor,
    }
    if snap_date in df.index:
        df.loc[snap_date, "Open"] = adjusted_snapshot["open"]
        df.loc[snap_date, "High"] = max(float(df.loc[snap_date, "High"]), adjusted_snapshot["high"])
        df.loc[snap_date, "Low"] = min(float(df.loc[snap_date, "Low"]), adjusted_snapshot["low"])
        df.loc[snap_date, "Close"] = adjusted_snapshot["close"]
        df.loc[snap_date, "Volume"] = max(float(df.loc[snap_date, "Volume"]), snapshot["volume"])
        if "AdjFactor" in df:
            df.loc[snap_date, "AdjFactor"] = adj_factor
    elif snap_date > max(df.index):
        previous = df.iloc[-1]
        df.loc[snap_date, ["Open", "High", "Low", "Close", "Volume"]] = [
            adjusted_snapshot["open"],
            adjusted_snapshot["high"],
            adjusted_snapshot["low"],
            adjusted_snapshot["close"],
            snapshot["volume"],
        ]
        # Seed non-price columns before recomputing indicators below.
        for column in df.columns:
            if column not in {"Open", "High", "Low", "Close", "Volume"}:
                df.loc[snap_date, column] = previous[column]
    base_columns = ["Open", "High", "Low", "Close", "Volume"]
    if "AdjFactor" in df:
        base_columns.append("AdjFactor")
    return add_indicators(df[base_columns].sort_index())


def apply_intraday_snapshots(data, qqq):
    errors = []
    refreshed = {}
    for ticker, df in data.items():
        try:
            refreshed[ticker] = apply_intraday_snapshot(df, fetch_yahoo_intraday_snapshot(ticker))
        except Exception as exc:
            refreshed[ticker] = df
            errors.append({"ticker": ticker, "error": f"intraday snapshot failed: {exc}"})
    try:
        qqq = apply_intraday_snapshot(qqq, fetch_yahoo_intraday_snapshot("QQQ"))
    except Exception as exc:
        errors.append({"ticker": "QQQ", "error": f"intraday snapshot failed: {exc}"})
    return refreshed, qqq, errors


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


def add_market_risk_indicators(qqq):
    qqq = qqq.copy()
    qqq["SMA10"] = qqq["Close"].rolling(10).mean()
    qqq["SMA20"] = qqq["Close"].rolling(20).mean()
    qqq["VOL50"] = qqq["Volume"].rolling(50).mean()
    qqq["RET5"] = qqq["Close"] / qqq["Close"].shift(5) - 1
    qqq["HIGH20"] = qqq["High"].rolling(20).max()
    qqq["DRAWDOWN20"] = qqq["Close"] / qqq["HIGH20"] - 1
    qqq["DIST_SMA20"] = qqq["Close"] / qqq["SMA20"] - 1
    qqq["DISTRIBUTION"] = ((qqq["Close"] < qqq["PREV_CLOSE"]) & (qqq["Volume"] > qqq["VOL50"] * 1.15)).astype(int)
    qqq["DISTRIBUTION5"] = qqq["DISTRIBUTION"].rolling(5).sum()
    return qqq.dropna()


def market_risk_score(qqq, date, config):
    if date not in qqq.index:
        return 0, []
    row = qqq.loc[date]
    score = 0
    reasons = []
    if row["Close"] < row["SMA20"]:
        score += int(config["below_sma20_points"])
        reasons.append("QQQ below SMA20")
    if row["Close"] < row["SMA10"]:
        score += int(config["below_sma10_points"])
        reasons.append("QQQ below SMA10")
    if row["RET5"] <= -float(config["ret5_drop"]):
        score += int(config["ret5_points"])
        reasons.append("QQQ 5d drop")
    if row["DISTRIBUTION5"] >= int(config["distribution_days"]):
        score += int(config["distribution_points"])
        reasons.append("distribution days")
    if row["DRAWDOWN20"] <= -float(config["drawdown20"]):
        score += int(config["drawdown_points"])
        reasons.append("20d drawdown")
    if row["RSI14"] >= float(config["rsi_hot"]):
        score += int(config["hot_rsi_points"])
        reasons.append("QQQ hot RSI")
    if row["DIST_SMA20"] >= float(config["hot_dist_sma20"]):
        score += int(config["hot_dist_points"])
        reasons.append("QQQ extended above SMA20")
    return score, reasons


RISK_CONFIGS = [
    {
        "name": "risk_loose",
        "below_sma20_points": 2,
        "below_sma10_points": 1,
        "ret5_drop": 0.04,
        "ret5_points": 1,
        "distribution_days": 3,
        "distribution_points": 1,
        "drawdown20": 0.06,
        "drawdown_points": 1,
        "rsi_hot": 82,
        "hot_rsi_points": 1,
        "hot_dist_sma20": 0.08,
        "hot_dist_points": 1,
        "elevated_threshold": 3,
        "defensive_threshold": 5,
    },
    {
        "name": "risk_balanced",
        "below_sma20_points": 2,
        "below_sma10_points": 1,
        "ret5_drop": 0.03,
        "ret5_points": 1,
        "distribution_days": 2,
        "distribution_points": 1,
        "drawdown20": 0.05,
        "drawdown_points": 1,
        "rsi_hot": 80,
        "hot_rsi_points": 1,
        "hot_dist_sma20": 0.07,
        "hot_dist_points": 1,
        "elevated_threshold": 3,
        "defensive_threshold": 5,
    },
    {
        "name": "risk_tight",
        "below_sma20_points": 2,
        "below_sma10_points": 1,
        "ret5_drop": 0.025,
        "ret5_points": 1,
        "distribution_days": 2,
        "distribution_points": 1,
        "drawdown20": 0.04,
        "drawdown_points": 1,
        "rsi_hot": 78,
        "hot_rsi_points": 1,
        "hot_dist_sma20": 0.06,
        "hot_dist_points": 1,
        "elevated_threshold": 2,
        "defensive_threshold": 4,
    },
]


def initial_stop(close, atr14):
    return max(close * 0.88, close - 2.5 * atr14)


def trailing_stop(highest_high, atr14):
    return max(highest_high * 0.85, highest_high - 3.0 * atr14)


def variant_initial_stop(close, atr14, variant):
    if variant == "aggressive":
        return max(close * 0.90, close - 2.0 * atr14)
    if variant == "turbo":
        return max(close * 0.88, close - 2.5 * atr14)
    return initial_stop(close, atr14)


def variant_trailing_stop(highest_high, atr14, variant):
    if variant == "aggressive":
        return max(highest_high * 0.88, highest_high - 2.5 * atr14)
    if variant == "turbo":
        return max(highest_high * 0.82, highest_high - 3.5 * atr14)
    return trailing_stop(highest_high, atr14)


def extension_warning(row):
    warnings = []
    rsi14 = float(row["RSI14"])
    above_sma50 = float(row["Close"] / row["SMA50"] - 1)
    intraday_move = float(row["Close"] / row["PREV_CLOSE"] - 1) if row["PREV_CLOSE"] else 0.0
    if rsi14 >= 80:
        warnings.append(f"RSI14 {rsi14:.0f}")
    if above_sma50 >= 0.30:
        warnings.append(f"{above_sma50:.0%} above SMA50")
    if intraday_move >= 0.08:
        warnings.append(f"{intraday_move:.0%} above prior close")
    if warnings:
        return "HOT BUT STRETCHED: " + ", ".join(warnings)
    return "OK"


def is_stretched(row):
    return extension_warning(row) != "OK"


def is_extremely_stretched(row):
    rsi14 = float(row["RSI14"])
    above_sma50 = float(row["Close"] / row["SMA50"] - 1)
    intraday_move = float(row["Close"] / row["PREV_CLOSE"] - 1) if row["PREV_CLOSE"] else 0.0
    return bool(rsi14 >= 85 or above_sma50 >= 0.60 or intraday_move >= 0.12)


def candidate_for(data, qqq, ticker, date, variant="base"):
    if ticker not in data or date not in data[ticker].index or date not in qqq.index:
        return None

    row = data[ticker].loc[date]
    qrow = qqq.loc[date]
    rs63 = row["RET63"] - qrow["RET63"]
    above_sma50 = row["Close"] / row["SMA50"] - 1

    if not qualifies_for_variant(row, qrow, variant):
        return None

    score = score_candidate(row, qrow, variant)
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
        "rsi14": float(row["RSI14"]),
        "intraday_move": float(row["Close"] / row["PREV_CLOSE"] - 1) if row["PREV_CLOSE"] else 0.0,
        "extension_warning": extension_warning(row),
        "sma50": float(row["SMA50"]),
        "sma200": float(row["SMA200"]),
        "atr14": atr14,
        "initial_stop": float(variant_initial_stop(close, atr14, variant)),
        "avg_dollar_volume": float(row["Close"] * row["VOL20"]),
    }


def scan_candidates(
    data,
    qqq,
    date,
    max_positions=2,
    variant="base",
    rank_policy="none",
    previous_targets=None,
    return_skipped=False,
):
    candidates = []
    skipped = []
    previous_targets = set(previous_targets or [])
    for ticker in data:
        signal = candidate_for(data, qqq, ticker, date, variant)
        if signal:
            candidates.append(signal)
    ranked = sorted(candidates, key=lambda item: item["score"], reverse=True)
    filtered = []
    for candidate in ranked:
        repeat_stretched = (
            rank_policy == "skip_repeat_stretched"
            and candidate["ticker"] in previous_targets
            and candidate["extension_warning"] != "OK"
        )
        if repeat_stretched:
            skipped.append({**candidate, "skip_reason": "repeat stretched candidate"})
            continue
        filtered.append(candidate)
        if len(filtered) >= max_positions:
            break
    if return_skipped:
        return filtered, skipped
    return filtered


def common_dates(data, qqq, start):
    first = pd.Timestamp(start).date()
    usable = set(qqq.index)
    for df in data.values():
        usable |= set(df.index)
    return sorted(date for date in usable if date >= first and date in qqq.index)


def max_drawdown(values):
    series = pd.Series(values, dtype=float)
    peaks = series.cummax()
    return float((series / peaks - 1).min())


def cagr(final_value, start_date, end_date):
    years = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days / 365.25
    if years <= 0:
        return 0.0
    return float(final_value ** (1 / years) - 1)


def score_candidate(row, qrow, variant):
    rs63 = row["RET63"] - qrow["RET63"]
    above_sma50 = row["Close"] / row["SMA50"] - 1
    if variant == "aggressive":
        return rs63 * 120 + row["RET20"] * 55 + above_sma50 * 25
    if variant == "turbo":
        return rs63 * 100 + row["RET20"] * 90
    return rs63 * 100 + row["RET20"] * 35 + above_sma50 * 20


def score_candidate_weights(row, qrow, weights):
    rs63 = row["RET63"] - qrow["RET63"]
    above_sma50 = row["Close"] / row["SMA50"] - 1
    return rs63 * weights["rs63"] + row["RET20"] * weights["ret20"] + above_sma50 * weights["above_sma50"]


def sector_for(ticker):
    for sector, tickers in SECTOR_GROUPS.items():
        if ticker in tickers:
            return sector
    return ticker


def qualifies_for_variant(row, qrow, variant):
    market_ok = qrow["Close"] > qrow["SMA200"]
    liquid = row["Close"] * row["VOL20"] > 50_000_000
    relative_strength = row["RET63"] > qrow["RET63"]
    if variant == "turbo":
        trend_ok = row["Close"] > row["EMA21"] and row["Close"] > row["SMA50"]
        momentum_ok = row["RET20"] > 0 and row["RET63"] > 0
    else:
        trend_ok = row["Close"] > row["SMA50"] > row["SMA200"]
        momentum_ok = True
    return bool(market_ok and liquid and relative_strength and trend_ok and momentum_ok)


def rank_for_date(data, qqq, date, positions, variant, rank_policy="none", previous_targets=None):
    if date not in qqq.index:
        return []
    qrow = qqq.loc[date]
    ranked = []
    previous_targets = set(previous_targets or [])
    for ticker, df in data.items():
        if ticker in positions or date not in df.index:
            continue
        row = df.loc[date]
        if qualifies_for_variant(row, qrow, variant):
            if rank_policy == "skip_repeat_stretched" and ticker in previous_targets and is_stretched(row):
                continue
            if rank_policy == "skip_repeat_extreme" and ticker in previous_targets and is_extremely_stretched(row):
                continue
            if rank_policy == "skip_extreme" and is_extremely_stretched(row):
                continue
            ranked.append((float(score_candidate(row, qrow, variant)), ticker))
    ranked.sort(reverse=True)
    return [ticker for _, ticker in ranked]


def dip_candidate_for(data, qqq, ticker, date, config):
    if ticker not in data or date not in data[ticker].index or date not in qqq.index:
        return None

    row = data[ticker].loc[date]
    qrow = qqq.loc[date]
    intraday_drop = row["Close"] / row["PREV_CLOSE"] - 1 if row["PREV_CLOSE"] else 0.0
    qqq_drop = qrow["Close"] / qrow["PREV_CLOSE"] - 1 if qrow["PREV_CLOSE"] else 0.0
    liquid = row["Close"] * row["VOL20"] > 50_000_000
    market_ok = qrow["Close"] > qrow["SMA200"]
    trend_ok = row["Close"] > row["SMA50"] and row["Close"] > row["SMA200"]
    momentum_ok = row["RET20"] > 0 and row["RET63"] > 0
    relative_strength = row["RET63"] > qrow["RET63"]
    dip_ok = intraday_drop <= -float(config["min_drop"])
    if config.get("must_drop_more_than_qqq", False):
        dip_ok = dip_ok and intraday_drop < qqq_drop

    if not all([liquid, market_ok, trend_ok, momentum_ok, relative_strength, dip_ok]):
        return None

    rs63 = row["RET63"] - qrow["RET63"]
    score = abs(intraday_drop) * 90 + rs63 * 60 + row["RET20"] * 25
    return {
        "ticker": ticker,
        "score": float(score),
        "drop": float(intraday_drop),
        "qqq_drop": float(qqq_drop),
        "ret20": float(row["RET20"]),
        "ret63": float(row["RET63"]),
        "rs63": float(rs63),
    }


def rank_dip_for_date(data, qqq, date, positions, config):
    if date not in qqq.index:
        return []
    ranked = []
    for ticker in data:
        if ticker in positions:
            continue
        signal = dip_candidate_for(data, qqq, ticker, date, config)
        if signal:
            ranked.append(signal)
    return [item["ticker"] for item in sorted(ranked, key=lambda item: item["score"], reverse=True)]


def risk_multiplier(risk_score, config, policy):
    if not policy or policy == "none":
        return 1.0
    if policy == "block_elevated" and risk_score >= config["elevated_threshold"]:
        return 0.0
    if policy == "half_elevated" and risk_score >= config["elevated_threshold"]:
        return 0.5
    return 1.0


def summarize_backtest_result(result, values, trades, positions, data, final_date, risk_events=None):
    final = values[-1][1]
    series = [value for _, value in values]
    wins = []
    buys = {}
    for trade_date, ticker, side, price, reason in trades:
        if side == "buy":
            buys.setdefault(ticker, []).append(price)
        elif side == "sell" and buys.get(ticker):
            entry = buys[ticker].pop(0)
            wins.append(price / entry - 1)

    annual = cagr(final, values[0][0], values[-1][0])
    dd = max_drawdown(series)
    result.update(
        {
            "start": values[0][0],
            "end": final_date,
            "final": final,
            "cagr": annual,
            "maxdd": dd,
            "calmar": annual / abs(dd) if dd else np.nan,
            "trades": len(trades),
            "round_trips": len(wins),
            "win_rate": float(np.mean([win > 0 for win in wins])) if wins else np.nan,
            "avg_trade": float(np.mean(wins)) if wins else np.nan,
            "risk_events": risk_events or [],
            "values": values,
            "trades_list": trades,
            "open_positions": sorted(positions),
        }
    )
    return result


def extension_multiplier(row, policy):
    if policy in {None, "none", "full"}:
        return 1.0
    stretched = is_stretched(row)
    if policy == "half_stretched" and stretched:
        return 0.5
    if policy == "skip_stretched" and stretched:
        return 0.0
    return 1.0


def run_rotation_backtest(
    data,
    qqq,
    start="2018-01-01",
    max_positions=2,
    variant="base",
    risk_config=None,
    risk_policy="none",
    extension_policy="none",
    entry_limit=None,
    rank_policy="none",
):
    dates = common_dates(data, qqq, start)
    cash = 1.0
    positions = {}
    values = []
    trades = []
    target_tickers = []
    rebalance_next_open = False
    risk_events = []
    qqq_risk = add_market_risk_indicators(qqq)

    for idx, date in enumerate(dates):
        qrow = qqq.loc[date]
        market_ok = qrow["Close"] > qrow["SMA200"]
        risk_score, risk_reasons = market_risk_score(qqq_risk, date, risk_config) if risk_config else (0, [])
        if risk_config and risk_score >= risk_config["elevated_threshold"]:
            risk_events.append((date, risk_score, "; ".join(risk_reasons)))

        if risk_policy == "exit_defensive" and risk_config and risk_score >= risk_config["defensive_threshold"]:
            for ticker in list(positions):
                if date in data[ticker].index:
                    row = data[ticker].loc[date]
                    pos = positions.pop(ticker)
                    cash += pos.shares * row["Close"]
                    trades.append((date, ticker, "sell", row["Close"], "risk_defensive_exit"))

        if rebalance_next_open:
            desired = set(target_tickers if market_ok else [])
            for ticker in list(positions):
                if ticker not in desired and date in data[ticker].index:
                    row = data[ticker].loc[date]
                    pos = positions.pop(ticker)
                    cash += pos.shares * row["Open"]
                    trades.append((date, ticker, "sell", row["Open"], "weekly_rotation"))

            equity = cash + sum(
                pos.shares * data[ticker].loc[date]["Open"]
                for ticker, pos in positions.items()
                if date in data[ticker].index
            )

            buys_this_rebalance = 0
            for ticker in target_tickers:
                if not market_ok or ticker in positions or ticker not in data or date not in data[ticker].index:
                    continue
                if len(positions) >= max_positions:
                    break
                if entry_limit and buys_this_rebalance >= entry_limit:
                    break
                row = data[ticker].loc[date]
                slots_left = max_positions - len(positions)
                target_value = equity / max_positions
                multiplier = risk_multiplier(risk_score, risk_config, risk_policy) * extension_multiplier(row, extension_policy)
                allocation = min(cash, target_value * multiplier if slots_left > 1 else cash * multiplier)
                if allocation <= 0:
                    trades.append((date, ticker, "skip", row["Open"], f"{risk_policy}_{extension_policy}_risk_score_{risk_score}"))
                    continue
                shares = allocation / row["Open"]
                cash -= allocation
                stop = variant_initial_stop(float(row["Open"]), float(row["ATR14"]), variant)
                positions[ticker] = BacktestPosition(ticker, shares, row["Open"], date, row["High"], stop)
                trades.append((date, ticker, "buy", row["Open"], f"{variant}_momentum"))
                buys_this_rebalance += 1
            rebalance_next_open = False

        for ticker in list(positions):
            if date not in data[ticker].index:
                continue
            row = data[ticker].loc[date]
            pos = positions[ticker]
            pos.highest_high = max(pos.highest_high, row["High"])
            pos.stop = max(pos.stop, variant_trailing_stop(float(pos.highest_high), float(row["ATR14"]), variant))
            if row["Low"] <= pos.stop:
                cash += pos.shares * pos.stop
                positions.pop(ticker)
                trades.append((date, ticker, "sell", pos.stop, "stop"))
            elif variant in {"base", "aggressive"} and row["Close"] < row["EMA21"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "ema21_exit"))
            elif variant == "turbo" and row["Close"] < row["SMA50"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "sma50_exit"))

        value = cash + sum(
            pos.shares * data[ticker].loc[date]["Close"]
            for ticker, pos in positions.items()
            if date in data[ticker].index
        )
        values.append((date, float(value)))

        is_week_end = idx == len(dates) - 1 or pd.Timestamp(dates[idx + 1]).isocalendar().week != pd.Timestamp(date).isocalendar().week
        if is_week_end:
            held = [ticker for ticker in positions if ticker in data and date in data[ticker].index]
            target_tickers = (
                held + rank_for_date(data, qqq, date, positions, variant, rank_policy, target_tickers)
            )[:max_positions]
            rebalance_next_open = True

    return summarize_backtest_result(
        {
        "variant": variant,
        "max_positions": max_positions,
        "risk_policy": risk_policy,
        "risk_config": risk_config["name"] if risk_config else "none",
        "extension_policy": extension_policy,
        "entry_limit": entry_limit or "none",
        "rank_policy": rank_policy,
        "entry_system": "momentum",
        },
        values,
        trades,
        positions,
        data,
        values[-1][0],
        risk_events,
    )


def run_dip_entry_backtest(data, qqq, start="2018-01-01", max_positions=2, config=None):
    config = config or {}
    dates = common_dates(data, qqq, start)
    cash = 1.0
    positions = {}
    values = []
    trades = []
    pending_tickers = []
    risk_config = next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced")
    qqq_risk = add_market_risk_indicators(qqq)

    for idx, date in enumerate(dates):
        qrow = qqq.loc[date]
        market_ok = qrow["Close"] > qrow["SMA200"]
        risk_score, _ = market_risk_score(qqq_risk, date, risk_config)

        if pending_tickers:
            equity = cash + sum(
                pos.shares * data[ticker].loc[date]["Open"]
                for ticker, pos in positions.items()
                if date in data[ticker].index
            )
            buys_today = 0
            for ticker in pending_tickers:
                if not market_ok or ticker in positions or ticker not in data or date not in data[ticker].index:
                    continue
                if len(positions) >= max_positions or buys_today >= int(config.get("entry_limit", max_positions)):
                    break
                row = data[ticker].loc[date]
                target_value = equity / max_positions
                multiplier = risk_multiplier(risk_score, risk_config, "half_elevated")
                allocation = min(cash, target_value * multiplier)
                if allocation <= 0:
                    trades.append((date, ticker, "skip", row["Open"], f"dip_risk_score_{risk_score}"))
                    continue
                shares = allocation / row["Open"]
                cash -= allocation
                stop = variant_initial_stop(float(row["Open"]), float(row["ATR14"]), "turbo")
                positions[ticker] = BacktestPosition(ticker, shares, row["Open"], date, row["High"], stop)
                trades.append((date, ticker, "buy", row["Open"], config["name"]))
                buys_today += 1
            pending_tickers = []

        for ticker in list(positions):
            if date not in data[ticker].index:
                continue
            row = data[ticker].loc[date]
            pos = positions[ticker]
            pos.highest_high = max(pos.highest_high, row["High"])
            pos.stop = max(pos.stop, variant_trailing_stop(float(pos.highest_high), float(row["ATR14"]), "turbo"))
            hold_days = (pd.Timestamp(date) - pd.Timestamp(pos.entry_date)).days
            target_hit = bool(config.get("profit_target")) and row["High"] >= pos.entry_price * (1 + float(config["profit_target"]))
            max_hold_hit = bool(config.get("max_hold_days")) and hold_days >= int(config["max_hold_days"])
            if row["Low"] <= pos.stop:
                cash += pos.shares * pos.stop
                positions.pop(ticker)
                trades.append((date, ticker, "sell", pos.stop, "stop"))
            elif target_hit:
                exit_price = pos.entry_price * (1 + float(config["profit_target"]))
                cash += pos.shares * exit_price
                positions.pop(ticker)
                trades.append((date, ticker, "sell", exit_price, "profit_target"))
            elif max_hold_hit:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "max_hold"))
            elif row["Close"] < row["SMA50"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "sma50_exit"))

        value = cash + sum(
            pos.shares * data[ticker].loc[date]["Close"]
            for ticker, pos in positions.items()
            if date in data[ticker].index
        )
        values.append((date, float(value)))

        if idx < len(dates) - 1 and market_ok:
            pending_tickers = rank_dip_for_date(data, qqq, date, positions, config)[:max_positions]

    return summarize_backtest_result(
        {
            "variant": "dip",
            "max_positions": max_positions,
            "risk_policy": "half_elevated",
            "risk_config": risk_config["name"],
            "extension_policy": "none",
            "entry_limit": config.get("entry_limit", max_positions),
            "entry_decision": config["name"],
            "entry_system": "dip",
            "min_drop": config["min_drop"],
            "profit_target": config.get("profit_target", "none"),
            "max_hold_days": config.get("max_hold_days", "none"),
        },
        values,
        trades,
        positions,
        data,
        values[-1][0],
    )


def run_variant_pack(data, qqq, start="2018-01-01"):
    specs = [
        ("base", 2),
        ("aggressive", 1),
        ("aggressive", 2),
        ("aggressive", 3),
        ("turbo", 1),
        ("turbo", 2),
    ]
    return [run_rotation_backtest(data, qqq, start, max_positions, variant) for variant, max_positions in specs]


def run_risk_overlay_pack(data, qqq, start="2018-01-01"):
    results = [run_rotation_backtest(data, qqq, start, 2, "turbo")]
    for config in RISK_CONFIGS:
        for policy in ["block_elevated", "half_elevated", "exit_defensive"]:
            results.append(run_rotation_backtest(data, qqq, start, 2, "turbo", config, policy))
    return results


def run_entry_decision_pack(data, qqq, start="2018-01-01"):
    config = next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced")
    specs = [
        ("full_two", "none", None),
        ("half_stretched_two", "half_stretched", None),
        ("skip_stretched_two", "skip_stretched", None),
        ("full_top_one", "none", 1),
        ("half_stretched_top_one", "half_stretched", 1),
        ("skip_stretched_top_one", "skip_stretched", 1),
    ]
    results = []
    for label, extension_policy, entry_limit in specs:
        result = run_rotation_backtest(
            data,
            qqq,
            start,
            2,
            "turbo",
            config,
            "half_elevated",
            extension_policy,
            entry_limit,
        )
        result["entry_decision"] = label
        results.append(result)
    return results


def run_repeat_stretch_pack(data, qqq, start="2018-01-01"):
    config = next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced")
    specs = [
        ("baseline_full_two", "none", "none", None),
        ("skip_repeat_stretched", "skip_repeat_stretched", "none", None),
        ("skip_repeat_extreme", "skip_repeat_extreme", "none", None),
        ("skip_all_extreme", "skip_extreme", "none", None),
        ("half_stretched_baseline", "none", "half_stretched", None),
        ("skip_stretched_baseline", "none", "skip_stretched", None),
    ]
    results = []
    for label, rank_policy, extension_policy, entry_limit in specs:
        result = run_rotation_backtest(
            data,
            qqq,
            start,
            2,
            "turbo",
            config,
            "half_elevated",
            extension_policy,
            entry_limit,
            rank_policy,
        )
        result["entry_decision"] = label
        result["entry_system"] = "repeat_stretch"
        results.append(result)
    return results


def run_dip_entry_pack(data, qqq, start="2018-01-01"):
    specs = [
        {
            "name": "dip_3pct_quick_bounce",
            "min_drop": 0.03,
            "profit_target": 0.08,
            "max_hold_days": 15,
            "entry_limit": 2,
            "must_drop_more_than_qqq": True,
        },
        {
            "name": "dip_5pct_quick_bounce",
            "min_drop": 0.05,
            "profit_target": 0.10,
            "max_hold_days": 20,
            "entry_limit": 2,
            "must_drop_more_than_qqq": True,
        },
        {
            "name": "dip_3pct_ride_trend",
            "min_drop": 0.03,
            "profit_target": None,
            "max_hold_days": None,
            "entry_limit": 2,
            "must_drop_more_than_qqq": True,
        },
        {
            "name": "dip_5pct_ride_trend",
            "min_drop": 0.05,
            "profit_target": None,
            "max_hold_days": None,
            "entry_limit": 2,
            "must_drop_more_than_qqq": True,
        },
        {
            "name": "dip_3pct_top_one_quick",
            "min_drop": 0.03,
            "profit_target": 0.08,
            "max_hold_days": 15,
            "entry_limit": 1,
            "must_drop_more_than_qqq": True,
        },
        {
            "name": "dip_5pct_top_one_quick",
            "min_drop": 0.05,
            "profit_target": 0.10,
            "max_hold_days": 20,
            "entry_limit": 1,
            "must_drop_more_than_qqq": True,
        },
    ]
    baseline = run_rotation_backtest(
        data,
        qqq,
        start,
        2,
        "turbo",
        next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced"),
        "half_elevated",
    )
    baseline["entry_decision"] = "turbo_full_two_baseline"
    return [baseline] + [run_dip_entry_backtest(data, qqq, start, 2, spec) for spec in specs]


def run_universe_pack(start="2018-01-01"):
    config = next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced")
    specs = [
        ("current_top2", UNIVERSE, 2),
        ("current_top3", UNIVERSE, 3),
        ("expanded_growth_top2", EXPANDED_GROWTH_UNIVERSE, 2),
        ("expanded_growth_top3", EXPANDED_GROWTH_UNIVERSE, 3),
        ("expanded_with_etfs_top2", EXPANDED_WITH_ETFS_UNIVERSE, 2),
        ("expanded_with_etfs_top3", EXPANDED_WITH_ETFS_UNIVERSE, 3),
    ]
    results = []
    load_notes = []
    for label, tickers, max_positions in specs:
        data, qqq, errors = load_universe(tickers)
        result = run_rotation_backtest(data, qqq, start, max_positions, "turbo", config, "half_elevated")
        result["entry_decision"] = label
        result["entry_system"] = "universe"
        result["universe_size"] = len(tickers)
        result["loaded_tickers"] = len(data)
        result["data_errors"] = len(errors)
        results.append(result)
        for item in errors:
            load_notes.append({"universe": label, **item})

    out_dir = Path("research/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    if load_notes:
        pd.DataFrame(load_notes).to_csv(out_dir / "universe_load_errors.csv", index=False)
    return results


def idea_trailing_stop(highest_high, atr14, stop_policy):
    if stop_policy == "tight":
        return max(highest_high * 0.88, highest_high - 2.5 * atr14)
    if stop_policy == "loose":
        return max(highest_high * 0.78, highest_high - 4.0 * atr14)
    return variant_trailing_stop(highest_high, atr14, "turbo")


def run_strategy_idea_backtest(data, qqq, start="2018-01-01", label="baseline", options=None):
    options = options or {}
    dates = common_dates(data, qqq, start)
    cash = 1.0
    positions = {}
    values = []
    trades = []
    target_tickers = []
    rebalance_next_open = False
    risk_events = []
    config = next(item for item in RISK_CONFIGS if item["name"] == "risk_balanced")
    qqq_risk = add_market_risk_indicators(qqq)
    weights = options.get("weights", {"rs63": 90, "ret20": 80, "above_sma50": 35})
    rank_policy = options.get("rank_policy", "skip_repeat_stretched")
    stop_policy = options.get("stop_policy", "turbo")
    exit_policy = options.get("exit_policy", "sma50")
    max_open_gap = options.get("max_open_gap")
    profit_lock = options.get("profit_lock")
    profit_target = options.get("profit_target")
    sector_limit = bool(options.get("sector_limit", False))

    for idx, date in enumerate(dates):
        qrow = qqq.loc[date]
        market_ok = qrow["Close"] > qrow["SMA200"]
        risk_score, risk_reasons = market_risk_score(qqq_risk, date, config)
        if risk_score >= config["elevated_threshold"]:
            risk_events.append((date, risk_score, "; ".join(risk_reasons)))

        if rebalance_next_open:
            desired = set(target_tickers if market_ok else [])
            for ticker in list(positions):
                if ticker not in desired and date in data[ticker].index:
                    row = data[ticker].loc[date]
                    pos = positions.pop(ticker)
                    cash += pos.shares * row["Open"]
                    trades.append((date, ticker, "sell", row["Open"], "weekly_rotation"))

            equity = cash + sum(
                pos.shares * data[ticker].loc[date]["Open"]
                for ticker, pos in positions.items()
                if date in data[ticker].index
            )
            active_sectors = {sector_for(ticker) for ticker in positions}
            buys_this_rebalance = 0
            for ticker in target_tickers:
                if not market_ok or ticker in positions or ticker not in data or date not in data[ticker].index:
                    continue
                if len(positions) >= 2:
                    break
                row = data[ticker].loc[date]
                prev_close = row["PREV_CLOSE"]
                opening_gap = row["Open"] / prev_close - 1 if prev_close else 0.0
                if max_open_gap is not None and opening_gap > max_open_gap:
                    trades.append((date, ticker, "skip", row["Open"], f"open_gap_{opening_gap:.2%}"))
                    continue
                sector = sector_for(ticker)
                if sector_limit and sector in active_sectors:
                    trades.append((date, ticker, "skip", row["Open"], f"sector_limit_{sector}"))
                    continue
                target_value = equity / 2
                allocation = min(cash, target_value * risk_multiplier(risk_score, config, "half_elevated"))
                if allocation <= 0:
                    trades.append((date, ticker, "skip", row["Open"], f"risk_score_{risk_score}"))
                    continue
                shares = allocation / row["Open"]
                cash -= allocation
                stop = variant_initial_stop(float(row["Open"]), float(row["ATR14"]), "turbo")
                positions[ticker] = BacktestPosition(ticker, shares, row["Open"], date, row["High"], stop)
                active_sectors.add(sector)
                trades.append((date, ticker, "buy", row["Open"], label))
                buys_this_rebalance += 1
            rebalance_next_open = False

        for ticker in list(positions):
            if date not in data[ticker].index:
                continue
            row = data[ticker].loc[date]
            pos = positions[ticker]
            pos.highest_high = max(pos.highest_high, row["High"])
            pos.stop = max(pos.stop, idea_trailing_stop(float(pos.highest_high), float(row["ATR14"]), stop_policy))
            if profit_lock and pos.highest_high >= pos.entry_price * (1 + profit_lock["trigger"]):
                pos.stop = max(pos.stop, pos.highest_high * (1 - profit_lock["trail"]))
            if profit_target and row["High"] >= pos.entry_price * (1 + profit_target):
                exit_price = pos.entry_price * (1 + profit_target)
                cash += pos.shares * exit_price
                positions.pop(ticker)
                trades.append((date, ticker, "sell", exit_price, "profit_target"))
            elif row["Low"] <= pos.stop:
                cash += pos.shares * pos.stop
                positions.pop(ticker)
                trades.append((date, ticker, "sell", pos.stop, "stop"))
            elif exit_policy == "ema21" and row["Close"] < row["EMA21"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "ema21_exit"))
            elif exit_policy == "sma20" and row["Close"] < row["SMA20"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "sma20_exit"))
            elif exit_policy == "sma50" and row["Close"] < row["SMA50"]:
                cash += pos.shares * row["Close"]
                positions.pop(ticker)
                trades.append((date, ticker, "sell", row["Close"], "sma50_exit"))

        value = cash + sum(
            pos.shares * data[ticker].loc[date]["Close"]
            for ticker, pos in positions.items()
            if date in data[ticker].index
        )
        values.append((date, float(value)))

        is_week_end = idx == len(dates) - 1 or pd.Timestamp(dates[idx + 1]).isocalendar().week != pd.Timestamp(date).isocalendar().week
        if is_week_end:
            held = [ticker for ticker in positions if ticker in data and date in data[ticker].index]
            ranked = []
            previous_targets = set(target_tickers)
            held_sectors = {sector_for(ticker) for ticker in held}
            for ticker, df in data.items():
                if ticker in positions or date not in df.index:
                    continue
                row = df.loc[date]
                if not qualifies_for_variant(row, qrow, "turbo"):
                    continue
                if rank_policy == "skip_repeat_stretched" and ticker in previous_targets and is_stretched(row):
                    continue
                if sector_limit and sector_for(ticker) in held_sectors:
                    continue
                ranked.append((float(score_candidate_weights(row, qrow, weights)), ticker))
            ranked.sort(reverse=True)
            target_tickers = (held + [ticker for _, ticker in ranked])[:2]
            rebalance_next_open = True

    return summarize_backtest_result(
        {
            "variant": "turbo",
            "max_positions": 2,
            "risk_policy": "half_elevated",
            "risk_config": config["name"],
            "extension_policy": "none",
            "rank_policy": rank_policy,
            "entry_limit": "none",
            "entry_decision": label,
            "entry_system": "strategy_idea",
            "stop_policy": stop_policy,
            "exit_policy": exit_policy,
            "profit_target": profit_target or "none",
            "max_open_gap": max_open_gap if max_open_gap is not None else "none",
            "sector_limit": sector_limit,
        },
        values,
        trades,
        positions,
        data,
        values[-1][0],
        risk_events,
    )


def run_strategy_idea_pack(data, qqq, start="2018-01-01"):
    specs = [
        ("baseline_live", {}),
        ("score_20d_heavy", {"weights": {"rs63": 70, "ret20": 120, "above_sma50": 25}}),
        ("score_rs63_heavy", {"weights": {"rs63": 130, "ret20": 55, "above_sma50": 25}}),
        ("score_no_extension", {"weights": {"rs63": 100, "ret20": 90, "above_sma50": 0}}),
        ("exit_ema21", {"exit_policy": "ema21"}),
        ("exit_sma20", {"exit_policy": "sma20"}),
        ("stop_tight", {"stop_policy": "tight"}),
        ("stop_loose", {"stop_policy": "loose"}),
        ("profit_lock_25_10", {"profit_lock": {"trigger": 0.25, "trail": 0.10}}),
        ("profit_lock_40_15", {"profit_lock": {"trigger": 0.40, "trail": 0.15}}),
        ("profit_target_50", {"profit_target": 0.50}),
        ("open_gap_max_8pct", {"max_open_gap": 0.08}),
        ("open_gap_max_12pct", {"max_open_gap": 0.12}),
        ("sector_limit", {"sector_limit": True}),
    ]
    return [run_strategy_idea_backtest(data, qqq, start, label, options) for label, options in specs]


def write_variant_outputs(results, summary_name="aggressive_variant_summary.csv", prefix=""):
    out_dir = Path("research/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for result in results:
        risk_suffix = "" if result.get("risk_config") in {None, "none"} else f"_{result['risk_config']}_{result['risk_policy']}"
        extension_suffix = "" if result.get("extension_policy") in {None, "none"} else f"_{result['extension_policy']}"
        entry_suffix = "" if result.get("entry_limit") in {None, "none"} else f"_top{result['entry_limit']}"
        decision_suffix = "" if not result.get("entry_decision") else f"_{result['entry_decision']}"
        name = f"{prefix}{result['variant']}_max{result['max_positions']}{risk_suffix}{extension_suffix}{entry_suffix}{decision_suffix}"
        pd.DataFrame(result["values"], columns=["Date", "Value"]).to_csv(out_dir / f"{name}_equity_curve.csv", index=False)
        pd.DataFrame(result["trades_list"], columns=["Date", "Ticker", "Side", "Price", "Reason"]).to_csv(
            out_dir / f"{name}_trades.csv", index=False
        )
        if result.get("risk_events"):
            pd.DataFrame(result["risk_events"], columns=["Date", "RiskScore", "Reasons"]).to_csv(
                out_dir / f"{name}_risk_events.csv", index=False
            )
        rows.append(
            {
                "variant": result["variant"],
                "max_positions": result["max_positions"],
                "risk_config": result.get("risk_config", "none"),
                "risk_policy": result.get("risk_policy", "none"),
                "extension_policy": result.get("extension_policy", "none"),
                "rank_policy": result.get("rank_policy", "none"),
                "entry_limit": result.get("entry_limit", "none"),
                "entry_decision": result.get("entry_decision", "n/a"),
                "entry_system": result.get("entry_system", "momentum"),
                "min_drop": result.get("min_drop", "n/a"),
                "profit_target": result.get("profit_target", "n/a"),
                "max_hold_days": result.get("max_hold_days", "n/a"),
                "universe_size": result.get("universe_size", "n/a"),
                "loaded_tickers": result.get("loaded_tickers", "n/a"),
                "data_errors": result.get("data_errors", "n/a"),
                "stop_policy": result.get("stop_policy", "n/a"),
                "exit_policy": result.get("exit_policy", "n/a"),
                "max_open_gap": result.get("max_open_gap", "n/a"),
                "sector_limit": result.get("sector_limit", "n/a"),
                "start": result["start"],
                "end": result["end"],
                "final": result["final"],
                "cagr": result["cagr"],
                "maxdd": result["maxdd"],
                "calmar": result["calmar"],
                "trades": result["trades"],
                "round_trips": result["round_trips"],
                "win_rate": result["win_rate"],
                "avg_trade": result["avg_trade"],
                "risk_events": len(result.get("risk_events", [])),
            }
        )
    summary = pd.DataFrame(rows).sort_values(["cagr", "calmar"], ascending=False)
    summary.to_csv(out_dir / summary_name, index=False)
    return summary


def position_exit_status(position, data, qqq, date, top_tickers, variant="base"):
    ticker = position["ticker"]
    if ticker not in data or date not in data[ticker].index:
        return None

    row = data[ticker].loc[date]
    qrow = qqq.loc[date]
    highest_high = max(float(position.get("highest_high_since_entry", position["entry_price"])), float(row["High"]))
    new_stop = max(float(position.get("stop", 0.0)), variant_trailing_stop(highest_high, float(row["ATR14"]), variant))
    reasons = []
    if qrow["Close"] <= qrow["SMA200"]:
        reasons.append("QQQ below SMA200")
    if variant != "turbo" and row["Close"] < row["EMA21"]:
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
    parser.add_argument("--start", default="2018-01-01")
    parser.add_argument("--research", action="store_true", help="Run aggressive variant backtests.")
    parser.add_argument("--risk-research", action="store_true", help="Run predictive risk overlay backtests.")
    parser.add_argument("--entry-research", action="store_true", help="Run buy-decision and overextension backtests.")
    parser.add_argument("--repeat-stretch-research", action="store_true", help="Run repeat stretched recommendation backtests.")
    parser.add_argument("--dip-research", action="store_true", help="Run separate buy-the-dip entry backtests.")
    parser.add_argument("--universe-research", action="store_true", help="Run expanded universe comparison backtests.")
    parser.add_argument("--idea-research", action="store_true", help="Run strategy idea backtests.")
    args = parser.parse_args()
    if args.universe_research:
        results = run_universe_pack(args.start)
        summary = write_variant_outputs(results, "universe_comparison_summary.csv", "universe_")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    data, qqq, errors = load_universe(UNIVERSE)
    if args.idea_research:
        results = run_strategy_idea_pack(data, qqq, args.start)
        summary = write_variant_outputs(results, "strategy_idea_summary.csv", "idea_")
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    if args.repeat_stretch_research:
        results = run_repeat_stretch_pack(data, qqq, args.start)
        summary = write_variant_outputs(results, "repeat_stretch_summary.csv", "repeat_")
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    if args.dip_research:
        results = run_dip_entry_pack(data, qqq, args.start)
        summary = write_variant_outputs(results, "dip_entry_summary.csv", "dip_")
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    if args.entry_research:
        results = run_entry_decision_pack(data, qqq, args.start)
        summary = write_variant_outputs(results, "entry_decision_summary.csv", "entry_")
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    if args.risk_research:
        results = run_risk_overlay_pack(data, qqq, args.start)
        summary = write_variant_outputs(results, "risk_overlay_summary.csv", "risk_")
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
    if args.research:
        results = run_variant_pack(data, qqq, args.start)
        summary = write_variant_outputs(results)
        print(f"Loaded stocks: {len(data)} | data errors: {len(errors)}")
        print(summary.to_string(index=False, formatters={
            "final": "{:.2f}x".format,
            "cagr": "{:.1%}".format,
            "maxdd": "{:.1%}".format,
            "calmar": "{:.2f}".format,
            "win_rate": "{:.1%}".format,
            "avg_trade": "{:.1%}".format,
        }))
        return
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
