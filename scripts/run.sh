#!/bin/bash
# Run with graphical display (X11 forwarding)
# Usage: ./scripts/run.sh [snake args...]
# Example: ./scripts/run.sh -sessions 10 -visual on -load models/100sess.txt

set -e

xhost +local:docker 2>/dev/null || true

docker run --rm -it \
    -v "$(pwd)/models:/app/models" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY="$DISPLAY" \
    --network host \
    learn2slither "$@"
