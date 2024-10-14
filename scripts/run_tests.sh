#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate the virtual environment
source venv/bin/activate

# Run pytest with verbosity and show locals on errors
pytest -vv --tb=short --show-capture=no

# Run coverage (if installed)
if command -v coverage &> /dev/null
then
    coverage run -m pytest
    coverage report -m
    coverage html
    echo "Coverage report generated in htmlcov/index.html"
fi

# Run any additional checks (e.g., linting)
if command -v flake8 &> /dev/null
then
    echo "Running flake8..."
    flake8 src tests
fi

if command -v mypy &> /dev/null
then
    echo "Running mypy..."
    mypy src
fi

echo "All tests and checks completed."
