#!/usr/bin/env bash
#
# E1 Structural Tests Runner
#
# Usage: ./run_tests.sh [pytest-args]
#
# Examples:
#   ./run_tests.sh                    # Run all tests
#   ./run_tests.sh -v                 # Verbose
#   ./run_tests.sh test_artifact_schema.py  # Run specific file
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Running E1 Structural Tests..."
echo "=============================="
echo

# Run pytest with uv
uv run --with pytest --with pyyaml --with pydantic pytest "$@"

echo
echo "=============================="
echo "E1 tests complete"
