"""Navigation helpers for PDF bookmarks and links."""


def checklist_destination_id() -> str:
    """Return the destination ID for the first checklist page.

    Returns:
        Destination ID string
    """
    return "checklist"


def month_destination_id() -> str:
    """Return the destination ID for the month overview page.

    Returns:
        Destination ID string
    """
    return "month"


def day_destination_id(year: int, month: int, day: int) -> str:
    """Return the destination ID for a daily page.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)
        day: The day (1-31)

    Returns:
        Destination ID string in format day_YYYY_MM_DD
    """
    return f"day_{year:04d}_{month:02d}_{day:02d}"


def notes_destination_id(year: int, month: int, day: int, page: int) -> str:
    """Return the destination ID for a note page belonging to a daily page.

    Args:
        year: The year (e.g., 2026)
        month: The month (1-12)
        day: The day (1-31)
        page: The note page number (1-based)

    Returns:
        Destination ID string in format notes_YYYY_MM_DD_PP
    """
    return f"notes_{year:04d}_{month:02d}_{day:02d}_{page:02d}"
