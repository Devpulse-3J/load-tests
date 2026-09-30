#!/usr/bin/env bash
# DevPulse Standard Load Test Script
# Runs a realistic load test (10 concurrent users, spawn rate 2, 2 minutes)

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p reports

HOST="${TARGET_HOST:-https://odineye.cse23.org}"
USERS="${USERS:-10}"
SPAWN_RATE="${SPAWN_RATE:-2}"
RUN_TIME="${RUN_TIME:-2m}"

echo "========================================================="
echo " Starting DevPulse Load Test"
echo " Host:       $HOST"
echo " Users:      $USERS"
echo " Spawn Rate: $SPAWN_RATE users/sec"
echo " Duration:   $RUN_TIME"
echo "========================================================="

"$DIR/.venv/bin/locust" \
  -f locustfile.py \
  --host "$HOST" \
  --headless \
  --users "$USERS" \
  --spawn-rate "$SPAWN_RATE" \
  --run-time "$RUN_TIME" \
  --html reports/load_test_report.html \
  --csv reports/load_test_stats

echo "Load test complete! HTML report generated at reports/load_test_report.html"
