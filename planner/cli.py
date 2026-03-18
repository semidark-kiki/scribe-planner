"""Argument parsing and validation for CLI."""

import argparse
import sys
from typing import Optional


def validate_month(month: int) -> None:
    """Validate that month is in range 1-12.

    Args:
        month: Month value to validate

    Raises:
        ValueError: If month is not in range 1-12
    """
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")


def validate_year(year: int) -> None:
    """Validate that year is reasonable.

    Args:
        year: Year value to validate

    Raises:
        ValueError: If year is not reasonable
    """
    if not 1900 <= year <= 2100:
        raise ValueError(f"Year should be between 1900 and 2100, got {year}")


def generate_default_output_path(year: int, month: int) -> str:
    """Generate default output filename for the planner PDF.

    Args:
        year: The year
        month: The month

    Returns:
        Default output filename in format YYYY-MM-planner.pdf
    """
    return f"{year:04d}-{month:02d}-planner.pdf"


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Optional list of arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace

    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    parser = argparse.ArgumentParser(
        description="Generate a monthly planner PDF for Kindle Scribe"
    )

    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Year for the planner (e.g., 2026)",
    )

    parser.add_argument(
        "--month",
        type=int,
        required=True,
        help="Month for the planner (1-12)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: YYYY-MM-planner.pdf)",
    )

    parsed = parser.parse_args(args)

    try:
        validate_year(parsed.year)
        validate_month(parsed.month)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if parsed.output is None:
        parsed.output = generate_default_output_path(parsed.year, parsed.month)

    return parsed
