#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python3 -u src/ui/tui_app.py "$@"
