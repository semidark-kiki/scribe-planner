"""Tests for the model module."""

from planner.model import (
    days_in_month,
    first_weekday,
    month_metadata,
    date_metadata,
    week_days_for_date,
)


class TestDaysInMonth:
    """Tests for days_in_month function."""

    def test_january_31_days(self):
        """January should have 31 days."""
        assert days_in_month(2026, 1) == 31

    def test_february_non_leap_28_days(self):
        """February in non-leap year should have 28 days."""
        assert days_in_month(2025, 2) == 28

    def test_february_leap_29_days(self):
        """February in leap year should have 29 days."""
        assert days_in_month(2024, 2) == 29

    def test_april_30_days(self):
        """April should have 30 days."""
        assert days_in_month(2026, 4) == 30

    def test_may_31_days(self):
        """May should have 31 days."""
        assert days_in_month(2026, 5) == 31

    def test_february_leap_year_2000(self):
        """Year 2000 is a leap year."""
        assert days_in_month(2000, 2) == 29

    def test_february_not_leap_1900(self):
        """Year 1900 is not a leap year."""
        assert days_in_month(1900, 2) == 28


class TestFirstWeekday:
    """Tests for first_weekday function."""

    def test_march_2026_starts_sunday(self):
        """March 2026 starts on Sunday (6)."""
        assert first_weekday(2026, 3) == 6

    def test_january_2026_starts_thursday(self):
        """January 2026 starts on Thursday (3)."""
        assert first_weekday(2026, 1) == 3

    def test_february_2025_starts_saturday(self):
        """February 2025 starts on Saturday (5)."""
        assert first_weekday(2025, 2) == 5


class TestMonthMetadata:
    """Tests for month_metadata function."""

    def test_march_2026_metadata(self):
        """March 2026 metadata should be correct."""
        meta = month_metadata(2026, 3)
        assert meta["year"] == 2026
        assert meta["month"] == 3
        assert meta["days"] == 31
        assert meta["month_name"] == "March"

    def test_february_leap_metadata(self):
        """February leap year metadata should have 29 days."""
        meta = month_metadata(2024, 2)
        assert meta["days"] == 29
        assert meta["month_name"] == "February"


class TestDateMetadata:
    """Tests for date_metadata function."""

    def test_full_date_format(self):
        """Full date should be formatted correctly."""
        meta = date_metadata(2026, 3, 16)
        assert meta["full_date"] == "Monday, March 16, 2026"

    def test_weekday_name(self):
        """Weekday name should be correct."""
        meta = date_metadata(2026, 3, 1)
        assert meta["weekday_name"] == "Sunday"

    def test_date_components(self):
        """Date components should be correct."""
        meta = date_metadata(2026, 3, 15)
        assert meta["year"] == 2026
        assert meta["month"] == 3
        assert meta["day"] == 15


class TestWeekDaysForDate:
    """Tests for week_days_for_date function."""

    def test_mid_month_all_in_month(self):
        """March 17, 2026 is a Tuesday; week is Mar 16-22 (all in month)."""
        result = week_days_for_date(2026, 3, 17)
        assert result == [16, 17, 18, 19, 20, 21, 22]

    def test_first_day_of_month_with_prev_month_days(self):
        """March 1, 2026 is a Sunday; week is Feb 23 - Mar 1 (only Sun in month)."""
        result = week_days_for_date(2026, 3, 1)
        assert result == [None, None, None, None, None, None, 1]

    def test_last_day_of_month_with_next_month_days(self):
        """March 31, 2026 is a Tuesday; week is Mar 30 - Apr 5 (Mon-Tue in month)."""
        result = week_days_for_date(2026, 3, 31)
        assert result == [30, 31, None, None, None, None, None]

    def test_month_starting_on_monday(self):
        """January 2026 starts on Thursday; test a week fully in month."""
        result = week_days_for_date(2026, 1, 12)  # Jan 12, 2026 is Monday
        assert result == [12, 13, 14, 15, 16, 17, 18]

    def test_february_leap_year_week_spanning(self):
        """Feb 29, 2024 is a Thursday; week is Feb 26 - Mar 3."""
        result = week_days_for_date(2024, 2, 29)
        assert result == [26, 27, 28, 29, None, None, None]

    def test_week_containing_month_start_sunday(self):
        """March 1, 2026 is Sunday; verify all None except last position."""
        result = week_days_for_date(2026, 3, 1)
        assert len(result) == 7
        assert result[6] == 1
        assert all(d is None for d in result[:6])

    def test_week_containing_month_end_wednesday(self):
        """April 30, 2026 is Wednesday; week is Apr 27 - May 3."""
        result = week_days_for_date(2026, 4, 30)
        assert result == [27, 28, 29, 30, None, None, None]
