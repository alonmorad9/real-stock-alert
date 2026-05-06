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


def scan_candidates(data, qqq, date, max_positions=2, variant="base"):
    candidates = []
    for ticker in data:
        signal = candidate_for(data, qqq, ticker, date, variant)
        if signal:
            candidates.append(signal)
    return sorted(candidates, key=lambda item: item["score"], reverse=True)[:max_positions]


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
        return rs63 * 90 + row["RET20"] * 80 + above_sma50 * 35
    return rs63 * 100 + row["RET20"] * 35 + above_sma50 * 20


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


def rank_for_date(data, qqq, date, positions, variant):
    if date not in qqq.index:
        return []
    qrow = qqq.loc[date]
    ranked = []
    for ticker, df in data.items():
        if ticker in positions or date not in df.index:
            continue
        row = df.loc[date]
        if qualifies_for_variant(row, qrow, variant):
            ranked.append((float(score_candidate(row, qrow, variant)), ticker))
    ranked.sort(reverse=True)
    return [ticker for _, ticker in ranked]


def risk_multiplier(risk_score, config, policy):
    if not policy or policy == "none":
        return 1.0
    if policy == "block_elevated" and risk_score >= config["elevated_threshold"]:
        return 0.0
    if policy == "half_elevated" and risk_score >= config["elevated_threshold"]:
        return 0.5
    return 1.0


def run_rotation_backtest(
    data,
    qqq,
    start="2018-01-01",
    max_positions=2,
    variant="base",
    risk_config=None,
    risk_policy="none",
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

            for ticker in target_tickers:
                if not market_ok or ticker in positions or ticker not in data or date not in data[ticker].index:
                    continue
                if len(positions) >= max_positions:
                    break
                row = data[ticker].loc[date]
                slots_left = max_positions - len(positions)
                target_value = equity / max_positions
                multiplier = risk_multiplier(risk_score, risk_config, risk_policy)
                allocation = min(cash, target_value * multiplier if slots_left > 1 else cash * multiplier)
                if allocation <= 0:
                    trades.append((date, ticker, "skip", row["Open"], f"{risk_policy}_risk_score_{risk_score}"))
                    continue
                shares = allocation / row["Open"]
                cash -= allocation
                stop = variant_initial_stop(float(row["Open"]), float(row["ATR14"]), variant)
                positions[ticker] = BacktestPosition(ticker, shares, row["Open"], date, row["High"], stop)
                trades.append((date, ticker, "buy", row["Open"], f"{variant}_momentum"))
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
            target_tickers = (held + rank_for_date(data, qqq, date, positions, variant))[:max_positions]
            rebalance_next_open = True

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
    return {
        "variant": variant,
        "max_positions": max_positions,
        "start": values[0][0],
        "end": values[-1][0],
        "final": final,
        "cagr": annual,
        "maxdd": dd,
        "calmar": annual / abs(dd) if dd else np.nan,
        "trades": len(trades),
        "round_trips": len(wins),
        "win_rate": float(np.mean([win > 0 for win in wins])) if wins else np.nan,
        "avg_trade": float(np.mean(wins)) if wins else np.nan,
        "risk_policy": risk_policy,
        "risk_config": risk_config["name"] if risk_config else "none",
        "risk_events": risk_events,
        "values": values,
        "trades_list": trades,
    }


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


def write_variant_outputs(results, summary_name="aggressive_variant_summary.csv", prefix=""):
    out_dir = Path("research/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for result in results:
        risk_suffix = "" if result.get("risk_config") in {None, "none"} else f"_{result['risk_config']}_{result['risk_policy']}"
        name = f"{prefix}{result['variant']}_max{result['max_positions']}{risk_suffix}"
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
    args = parser.parse_args()
    data, qqq, errors = load_universe(UNIVERSE)
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
