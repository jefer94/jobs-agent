#!/bin/bash
# Quick render script for CVs
# Usage: ./render-cv.sh <yaml-file>

CV_DIR="/home/jefer/dev/projects/jobs-bot/generated-cvs"

if [ -z "$1" ]; then
    echo "Usage: ./render-cv.sh <yaml-file>"
    echo "Example: ./render-cv.sh pleyasoft-ingeniero-ia-aws-2026-03-31.yaml"
    exit 1
fi

YAML_FILE="$CV_DIR/$1"

if [ ! -f "$YAML_FILE" ]; then
    echo "Error: $YAML_FILE not found"
    exit 1
fi

cd "$CV_DIR" || exit 1

# Render with rendercv
rendercv render "$1"

# Move PDF to correct name
PDF_NAME="${1%.yaml}.pdf"
mv rendercv_output/Jeferson_José_De_Freitas_Pinto_CV.pdf "$PDF_NAME"

echo ""
echo "✅ Rendered: $PDF_NAME"
