#!/usr/bin/env python3
import argparse
import json
import os
from datetime import UTC, date, datetime
from pathlib import Path

import requests

from research.real_stock_strategy import (
    UNIVERSE,
    apply_intraday_snapshots,
    latest_common_date,
    load_prices,
    load_universe,
    market_filter,
    position_exit_status,
    scan_candidates,
    variant_initial_stop,
)


STATE_FILE = Path("position_state.json")
REPORTS_DIR = Path("reports")
LATEST_REPORT = REPORTS_DIR / "latest_report.md"
SYSTEM_LABEL = "REAL STOCK SYSTEM"


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

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": message, "disable_web_page_preview": True},
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
    candidates = scan_candidates(data, qqq, asof, max_positions, profile)
    top_tickers = [item["ticker"] for item in candidates] if mode in {"weekly", "opening"} else []
    market = market_filter(qqq, asof)

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
    state["active_profile"] = profile
    state["last_action"] = f"{mode}_scan"
    save_state(state)

    open_positions = state.get("positions", [])
    open_tickers = {position["ticker"] for position in open_positions}
    slots = max(0, max_positions - len(open_positions))
    cash_per_slot = float(state.get("cash", 0.0)) / slots if slots else 0.0

    lines = [
        f"# {SYSTEM_LABEL} Report - {asof}",
        "",
        f"Mode: `{mode}`",
        f"Profile: `{profile}`",
        f"Max positions: `{max_positions}`",
        f"Data source: `{data_source}`",
        "",
        "## Market Filter",
        "",
        f"- QQQ close: {money(market['close'])}",
        f"- QQQ SMA200: {money(market['sma200'])}",
        f"- Market filter: {'ON' if market['market_on'] else 'OFF'}",
        "",
        "## Real Account State",
        "",
        f"- Allocated cash: {money(state.get('allocated_cash', 0.0))}",
        f"- Tracked cash: {money(state.get('cash', 0.0))}",
        f"- Portfolio value estimate: {money(portfolio_value)}",
        f"- Realized P&L: {money(state.get('realized_pnl', 0.0))}",
        "",
    ]

    if not open_positions:
        lines.extend(["## Open Positions", "", "No confirmed real positions are currently tracked.", ""])
    else:
        lines.extend(
            [
                "## Open Positions",
                "",
                "| Ticker | Shares | Entry | Close | Stop | Return | Status |",
                "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        status_by_ticker = {status["ticker"]: status for status in exit_statuses}
        for position in open_positions:
            status = status_by_ticker.get(position["ticker"], {})
            close = status.get("close", position["entry_price"])
            ret = close / float(position["entry_price"]) - 1
            note = "SELL: " + ", ".join(status["reasons"]) if status.get("sell") else "Hold"
            lines.append(
                f"| {position['ticker']} | {position['shares']} | {money(position['entry_price'])} | "
                f"{money(close)} | {money(position['stop'])} | {pct(ret)} | {note} |"
            )
        lines.append("")

    sell_alerts = [status for status in exit_statuses if status["sell"]]
    if sell_alerts:
        lines.extend(["## Sell Instructions", ""])
        for status in sell_alerts:
            lines.append(
                f"- SELL CANDIDATE: `{status['ticker']}` because {', '.join(status['reasons'])}. "
                "If you sell manually, confirm with `manual_sold`."
            )
        lines.append("")

    lines.extend(["## Buy Candidates", ""])
    if mode not in {"weekly", "opening"}:
        lines.append("Buy scan was not requested on this run.")
    elif not market["market_on"]:
        lines.append("No new buys. QQQ is below SMA200.")
    elif slots <= 0:
        lines.append("No new buys. Max confirmed positions are already filled.")
    else:
        buy_candidates = [candidate for candidate in candidates if candidate["ticker"] not in open_tickers][:slots]
        if not buy_candidates:
            lines.append("No qualified new buy candidates.")
        else:
            lines.extend(
                [
                    "| Rank | Ticker | Close | Suggested Allocation | Initial Stop | 63d RS | 20d Return |",
                    "| ---: | --- | ---: | ---: | ---: | ---: | ---: |",
                ]
            )
            for idx, candidate in enumerate(buy_candidates, start=1):
                lines.append(
                    f"| {idx} | {candidate['ticker']} | {money(candidate['close'])} | "
                    f"{money(cash_per_slot)} | {money(candidate['initial_stop'])} | "
                    f"{pct(candidate['rs63'])} | {pct(candidate['ret20'])} |"
                )
            lines.extend(
                [
                    "",
                    "These are instructions only. The repo does not mark a buy as real until `manual_bought` is run with the actual fill.",
                ]
            )

    if errors:
        lines.extend(["", "## Data Warnings", ""])
        for item in errors[:10]:
            lines.append(f"- {item['ticker']}: {item['error']}")

    content = write_report(asof, lines)
    send_telegram(content[:3900])
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
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "manual_bought":
        manual_bought(args)
    elif args.command == "manual_sold":
        manual_sold(args)
    else:
        build_report(args.command or "manual")


if __name__ == "__main__":
    main()
