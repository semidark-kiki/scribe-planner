"""Tests for the CLI module."""

import pytest
from planner.cli import (
    parse_args,
    validate_month,
    validate_year,
    generate_default_output_path,
)


class TestValidateMonth:
    """Tests for month validation."""

    def test_valid_month(self):
        """Should not raise for valid months."""
        for m in range(1, 13):
            validate_month(m)

    def test_invalid_month_zero(self):
        """Should raise for month 0."""
        with pytest.raises(ValueError, match="Month must be between 1 and 12"):
            validate_month(0)

    def test_invalid_month_thirteen(self):
        """Should raise for month 13."""
        with pytest.raises(ValueError, match="Month must be between 1 and 12"):
            validate_month(13)

    def test_invalid_month_negative(self):
        """Should raise for negative month."""
        with pytest.raises(ValueError, match="Month must be between 1 and 12"):
            validate_month(-1)


class TestValidateYear:
    """Tests for year validation."""

    def test_valid_year(self):
        """Should not raise for valid years."""
        validate_year(2026)
        validate_year(1900)
        validate_year(2100)

    def test_invalid_year_before_1900(self):
        """Should raise for year before 1900."""
        with pytest.raises(ValueError, match="Year should be between 1900 and 2100"):
            validate_year(1899)

    def test_invalid_year_after_2100(self):
        """Should raise for year after 2100."""
        with pytest.raises(ValueError, match="Year should be between 1900 and 2100"):
            validate_year(2101)


class TestGenerateDefaultOutputPath:
    """Tests for default output path generation."""

    def test_default_naming_format(self):
        """Should generate correct default filename format."""
        assert generate_default_output_path(2026, 3) == "2026-03-planner.pdf"
        assert generate_default_output_path(2025, 12) == "2025-12-planner.pdf"
        assert generate_default_output_path(2024, 1) == "2024-01-planner.pdf"


class TestParseArgs:
    """Tests for argument parsing."""

    def test_valid_args(self):
        """Should parse valid arguments correctly."""
        args = parse_args(["--year", "2026", "--month", "3"])
        assert args.year == 2026
        assert args.month == 3
        assert args.output == "2026-03-planner.pdf"

    def test_custom_output_path(self):
        """Should use custom output path when provided."""
        args = parse_args(["--year", "2026", "--month", "3", "--output", "custom.pdf"])
        assert args.output == "custom.pdf"

    def test_missing_year(self):
        """Should exit with error when year is missing."""
        with pytest.raises(SystemExit):
            parse_args(["--month", "3"])

    def test_missing_month(self):
        """Should exit with error when month is missing."""
        with pytest.raises(SystemExit):
            parse_args(["--year", "2026"])

    def test_invalid_month(self):
        """Should exit with error for invalid month."""
        with pytest.raises(SystemExit):
            parse_args(["--year", "2026", "--month", "13"])

    def test_leap_year_february(self):
        """Should accept leap year February."""
        args = parse_args(["--year", "2024", "--month", "2"])
        assert args.year == 2024
        assert args.month == 2
