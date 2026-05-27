#!/usr/bin/env python3
import argparse
import json
import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from research.real_stock_strategy import (
    RISK_CONFIGS,
    UNIVERSE,
    add_market_risk_indicators,
    apply_intraday_snapshots,
    latest_common_date,
    load_prices,
    load_universe,
    market_filter,
    market_risk_score,
    position_exit_status,
    scan_candidates,
    variant_initial_stop,
)


STATE_FILE = Path("position_state.json")
REPORTS_DIR = Path("reports")
LATEST_REPORT = REPORTS_DIR / "latest_report.md"
SYSTEM_LABEL = "REAL STOCK SYSTEM"
CAPITAL_MODE = "TQQQ-out swing mode"
MASTER_RULE = "TQQQ has priority: if tqqq-alert sends a TQQQ re-buy signal, sell real-stock positions and move the bucket back to TQQQ."
REFERENCE_CASH = 2699.99
MARKET_TZ = ZoneInfo("America/New_York")


def observed_fixed_holiday(year, month, day):
    holiday = datetime(year, month, day).date()
    if holiday.weekday() == 5:
        return holiday - timedelta(days=1)
    if holiday.weekday() == 6:
        return holiday + timedelta(days=1)
    return holiday


def nth_weekday(year, month, weekday, n):
    day = datetime(year, month, 1).date()
    while day.weekday() != weekday:
        day += timedelta(days=1)
    return day + timedelta(days=7 * (n - 1))


def last_weekday(year, month, weekday):
    if month == 12:
        day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        day = datetime(year, month + 1, 1).date() - timedelta(days=1)
    while day.weekday() != weekday:
        day -= timedelta(days=1)
    return day


def easter_date(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day).date()


def market_holidays(year):
    return {
        observed_fixed_holiday(year, 1, 1),
        nth_weekday(year, 1, 0, 3),
        nth_weekday(year, 2, 0, 3),
        easter_date(year) - timedelta(days=2),
        last_weekday(year, 5, 0),
        observed_fixed_holiday(year, 6, 19),
        observed_fixed_holiday(year, 7, 4),
        nth_weekday(year, 9, 0, 1),
        nth_weekday(year, 11, 3, 4),
        observed_fixed_holiday(year, 12, 25),
        observed_fixed_holiday(year + 1, 1, 1),
    }


def is_market_trading_day(trading_day):
    return trading_day.weekday() < 5 and trading_day not in market_holidays(trading_day.year)


def current_market_date(now_utc=None):
    now_utc = now_utc or datetime.now(UTC)
    return now_utc.astimezone(MARKET_TZ).date()


def skip_scheduled_report_if_market_closed(mode):
    if mode not in {"opening", "daily", "weekly"}:
        return False

    market_date = current_market_date()
    if is_market_trading_day(market_date):
        return False

    print(f"[SKIP] US market is closed on {market_date}; no {mode} Telegram report sent.")
    return True


def money(value):
    return f"${float(value):,.2f}"


def pct(value):
    return f"{float(value):.1%}"


def load_state():
    with STATE_FILE.open() as f:
        return json.load(f)


def save_state(state):
    state["last_action_at"] = datetime.now(UTC).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def send_telegram(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram secrets missing; skipping send.")
        return

    chunks = []
    current = []
    current_len = 0
    for line in message.splitlines():
        addition = len(line) + 1
        if current and current_len + addition > 3900:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += addition
    if current:
        chunks.append("\n".join(current))

    for chunk in chunks:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": chunk, "disable_web_page_preview": True},
            timeout=30,
        )
        response.raise_for_status()


def report_path(asof):
    return REPORTS_DIR / f"{asof}.md"


def write_report(asof, lines):
    REPORTS_DIR.mkdir(exist_ok=True)
    content = "\n".join(lines).rstrip() + "\n"
    LATEST_REPORT.write_text(content)
    report_path(asof).write_text(content)
    return content


def get_latest_price(ticker):
    df = load_prices(ticker)
    row = df.iloc[-1]
    return df.index[-1], float(row["Close"]), float(row["High"]), float(row["ATR14"])


def strategy_profile(state):
    return state.get("settings", {}).get("profile", "base")


def live_risk_config():
    return next(config for config in RISK_CONFIGS if config["name"] == "risk_balanced")


def risk_guidance(qqq, asof):
    config = live_risk_config()
    risk_score, reasons = market_risk_score(add_market_risk_indicators(qqq), asof, config)
    if risk_score >= config["defensive_threshold"]:
        return {
            "level": "DEFENSIVE",
            "score": risk_score,
            "reasons": reasons,
            "allocation_multiplier": 0.5,
            "action": "Use half-size only for new buys. Do not auto-sell from this overlay.",
        }
    if risk_score >= config["elevated_threshold"]:
        return {
            "level": "ELEVATED",
            "score": risk_score,
            "reasons": reasons,
            "allocation_multiplier": 0.5,
            "action": "Use half-size for new buys.",
        }
    return {
        "level": "NORMAL",
        "score": risk_score,
        "reasons": reasons,
        "allocation_multiplier": 1.0,
        "action": "Use normal suggested allocation.",
    }


def update_bot_only_benchmark(state, data, qqq, asof, candidates, top_tickers, market, risk, max_positions, profile):
    benchmark = state.get("bot_only_benchmark") or {}
    initial_cash = float(
        benchmark.get("initial_cash")
        or state.get("allocated_cash")
        or REFERENCE_CASH
    )
    cash = float(benchmark.get("cash", initial_cash))
    positions = benchmark.get("positions", [])
    realized_pnl = float(benchmark.get("realized_pnl", 0.0))
    actions = []
    trade_messages = []

    kept_positions = []
    for position in positions:
        status = position_exit_status(position, data, qqq, asof, top_tickers, profile)
        if not status:
            kept_positions.append(position)
            continue

        position["highest_high_since_entry"] = round(status["highest_high_since_entry"], 4)
        position["stop"] = round(status["stop"], 4)
        if status["sell"]:
            shares = float(position["shares"])
            entry_price = float(position["entry_price"])
            close = float(status["close"])
            proceeds = shares * close
            trade_pnl = shares * (close - entry_price)
            trade_return = close / entry_price - 1 if entry_price else 0.0
            reasons = ", ".join(status["reasons"])
            realized_pnl += trade_pnl
            cash += proceeds
            actions.append(f"sold {position['ticker']}")
            trade_messages.append(
                f"BOT SELL {position['ticker']}: {shares:.4f} shares at {money(close)}; "
                f"proceeds {money(proceeds)}; P&L {money(trade_pnl)} ({pct(trade_return)}). "
                f"Reason: {reasons}."
            )
        else:
            kept_positions.append(position)

    positions = kept_positions
    if market["market_on"] and len(positions) < max_positions and cash > 0:
        open_tickers = {position["ticker"] for position in positions}
        for candidate in candidates:
            if len(positions) >= max_positions or cash <= 0:
                break
            if candidate["ticker"] in open_tickers:
                continue

            slots_left = max_positions - len(positions)
            allocation = min(cash, (cash / slots_left) * risk["allocation_multiplier"])
            if allocation <= 0:
                continue
            ticker = candidate["ticker"]
            close = float(candidate["close"])
            row = data[ticker].loc[asof]
            shares = allocation / close
            positions.append(
                {
                    "ticker": ticker,
                    "entry_date": asof.isoformat(),
                    "entry_price": round(close, 4),
                    "shares": round(shares, 8),
                    "highest_high_since_entry": round(max(close, float(row["High"])), 4),
                    "stop": round(float(candidate["initial_stop"]), 4),
                    "allocation": round(allocation, 2),
                    "last_signal": "bot_only_bought",
                }
            )
            cash -= allocation
            open_tickers.add(ticker)
            actions.append(f"bought {ticker}")
            trade_messages.append(
                f"BOT BUY {ticker}: {money(allocation)} at {money(close)} = {shares:.4f} shares. "
                f"Initial stop {money(candidate['initial_stop'])}."
            )

    value = cash
    position_details = []
    for position in positions:
        ticker = position["ticker"]
        if ticker in data and asof in data[ticker].index:
            close = float(data[ticker].loc[asof]["Close"])
        else:
            close = float(position["entry_price"])
        position_value = float(position["shares"]) * close
        entry_price = float(position["entry_price"])
        value += position_value
        position_details.append(
            {
                "ticker": ticker,
                "shares": round(float(position["shares"]), 8),
                "entry_date": position.get("entry_date"),
                "entry_price": round(entry_price, 4),
                "current_price": round(close, 4),
                "stop": round(float(position.get("stop", 0.0)), 4),
                "value": round(position_value, 2),
                "return": round(close / entry_price - 1, 6) if entry_price else 0.0,
                "status": "HOLD",
            }
        )

    if not trade_messages:
        trade_messages = ["BOT HOLD: no bot-only buy or sell this run."]

    benchmark.update(
        {
            "initial_cash": round(initial_cash, 2),
            "cash": round(cash, 2),
            "positions": positions,
            "position_details": position_details,
            "value": round(value, 2),
            "return": round(value / initial_cash - 1, 6) if initial_cash else 0.0,
            "realized_pnl": round(realized_pnl, 2),
            "last_scan_date": asof.isoformat(),
            "last_actions": actions or ["held"],
            "last_trade_messages": trade_messages,
            "meaning": "Paper benchmark: what the real-stock bot would track if its own buy/sell instructions were followed automatically.",
        }
    )
    state["bot_only_benchmark"] = benchmark
    return benchmark


def manual_bought(args):
    state = load_state()
    ticker = args.ticker.upper()
    shares = float(args.shares)
    fill_price = float(args.fill_price)
    fill_date = args.date or date.today().isoformat()
    if shares <= 0 or fill_price <= 0:
        raise SystemExit("shares and fill_price must be positive")
    if any(pos["ticker"] == ticker for pos in state.get("positions", [])):
        raise SystemExit(f"{ticker} is already in position_state.json")

    allocation = shares * fill_price
    if allocation > float(state.get("cash", 0.0)) + 0.01:
        raise SystemExit(f"Not enough tracked cash for {ticker}: need {money(allocation)}")

    try:
        _, _, high, atr14 = get_latest_price(ticker)
        stop = variant_initial_stop(fill_price, atr14, strategy_profile(state))
        highest_high = max(fill_price, high)
    except Exception:
        stop = fill_price * 0.88
        highest_high = fill_price

    state.setdefault("positions", []).append(
        {
            "ticker": ticker,
            "entry_date": fill_date,
            "entry_price": fill_price,
            "shares": shares,
            "highest_high_since_entry": round(highest_high, 4),
            "stop": round(stop, 4),
            "allocation": round(allocation, 2),
            "last_signal": "manual_bought",
        }
    )
    state["cash"] = round(float(state.get("cash", 0.0)) - allocation, 2)
    state["last_action"] = f"manual_bought {ticker} {shares} @ {fill_price}"
    save_state(state)
    print(f"Confirmed manual buy: {ticker} {shares} shares at {money(fill_price)}")


def manual_sold(args):
    state = load_state()
    ticker = args.ticker.upper()
    shares = float(args.shares)
    fill_price = float(args.fill_price)
    fill_date = args.date or date.today().isoformat()
    positions = state.get("positions", [])
    position = next((pos for pos in positions if pos["ticker"] == ticker), None)
    if not position:
        raise SystemExit(f"{ticker} is not in position_state.json")
    if shares <= 0 or fill_price <= 0:
        raise SystemExit("shares and fill_price must be positive")
    if shares > float(position["shares"]) + 1e-8:
        raise SystemExit(f"Cannot sell more shares than tracked for {ticker}")

    proceeds = shares * fill_price
    realized = shares * (fill_price - float(position["entry_price"]))
    remaining = round(float(position["shares"]) - shares, 8)
    state["cash"] = round(float(state.get("cash", 0.0)) + proceeds, 2)
    state["realized_pnl"] = round(float(state.get("realized_pnl", 0.0)) + realized, 2)
    if remaining <= 1e-8:
        state["positions"] = [pos for pos in positions if pos["ticker"] != ticker]
    else:
        position["shares"] = remaining
        position["allocation"] = round(remaining * float(position["entry_price"]), 2)
        position["last_signal"] = "partial_manual_sold"
    state["last_action"] = f"manual_sold {ticker} {shares} @ {fill_price} on {fill_date}"
    save_state(state)
    print(f"Confirmed manual sell: {ticker} {shares} shares at {money(fill_price)}")


def set_cash(args):
    state = load_state()
    amount = float(args.amount)
    if amount < 0:
        raise SystemExit("amount must be non-negative")
    if state.get("positions"):
        raise SystemExit("Cannot reset cash while positions are tracked. Sell and confirm positions first.")

    state["allocated_cash"] = round(amount, 2)
    state["cash"] = round(amount, 2)
    state["realized_pnl"] = 0.0
    state["latest_portfolio_value"] = round(amount, 2)
    state["latest_unrealized_pnl"] = 0.0
    state["capital_mode"] = CAPITAL_MODE
    state["master_rule"] = MASTER_RULE
    state["last_action"] = f"set_cash {amount:.2f}"
    save_state(state)
    send_telegram(
        "\n".join([
            "🧩 Real-Stock Cash Bucket Set",
            "─" * 30,
            f"Tracked cash: {money(amount)}",
            f"Mode: {CAPITAL_MODE}",
            "TQQQ has priority. If tqqq-alert sends a re-buy signal, sell real-stock positions and move back to TQQQ.",
        ])
    )
    print(f"Set real-stock cash bucket to {money(amount)}")


def reset_bot_benchmark(_args):
    state = load_state()
    state["bot_only_benchmark"] = {
        "initial_cash": REFERENCE_CASH,
        "cash": REFERENCE_CASH,
        "positions": [],
        "position_details": [],
        "value": REFERENCE_CASH,
        "return": 0.0,
        "realized_pnl": 0.0,
        "last_scan_date": None,
        "last_actions": ["reset"],
        "last_trade_messages": ["BOT RESET: bot-only benchmark reset to cash."],
        "meaning": "Paper benchmark: what the real-stock bot would track if its own buy/sell instructions were followed automatically.",
    }
    state["last_action"] = "reset_bot_benchmark"
    save_state(state)
    send_telegram(
        "\n".join([
            "🧪 Bot-Only Benchmark Reset",
            "─" * 30,
            f"Benchmark cash: {money(REFERENCE_CASH)}",
            "Paper positions cleared.",
            "Real stock positions and real cash were not changed.",
            "The next scan will start the paper benchmark fresh under the current rules.",
        ])
    )
    print("Reset bot-only benchmark to cash.")


def build_report(mode):
    state = load_state()
    data, qqq, errors = load_universe(UNIVERSE)
    data_source = "daily Yahoo bars"
    if mode == "opening":
        data, qqq, intraday_errors = apply_intraday_snapshots(data, qqq)
        errors.extend(intraday_errors)
        data_source = "daily Yahoo bars with intraday 1-minute opening snapshot"
    asof = latest_common_date(data, qqq)
    settings = state.get("settings", {})
    max_positions = int(settings.get("max_positions", 2))
    profile = strategy_profile(state)
    previous_targets = list(
        dict.fromkeys(
            state.get("latest_candidates", [])
            + [item["ticker"] for item in state.get("latest_skipped_candidates", [])]
        )
    )
    rank_policy = settings.get("rank_policy", "skip_repeat_stretched")
    max_atr_pct = settings.get("max_atr_pct")
    raw_candidates = scan_candidates(data, qqq, asof, max_positions, profile)
    candidates, skipped_candidates = scan_candidates(
        data,
        qqq,
        asof,
        max_positions,
        profile,
        rank_policy,
        previous_targets,
        True,
        max_atr_pct,
    )
    buy_scan_modes = {"weekly", "opening", "daily"}
    top_tickers = [item["ticker"] for item in raw_candidates] if mode == "weekly" else []
    market = market_filter(qqq, asof)
    risk = risk_guidance(qqq, asof)

    exit_statuses = []
    portfolio_value = float(state.get("cash", 0.0))
    for position in state.get("positions", []):
        status = position_exit_status(position, data, qqq, asof, top_tickers, profile)
        if status:
            position["highest_high_since_entry"] = round(status["highest_high_since_entry"], 4)
            position["stop"] = round(status["stop"], 4)
            exit_statuses.append(status)
            portfolio_value += float(position["shares"]) * status["close"]
        else:
            portfolio_value += float(position["shares"]) * float(position["entry_price"])

    state["last_scan_date"] = asof.isoformat()
    state["latest_portfolio_value"] = round(portfolio_value, 2)
    state["latest_unrealized_pnl"] = round(portfolio_value - float(state.get("allocated_cash", 0.0)), 2)
    state["latest_candidates"] = [candidate["ticker"] for candidate in candidates]
    state["latest_skipped_candidates"] = [
        {"ticker": candidate["ticker"], "reason": candidate["skip_reason"]}
        for candidate in skipped_candidates[:max_positions]
    ]
    state["latest_market_risk"] = {
        "level": risk["level"],
        "score": risk["score"],
        "reasons": risk["reasons"],
        "allocation_multiplier": risk["allocation_multiplier"],
    }
    benchmark_candidates = candidates if mode in buy_scan_modes else []
    bot_benchmark = update_bot_only_benchmark(
        state,
        data,
        qqq,
        asof,
        benchmark_candidates,
        top_tickers,
        market,
        risk,
        max_positions,
        profile,
    )
    state["active_profile"] = profile
    state["last_action"] = f"{mode}_scan"
    save_state(state)

    open_positions = state.get("positions", [])
    open_tickers = {position["ticker"] for position in open_positions}
    slots = max(0, max_positions - len(open_positions))
    tracked_cash = float(state.get("cash", 0.0))
    planning_cash = tracked_cash if tracked_cash > 0 else REFERENCE_CASH
    cash_per_slot = planning_cash / slots if slots else 0.0
    risk_adjusted_cash_per_slot = cash_per_slot * risk["allocation_multiplier"]
    benchmark_value = float(bot_benchmark.get("value", 0.0))
    benchmark_initial = float(bot_benchmark.get("initial_cash", REFERENCE_CASH))
    benchmark_return = float(bot_benchmark.get("return", 0.0))
    benchmark_gap = portfolio_value - benchmark_value
    benchmark_gap_pct = benchmark_gap / benchmark_value if benchmark_value else 0.0
    benchmark_holdings = ", ".join(
        item["ticker"] for item in bot_benchmark.get("positions", [])
    ) or "cash"

    sep = "─" * 30
    report_date = asof.strftime("%d/%m/%Y")
    capital_mode = state.get("capital_mode", CAPITAL_MODE)
    atr_cap_text = pct(max_atr_pct) if max_atr_pct is not None else "none"
    risk_reasons = ", ".join(risk["reasons"]) if risk["reasons"] else "none"
    position_word = "position" if len(open_positions) == 1 else "positions"
    if mode not in buy_scan_modes:
        action = "ℹ️ INFO — Buy scan was not requested"
    elif not market["market_on"]:
        action = "⏸️ NO STOCK BUY — QQQ below SMA200"
    elif slots <= 0:
        action = "✅ HOLD — Max stock positions already filled"
    elif tracked_cash <= 0:
        action = "👀 WATCHLIST — Planning only while TQQQ is open"
    else:
        action = "🟢 REVIEW BUYS — Candidates available"

    lines = [
        f"📊 Real Stock {mode.title()} Report — {report_date}",
        sep,
        f"Action: {action}",
        "Read first: TQQQ is the master system. Use these stock candidates only when the TQQQ bucket is available for stocks.",
        sep,
        f"Mode:          {mode}",
        f"Capital Mode:  {capital_mode}",
        f"Profile:       {profile} — aggressive momentum leaders, not dip buys",
        f"Max Positions: {max_positions}",
        f"Data Source:   {data_source}",
        sep,
        "🧭 Market Filter",
        "Meaning: controls whether new stock buys are allowed.",
        "What to do: if this is OFF, do not start new stock positions.",
        f"QQQ:           {money(market['close'])}",
        f"SMA200:        {money(market['sma200'])}",
        f"Status:        {'ON' if market['market_on'] else 'OFF'}",
        sep,
        "🛡️ Market Risk Overlay",
        "Meaning: controls suggested buy size only; it does not choose tickers and does not auto-sell.",
        "What to do: NORMAL means use the full suggested buy amount; ELEVATED/DEFENSIVE means size down.",
        f"Risk Level:    {risk['level']}",
        f"Risk Score:    {risk['score']}",
        f"Buy Size:      {pct(risk['allocation_multiplier'])} of normal",
        f"Reasons:       {risk_reasons}",
        f"Action:        {risk['action']}",
        sep,
        "⚙️ Strategy Settings",
        "Meaning: these rules decide which stocks appear in the candidate list.",
        "What to do: use the score and warnings together; the highest score is not a guarantee.",
        f"Turbo:         ranks strong momentum leaders",
        f"Score:         63d relative strength vs QQQ + 20d return",
        f"Rank Policy:   {rank_policy}",
        f"ATR Cap:       {atr_cap_text} max ATR14/price for fresh buys",
        "Repeat Rule:   recent stretched names are skipped so the list does not chase the same hot ticker forever",
        sep,
        "💼 Real Stock Bucket",
        f"Allocated:     {money(state.get('allocated_cash', 0.0))}",
        f"Tracked Cash:  {money(tracked_cash)}",
        f"Planning Cash: {money(planning_cash)} — used only to size suggestions in this message",
        f"Open:          {len(open_positions)} confirmed {position_word}",
        f"Value Est.:    {money(portfolio_value)}",
        f"Realized P&L:  {money(state.get('realized_pnl', 0.0))}",
        sep,
        "🧪 Bot-Only Benchmark",
        "Meaning: paper path showing what this stock bot would do if its own buy/sell instructions were followed automatically.",
        "What to do: use this to compare your confirmed real-stock bucket against the bot path; it is not a trade instruction.",
        f"Start Cash:    {money(benchmark_initial)}",
        f"Bot Value:     {money(benchmark_value)} ({pct(benchmark_return)})",
        f"Real Bucket:   {money(portfolio_value)}",
        f"Vs Bot-Only:   {money(benchmark_gap)} ({pct(benchmark_gap_pct)})",
        f"Bot Cash:      {money(bot_benchmark.get('cash', 0.0))}",
        f"Bot Holding:   {benchmark_holdings}",
        f"Bot Actions:   {', '.join(bot_benchmark.get('last_actions', ['held']))}",
        sep,
        "🤖 Bot-Only Trade Log",
        "Meaning: simulated paper events only. These show what the bot path did, not what happened in your broker.",
    ]

    for message in bot_benchmark.get("last_trade_messages", ["BOT HOLD: no bot-only buy or sell this run."]):
        lines.append(f"- {message}")

    lines.extend([
        sep,
        "📌 Bot-Only Holdings",
    ])

    bot_position_details = bot_benchmark.get("position_details", [])
    if not bot_position_details:
        lines.extend(["Bot-only benchmark is in cash.", sep])
    else:
        for detail in bot_position_details:
            lines.extend([
                f"{detail['ticker']}",
                f"Shares:        {float(detail.get('shares', 0.0)):.4f}",
                f"Entry:         {money(detail.get('entry_price', 0.0))}",
                f"Current:       {money(detail.get('current_price', 0.0))}",
                f"Stop:          {money(detail.get('stop', 0.0))}",
                f"Value:         {money(detail.get('value', 0.0))}",
                f"Return:        {pct(detail.get('return', 0.0))}",
                f"Status:        {detail.get('status', 'HOLD')}",
                "",
            ])
        lines.append(sep)

    if not open_positions:
        lines.extend(["📦 Open Positions", "No confirmed real stock positions are currently tracked.", sep])
    else:
        lines.extend(["📦 Open Positions"])
        status_by_ticker = {status["ticker"]: status for status in exit_statuses}
        for position in open_positions:
            status = status_by_ticker.get(position["ticker"], {})
            close = status.get("close", position["entry_price"])
            ret = close / float(position["entry_price"]) - 1
            note = "SELL: " + ", ".join(status["reasons"]) if status.get("sell") else "Hold"
            lines.extend([
                f"{position['ticker']}",
                f"Shares:        {position['shares']}",
                f"Entry:         {money(position['entry_price'])}",
                f"Close:         {money(close)}",
                f"Stop:          {money(position['stop'])}",
                f"Return:        {pct(ret)}",
                f"Status:        {note}",
                "",
            ])
        lines.append(sep)

    sell_alerts = [status for status in exit_statuses if status["sell"]]
    if sell_alerts:
        lines.extend(["🚨 Sell Instructions"])
        for status in sell_alerts:
            lines.append(
                f"{status['ticker']}: SELL CANDIDATE because {', '.join(status['reasons'])}. "
                "If you sell manually, confirm with manual_sold."
            )
        lines.append(sep)

    lines.extend(["🧾 Buy Candidates"])
    if mode not in buy_scan_modes:
        lines.append("Buy scan was not requested on this run.")
    elif not market["market_on"]:
        lines.append("No new buys. QQQ is below SMA200.")
    elif slots <= 0:
        lines.append("No new buys. Max confirmed positions are already filled.")
    else:
        buy_candidates = [candidate for candidate in candidates if candidate["ticker"] not in open_tickers][:slots]
        visible_skips = [candidate for candidate in skipped_candidates if candidate["ticker"] not in open_tickers]
        if rank_policy == "skip_repeat_stretched" and previous_targets:
            lines.append(f"Repeat Memory: {', '.join(previous_targets)}")
            lines.append("Meaning: these tickers were recent candidates/skips and can be skipped if still stretched.")
            lines.append("")
        if visible_skips:
            lines.extend(["Skipped Candidates"])
            for candidate in visible_skips[:max_positions]:
                if candidate.get("skip_reason", "").startswith("ATR14"):
                    atr_pct = candidate["atr14"] / candidate["close"] if candidate["close"] else 0.0
                    lines.append(
                        f"{candidate['ticker']}: skipped because ATR14 is {pct(atr_pct)}, above the "
                        f"{pct(max_atr_pct)} fresh-buy cap."
                    )
                else:
                    lines.append(
                        f"{candidate['ticker']}: skipped because it was already a recent target and is still stretched "
                        f"({candidate['extension_warning']})."
                    )
            lines.append("")
        if not buy_candidates:
            lines.append("No qualified new buy candidates.")
        else:
            for idx, candidate in enumerate(buy_candidates, start=1):
                approx_shares = risk_adjusted_cash_per_slot / candidate["close"] if candidate["close"] else 0.0
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else f"{idx}."
                lines.extend([
                    f"{medal} {candidate['ticker']}",
                    f"Price:         {money(candidate['close'])}",
                    f"Score:         {candidate['score']:.2f} — higher means stronger momentum rank",
                    f"Suggested Buy: {money(risk_adjusted_cash_per_slot)} ({approx_shares:.4f} shares)",
                    f"Normal Slot:   {money(cash_per_slot)}",
                    f"Initial Stop:  {money(candidate['initial_stop'])}",
                    f"63d RS:        {pct(candidate['rs63'])}",
                    f"20d Return:    {pct(candidate['ret20'])}",
                    f"Stretch:       {candidate['extension_warning']}",
                    "",
                ])
            stretched = [candidate for candidate in buy_candidates if candidate["extension_warning"] != "OK"]
            if stretched:
                lines.extend(["⚠️ Overextension Warnings"])
                lines.append("Meaning: these are hot names. The signal can still be valid, but avoid chasing a live price far above the report price.")
                for candidate in stretched:
                    lines.append(
                        f"{candidate['ticker']}: {candidate['extension_warning']}"
                    )
            lines.extend(
                [
                    sep,
                    "These are instructions only. The repo does not mark a buy as real until manual_bought is run with the actual fill.",
                ]
            )

    if errors:
        lines.extend([sep, "⚠️ Data Warnings"])
        for item in errors[:10]:
            lines.append(f"- {item['ticker']}: {item['error']}")

    content = write_report(asof, lines)
    send_telegram(content)
    print(content)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("weekly")
    subparsers.add_parser("opening")
    subparsers.add_parser("daily")
    subparsers.add_parser("manual")

    bought = subparsers.add_parser("manual_bought")
    bought.add_argument("ticker")
    bought.add_argument("shares", type=float)
    bought.add_argument("fill_price", type=float)
    bought.add_argument("--date")

    sold = subparsers.add_parser("manual_sold")
    sold.add_argument("ticker")
    sold.add_argument("shares", type=float)
    sold.add_argument("fill_price", type=float)
    sold.add_argument("--date")

    reset = subparsers.add_parser("set_cash")
    reset.add_argument("amount", type=float)
    subparsers.add_parser("reset_bot_benchmark")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "manual_bought":
        manual_bought(args)
    elif args.command == "manual_sold":
        manual_sold(args)
    elif args.command == "set_cash":
        set_cash(args)
    elif args.command == "reset_bot_benchmark":
        reset_bot_benchmark(args)
    else:
        mode = args.command or "manual"
        if skip_scheduled_report_if_market_closed(mode):
            return
        build_report(mode)


if __name__ == "__main__":
    main()
