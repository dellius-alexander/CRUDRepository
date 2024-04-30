#!/usr/bin/env bash

if [[ ! -d ".venv" ]]; then
    echo "Creating virtual environment..."
else
    echo "Virtual environment already exists."
    exit 1
fi
# Set up environment variables for the project
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -r requirements-dev.txt
