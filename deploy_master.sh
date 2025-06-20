#!/bin/bash
# Master deployment script

# Rebuild and launch Docker containers

echo "[+] Rebuilding containers..."
docker-compose down
docker-compose up -d --build
echo "[+] Master deploy complete."
