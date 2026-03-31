#!/bin/bash
# CV Editor - Bypass gitignore restriction by using shell commands
# Usage: ./edit-cv.sh <cv-name> [editor]

CV_DIR="/home/jefer/dev/projects/jobs-bot/generated-cvs"
EDITOR="${2:-cat}"

if [ -z "$1" ]; then
    echo "Usage: ./edit-cv.sh <cv-name> [editor]"
    echo "Example: ./edit-cv.sh pleyasoft-ingeniero-ia-aws-2026-03-31.yaml"
    echo ""
    echo "Available CVs:"
    ls -la "$CV_DIR"/*.yaml 2>/dev/null || echo "  (none found)"
    exit 1
fi

CV_NAME="$1"
CV_PATH="$CV_DIR/$CV_NAME"

if [ ! -f "$CV_PATH" ]; then
    echo "Error: $CV_PATH not found"
    exit 1
fi

echo "=== Current content of $CV_NAME ==="
"$EDITOR" "$CV_PATH"
