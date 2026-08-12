#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

while true; do
    echo
    echo "=============================="
    echo "  PERFUMERY - ELT CONTROL"
    echo "=============================="
    echo "1) Run ELT pipeline"
    echo "2) View Silver and Gold tables"
    echo "3) Run quality checks"
    echo "0) Exit"
    read -r -p "Choose an option: " option

    case "$option" in
        1) "$PYTHON_BIN" main.py ;;
        2) "$PYTHON_BIN" main.py view ;;
        3) "$PYTHON_BIN" -m elt.run_quality_checks ;;
        0) exit 0 ;;
        *) echo "Invalid option." ;;
    esac
done

