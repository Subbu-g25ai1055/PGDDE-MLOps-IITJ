#!/bin/bash

echo "======================================="
echo "Starting Chaos Test"
echo "======================================="

echo ""
echo "[1] Stopping node3 temporarily..."
docker stop node3

sleep 10

echo ""
echo "[2] Restarting node3..."
docker start node3

sleep 5

echo ""
echo "======================================="
echo "Chaos Test Completed"
echo "======================================="