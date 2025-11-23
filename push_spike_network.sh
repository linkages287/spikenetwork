#!/bin/bash

# Script to push spike network updates to GitHub
# Usage: ./push_spike_network.sh [commit message]

COMMIT_MSG="${1:-Update spike network}"

echo "Staging spike network files..."
git add network.cpp network.h neuron.cpp neuron.h main.cpp
git add export_network.cpp test_functionality.cpp visualize_network.py
git add *.json *.sh *.py Makefile requirements.txt
git add *.md README*

echo "Checking for changes..."
if git diff --staged --quiet; then
    echo "No changes to commit."
    exit 0
fi

echo "Committing changes..."
git commit -m "$COMMIT_MSG"

echo "Pushing to GitHub..."
git push

echo "Done! Spike network updates pushed to GitHub."


