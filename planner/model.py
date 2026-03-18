"""Calendar and date model logic."""

import calendar
from datetime import date, timedelta


def days_in_month(year: int, month: int) -> int:
    """Return the number of days in the given month/year.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)

    Returns:
        Number of days in the month (28-31)
    """
    return calendar.monthrange(year, month)[1]


def first_weekday(year: int, month: int) -> int:
    """Return the weekday of the first day of the month.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)

    Returns:
        Weekday as integer (0=Monday, 6=Sunday)
    """
    return date(year, month, 1).weekday()


def week_days_for_date(year: int, month: int, day: int) -> list[int | None]:
    """Return the 7 days (Mon-Sun) of the week containing the given date.

    Days outside the given month are returned as None.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)
        day: The day (1-31)

    Returns:
        List of 7 elements representing Mon-Sun, where each element is
        the day number (int) if it falls within the given month, or None otherwise.
    """
    d = date(year, month, day)
    monday = d - timedelta(days=d.weekday())  # weekday() returns 0=Mon
    result: list[int | None] = []
    for i in range(7):
        current = monday + timedelta(days=i)
        if current.month == month and current.year == year:
            result.append(current.day)
        else:
            result.append(None)
    return result


def month_metadata(year: int, month: int) -> dict:
    """Generate metadata for a given month/year.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)

    Returns:
        Dictionary containing month metadata
    """
    days = days_in_month(year, month)
    first_day = first_weekday(year, month)

    return {
        "year": year,
        "month": month,
        "days": days,
        "first_weekday": first_day,
        "month_name": calendar.month_name[month],
    }


def date_metadata(year: int, month: int, day: int) -> dict:
    """Generate metadata for a specific date.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)
        day: The day (1-31)

    Returns:
        Dictionary containing date metadata
    """
    d = date(year, month, day)

    return {
        "year": year,
        "month": month,
        "day": day,
        "weekday": d.weekday(),
        "weekday_name": d.strftime("%A"),
        "full_date": d.strftime("%A, %B %d, %Y"),
    }
