"""Page layout constants for Kindle Scribe PDF generation."""

# Page dimensions (Kindle Scribe portrait ratio)
PAGE_WIDTH = 1404
PAGE_HEIGHT = 1872

# Margins
MARGIN_TOP = 120
MARGIN_BOTTOM = 50
MARGIN_LEFT = 50
MARGIN_RIGHT = 50

# Title area
TITLE_HEIGHT = 70
TITLE_FONT = "Helvetica-Bold"
TITLE_FONT_SIZE = 32

# Navigation bar
NAV_HEIGHT = 50
NAV_FONT = "Helvetica"
NAV_FONT_SIZE = 16
NAV_BUTTON_WIDTH = 120
NAV_BUTTON_HEIGHT = 40

# Section boxes (used by checklist pages)
SECTION_FONT = "Helvetica-Bold"
SECTION_FONT_SIZE = 18
SECTION_BOX_HEIGHT = 400
SECTION_BOX_PADDING = 20
SECTION_BORDER_WIDTH = 1

# Daily page body sections
DAILY_SECTION_GAP = 20
DAILY_SECTION_PADDING = 16
DAILY_CHECKBOX_SIZE = 48  # 30 * 1.6
DAILY_ROW_HEIGHT = 70  # 44 * 1.6 ≈ 70
DAILY_SECTION_TITLE_FONT = "Helvetica-Bold"
DAILY_SECTION_TITLE_FONT_SIZE = 25  # 22 * 1.15 ≈ 25
DAILY_LABEL_FONT = "Helvetica"
DAILY_LABEL_FONT_SIZE = 23  # 20 * 1.15 ≈ 23
DAILY_NOTE_LINE_SPACING = 70  # 44 * 1.6 ≈ 70
DAILY_TODO_LINES = 7
DAILY_ROUTINES: list[str] = [
    "Check Calendar",
    "Check Email",
    "Book Times",
    "Take a Break",
]

# Month grid
GRID_FONT = "Helvetica"
GRID_FONT_SIZE = 36  # 18 * 2 = 36
GRID_HEADER_FONT = "Helvetica-Bold"
GRID_HEADER_FONT_SIZE = 32  # 16 * 2 = 32
CELL_WIDTH = 180
CELL_HEIGHT = 200
GRID_HEADER_HEIGHT = 40

# Checklist
CHECKLIST_ITEMS_PER_PAGE = 15
CHECKLIST_TOTAL_PAGES = 3
CHECKBOX_SIZE = 45  # 28 * 1.6
CHECKBOX_LINE_GAP = 20
CHECKLIST_FONT = "Helvetica"
CHECKLIST_FONT_SIZE = 16

# Note pages (extra ruled pages appended after all daily pages)
NOTES_PAGES_PER_DAY = 10

# Colors
BLACK = (0, 0, 0)
GRAY = (0.5, 0.5, 0.5)
LIGHT_GRAY = (0.9, 0.9, 0.9)

# Week overview strip on daily pages
# Cell width is computed dynamically to fill the content area:
#   (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / 7
WEEK_STRIP_CELL_HEIGHT = 80
WEEK_STRIP_HEADER_HEIGHT = 25
WEEK_STRIP_HIGHLIGHT_GRAY = 0.82
WEEK_STRIP_DAY_FONT_SIZE = 33  # 22 * 1.5 ≈ 33
WEEK_STRIP_WEEKDAY_FONT_SIZE = 24  # 12 * 2 = 24
# Padding within strip cells
WEEK_STRIP_WEEKDAY_TOP_PADDING = 38  # Space from top for weekday name (increased for better spacing)
WEEK_STRIP_DAY_BOTTOM_PADDING = 30  # Space from bottom for day number (increased for better spacing)
