#!/bin/bash

# --- AUTO-DETECT PROJECT PATH ---
# Ensures the script works regardless of where it is executed from
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Move to the project root so Python relative paths work correctly
cd "$PROJECT_ROOT"

# --- CONFIGURATION ---
PYTHON_BIN="./venvp/bin/python"
PROJECT_NAME="Niche Perfumery Pipeline"

# Console colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- FUNCTIONS ---

show_banner() {
    clear
    echo -e "${BLUE}============================================================${NC}"
    echo -e "          ${BLUE}CONTROL PANEL - $PROJECT_NAME${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

run_pipeline() {
    echo -e "${YELLOW}>>> Starting Full Pipeline Execution...${NC}"
    $PYTHON_BIN main.py
}

check_health() {
    echo -e "${YELLOW}>>> Checking System Health...${NC}"
    
    if command -v psql > /dev/null; then
        echo -n "PostgreSQL: "
        if pg_isready -h localhost > /dev/null 2>&1; then
            echo -e "${GREEN}[OK]${NC}"
        else
            echo -e "${RED}[ERROR] Could not connect to Postgres${NC}"
        fi
    fi

    echo -n "Data Layers (Delta): "
    if [ -d "data/bronze" ] && [ -d "data/silver" ] && [ -d "data/gold" ]; then
        echo -e "${GREEN}[OK]${NC}"
    else
        echo -e "${YELLOW}[WARNING] Layers missing. Please run the pipeline.${NC}"
    fi
}

show_silver() {
    echo -e "${BLUE}--- Silver Layer Explorer ---${NC}"
    echo "1) Sales Enriched"
    echo "2) Customers Enriched"
    echo "3) Perfumes Enriched"
    echo "4) Inventory Enriched"
    echo "5) Back"
    read -p "Select a table: " sil_opt
    
    case $sil_opt in
        1) $PYTHON_BIN main.py --table sales_enriched ;;
        2) $PYTHON_BIN main.py --table customers_enriched ;;
        3) $PYTHON_BIN main.py --table perfumes_enriched ;;
        4) $PYTHON_BIN main.py --table inventory_enriched ;;
        *) return ;;
    esac
}

show_gold() {
    echo -e "${BLUE}--- Gold Layer Summary ---${NC}"
    $PYTHON_BIN main.py --gold
}

check_stock() {
    echo -e "${RED}>>> CRITICAL STOCK ALERTS <<<${NC}"
    $PYTHON_BIN main.py --table inventory_enriched | grep -E "brand|perfume|size_ml|current_stock| [0-4]$| 0$"
}

# --- MAIN MENU ---

while true; do
    show_banner
    echo -e "1) ${GREEN}Run Pipeline${NC} (Full ETL)"
    echo -e "2) ${GREEN}Health Check${NC} (Postgres & Files)"
    echo -e "3) ${GREEN}Explore Silver Layer${NC} (Enriched Tables)"
    echo -e "4) ${GREEN}View Gold Layer${NC} (Aggregations)"
    echo -e "5) ${YELLOW}Stock Alerts${NC} (Critical)"
    echo -e "6) ${BLUE}Clear Cache${NC} (__pycache__)"
    echo -e "0) Exit"
    echo -e "${BLUE}============================================================${NC}"
    read -p "Choose an option: " opcion

    case $opcion in
        1) run_pipeline ;;
        2) check_health ;;
        3) show_silver ;;
        4) show_gold ;;
        5) check_stock ;;
        6) 
            find . -type d -name "__pycache__" -exec rm -rf {} +
            echo -e "${GREEN}Cache cleared.${NC}"
            ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo -e "${RED}Invalid option.${NC}" ;;
    esac
    
    read -p "Press [Enter] to continue..."
done
