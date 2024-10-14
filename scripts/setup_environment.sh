#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio

# Set up pre-commit hooks (optional, but recommended)
if [ -f .pre-commit-config.yaml ]; then
    pip install pre-commit
    pre-commit install
fi

# Create necessary directories if they don't exist
mkdir -p logs
mkdir -p data

echo "Environment setup complete. Activate it with 'source venv/bin/activate'"
