#!/usr/bin/env python3
"""Count tokens for S2D Lab prompt/artifact files.

Usage:
    uv run --with tiktoken scripts/token-count.py [--encoding o200k_base] FILE...

Counts full file content (frontmatter + body), i.e. exactly what enters
the model context. The tiktoken encoding is a proxy: the S2D target model
is a local LLM with its own tokenizer, so treat results as comparable
estimates, not exact target-model counts.
"""

import argparse
import sys

import tiktoken


def main() -> int:
    parser = argparse.ArgumentParser(description="Count file tokens with tiktoken")
    parser.add_argument("files", nargs="+", help="files to count")
    parser.add_argument(
        "--encoding",
        default="o200k_base",
        help="tiktoken encoding name (default: o200k_base)",
    )
    args = parser.parse_args()

    enc = tiktoken.get_encoding(args.encoding)
    total = 0
    for path in args.files:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"ERROR: {path}: {e}", file=sys.stderr)
            return 1
        n = len(enc.encode(text))
        total += n
        print(f"{n:>7}  {path}")
    print(f"{total:>7}  TOTAL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
