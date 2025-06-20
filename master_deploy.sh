#!/bin/bash

# Master deployment script for full production setup

set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run ZEUS in live mode
echo "[+] Starting ZEUS in live trading mode..."
python3 main.py --live
