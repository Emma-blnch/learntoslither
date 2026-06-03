#!/bin/bash
set -e

cd "$(dirname "$0")/.."
docker build -t learn2slither .
echo "Image learn2slither built."
