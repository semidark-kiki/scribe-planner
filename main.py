#!/usr/bin/env python3
"""Main entry point for the planner PDF generator."""

import sys

from planner.cli import parse_args
from planner.generator import generate_pdf


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()

    try:
        generate_pdf(args.year, args.month, args.output)
        print(f"Generated: {args.output}")
        return 0
    except Exception as e:
        print(f"Error generating PDF: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
