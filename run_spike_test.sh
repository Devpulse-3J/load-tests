#!/usr/bin/env bash
# DevPulse Spike Test Script
# Generates a sudden burst of high-concurrency requests to test gateway resilience and rate limiting

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p reports

HOST="${TARGET_HOST:-https://odineye.cse23.org}"
USERS="${USERS:-100}"
SPAWN_RATE="${SPAWN_RATE:-50}"
RUN_TIME="${RUN_TIME:-1m}"

echo "========================================================="
echo " Starting DevPulse Spike Test"
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
  --html reports/spike_test_report.html \
  --csv reports/spike_test_stats

echo "Spike test complete! Report generated at reports/spike_test_report.html"
