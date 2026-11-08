#!/usr/bin/env python3
"""
Validate run state YAML against schema.

Usage:
    uv run --with pydantic --with pyyaml scripts/validate-state.py <state-yaml-path>

Examples:
    # Validate single state file
    uv run --with pydantic --with pyyaml scripts/validate-state.py runs/.work/2026-11-08-fx01-short-simple/state.yaml

    # Validate all gate-set runs
    find runs/.work/2026-11-08-fx* -name state.yaml -exec uv run --with pydantic --with pyyaml scripts/validate-state.py {} \;

D3.3 implementation (session 05).
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
    from pydantic import ValidationError

    # Import from same directory
    sys.path.insert(0, str(Path(__file__).parent))
    from state_schema import RunState
except ImportError as e:
    print(f"Error: Missing dependency: {e}")
    print("Run with: uv run --with pydantic --with pyyaml scripts/validate-state.py")
    sys.exit(1)


def validate_state_file(path: Path) -> tuple[bool, list[str]]:
    """
    Validate state YAML file.

    Args:
        path: Path to state.yaml file

    Returns:
        (valid: bool, errors: list[str])
    """
    errors = []

    # Check file exists
    if not path.exists():
        return False, [f"File not found: {path}"]

    # Load YAML
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]

    # Validate with Pydantic
    try:
        state = RunState(**data)
        return True, []
    except ValidationError as e:
        # Extract error messages
        for error in e.errors():
            loc = " → ".join(str(x) for x in error["loc"])
            msg = error["msg"]
            errors.append(f"{loc}: {msg}")
        return False, errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate run state YAML against schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("state_path", type=Path, help="Path to state.yaml file")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Only print errors (no success message)"
    )

    args = parser.parse_args()

    valid, errors = validate_state_file(args.state_path)

    if valid:
        if not args.quiet:
            print(f"✓ {args.state_path}")
            print("  Valid state")
        sys.exit(0)
    else:
        print(f"✗ {args.state_path}")
        for error in errors:
            print(f"  ✗ [ERROR] {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
