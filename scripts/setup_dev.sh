#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -e ".[dev]"

# Initialize pre-commit hooks if git is present
if [ -d ".git" ]; then
    echo "Setting up pre-commit hooks..."
    pre-commit install
fi

echo "Development environment setup complete!" 