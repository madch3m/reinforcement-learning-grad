#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ -f ".venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

echo "Starting Gradio app at http://127.0.0.1:7860"
exec python gradio_app/gradio_traffic_app.py
