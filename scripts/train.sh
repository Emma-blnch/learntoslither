#!/bin/bash
# Headless training (no display, fast)
# Usage: ./scripts/train.sh -sessions 1000 -save models/1000sess.json
# Example: ./scripts/train.sh -sessions 100 -save models/100sess.json -board-size 10

set -e

docker run --rm -it \
    -v "$(pwd)/models:/app/models" \
    -e SDL_VIDEODRIVER=offscreen \
    -e SDL_AUDIODRIVER=dummy \
    learn2slither -visual off "$@"
