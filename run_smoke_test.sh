#!/usr/bin/env bash
# DevPulse Smoke Test Script
# Runs a quick 30-second verification with 1 user against https://odineye.cse23.org

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p reports

HOST="${TARGET_HOST:-https://odineye.cse23.org}"
echo "Running DevPulse Smoke Test against $HOST..."

"$DIR/.venv/bin/locust" \
  -f locustfile.py \
  --host "$HOST" \
  --headless \
  --users 1 \
  --spawn-rate 1 \
  --run-time 30s \
  --html reports/smoke_test_report.html \
  --csv reports/smoke_test_stats

echo "Smoke test completed! Report saved to reports/smoke_test_report.html"
