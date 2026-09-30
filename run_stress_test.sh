#!/usr/bin/env bash
# DevPulse Stress Test Script
# Ramps up concurrent users to identify service bottlenecks, database saturation, and rate-limiting limits

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p reports

HOST="${TARGET_HOST:-https://odineye.cse23.org}"
USERS="${USERS:-50}"
SPAWN_RATE="${SPAWN_RATE:-5}"
RUN_TIME="${RUN_TIME:-3m}"

echo "========================================================="
echo " Starting DevPulse Stress Test"
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
  --html reports/stress_test_report.html \
  --csv reports/stress_test_stats

echo "Stress test complete! Report generated at reports/stress_test_report.html"
