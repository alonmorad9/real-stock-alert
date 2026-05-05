#!/usr/bin/env bash
set -euo pipefail

REPO="alonmorad9/real-stock-alert"

read -rsp "Telegram bot token: " TELEGRAM_TOKEN
printf "\n"
read -rsp "Telegram chat id: " TELEGRAM_CHAT_ID
printf "\n"

printf "%s" "$TELEGRAM_TOKEN" | gh secret set TELEGRAM_TOKEN --repo "$REPO"
printf "%s" "$TELEGRAM_CHAT_ID" | gh secret set TELEGRAM_CHAT_ID --repo "$REPO"

printf "GitHub Telegram secrets set for %s.\n" "$REPO"

read -rp "Set Cloudflare GITHUB_TOKEN now? [y/N] " SET_CLOUDFLARE
case "$SET_CLOUDFLARE" in
  [Yy]*)
    if ! command -v npx >/dev/null 2>&1; then
      echo "npx is required to run wrangler."
      exit 1
    fi
    read -rsp "Cloudflare GitHub token: " CLOUDFLARE_GITHUB_TOKEN
    printf "\n"
    printf "%s" "$CLOUDFLARE_GITHUB_TOKEN" | npx wrangler secret put GITHUB_TOKEN --config scheduler/cloudflare/wrangler.toml
    printf "Cloudflare GITHUB_TOKEN set.\n"
    ;;
  *)
    printf "Skipped Cloudflare secret.\n"
    ;;
esac

