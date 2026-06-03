#!/bin/bash
# Check Python norm (flake8 / norminette_python)
# Usage: ./scripts/norm.sh

set -e

cd "$(dirname "$0")/.."
docker run --rm \
    -v "$(pwd):/app" \
    --entrypoint python3 \
    learn2slither -m flake8 --max-line-length=79 \
    --exclude=__pycache__,.git \
    .
