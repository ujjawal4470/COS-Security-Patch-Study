#!/bin/bash
# Run a full security scan against the configured COS VM
set -euo pipefail

BACKEND_URL=${BACKEND_URL:-"http://localhost:5000"}
LABEL=""

if [ "${1:-}" == "--label" ]; then
    LABEL="${2:-}"
    echo "Running scan with label: $LABEL"
fi

echo "Checking backend health at $BACKEND_URL..."
if ! curl -s "$BACKEND_URL/api/health" > /dev/null; then
    echo "Error: Backend is not reachable at $BACKEND_URL"
    exit 1
fi

echo "Triggering generic assessment..."
ASSESSMENT_RES=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"label\":\"$LABEL\"}" "$BACKEND_URL/api/assessment/run")
echo "$ASSESSMENT_RES"

echo "Triggering CIS benchmarks..."
CIS_RES=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"label\":\"$LABEL\"}" "$BACKEND_URL/api/cis/run")
echo "$CIS_RES"

echo "Full scan completed."
