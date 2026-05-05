#!/usr/bin/env bash
set -euo pipefail

git remote add origin git@github.com:alonmorad9/real-stock-alert.git 2>/dev/null || true
git branch -M main
git push -u origin main

