"""PDF generation and rendering logic."""

from reportlab.pdfgen import canvas

from .layout import (
    PAGE_WIDTH,
    PAGE_HEIGHT,
    MARGIN_TOP,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    TITLE_HEIGHT,
    TITLE_FONT,
    TITLE_FONT_SIZE,
    NAV_FONT,
    NAV_FONT_SIZE,
    NAV_BUTTON_WIDTH,
    NAV_BUTTON_HEIGHT,
    GRID_FONT,
    GRID_FONT_SIZE,
    GRID_HEADER_FONT,
    GRID_HEADER_FONT_SIZE,
    CELL_WIDTH,
    GRID_HEADER_HEIGHT,
    CHECKLIST_ITEMS_PER_PAGE,
    CHECKLIST_TOTAL_PAGES,
    CHECKBOX_SIZE,
    CHECKBOX_LINE_GAP,
    CHECKLIST_FONT,
    CHECKLIST_FONT_SIZE,
    WEEK_STRIP_CELL_HEIGHT,
    WEEK_STRIP_HIGHLIGHT_GRAY,
    WEEK_STRIP_DAY_FONT_SIZE,
    WEEK_STRIP_WEEKDAY_FONT_SIZE,
    WEEK_STRIP_WEEKDAY_TOP_PADDING,
    WEEK_STRIP_DAY_BOTTOM_PADDING,
    DAILY_SECTION_GAP,
    DAILY_SECTION_PADDING,
    DAILY_CHECKBOX_SIZE,
    DAILY_ROW_HEIGHT,
    DAILY_SECTION_TITLE_FONT,
    DAILY_SECTION_TITLE_FONT_SIZE,
    DAILY_LABEL_FONT,
    DAILY_LABEL_FONT_SIZE,
    DAILY_NOTE_LINE_SPACING,
    DAILY_TODO_LINES,
    DAILY_ROUTINES,
    NOTES_PAGES_PER_DAY,
)
from .model import month_metadata, date_metadata, week_days_for_date
from .navigation import (
    month_destination_id,
    day_destination_id,
    checklist_destination_id,
    notes_destination_id,
)


def draw_checklist_page(
    c: canvas.Canvas, page_number: int, total_pages: int, month_meta: dict
) -> None:
    """Draw a checklist page with empty checkboxes and writing lines.

    Args:
        c: ReportLab canvas
        page_number: Current checklist page (1-based)
        total_pages: Total number of checklist pages
        month_meta: Month metadata dictionary
    """
    year = month_meta["year"]
    month_name = month_meta["month_name"]

    # Combined title: "Todo – Month Year (page/total)"
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    checklist_title = f"Todo – {month_name} {year} ({page_number}/{total_pages})"
    checklist_title_width = c.stringWidth(checklist_title, TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(
        (PAGE_WIDTH - checklist_title_width) / 2,
        PAGE_HEIGHT - MARGIN_TOP - 25,
        checklist_title,
    )

    # Navigation bar (Month button on checklist pages for convenience)
    nav_y = PAGE_HEIGHT - MARGIN_TOP - TITLE_HEIGHT - NAV_BUTTON_HEIGHT - 20
    nav_center_x = PAGE_WIDTH / 2

    c.setFont(NAV_FONT, NAV_FONT_SIZE)

    month_x = nav_center_x - NAV_BUTTON_WIDTH / 2
    c.rect(month_x, nav_y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)
    month_text = "Month"
    month_text_width = c.stringWidth(month_text, NAV_FONT, NAV_FONT_SIZE)
    c.drawString(
        month_x + (NAV_BUTTON_WIDTH - month_text_width) / 2,
        nav_y + 12,
        month_text,
    )
    c.linkAbsolute(
        "",
        month_destination_id(),
        (month_x, nav_y, month_x + NAV_BUTTON_WIDTH, nav_y + NAV_BUTTON_HEIGHT),
    )

    # Checklist items
    body_start_y = nav_y - 30
    content_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    available_height = body_start_y - MARGIN_BOTTOM
    row_height = available_height / CHECKLIST_ITEMS_PER_PAGE

    c.setFont(CHECKLIST_FONT, CHECKLIST_FONT_SIZE)

    for i in range(CHECKLIST_ITEMS_PER_PAGE):
        item_y = body_start_y - (i + 1) * row_height

        # Draw checkbox (empty square)
        checkbox_x = MARGIN_LEFT
        checkbox_y = item_y + (row_height - CHECKBOX_SIZE) / 2
        c.rect(checkbox_x, checkbox_y, CHECKBOX_SIZE, CHECKBOX_SIZE)

        # Draw writing line next to checkbox
        line_x_start = checkbox_x + CHECKBOX_SIZE + CHECKBOX_LINE_GAP
        line_x_end = MARGIN_LEFT + content_width
        line_y = checkbox_y
        c.setLineWidth(0.5)
        c.line(line_x_start, line_y, line_x_end, line_y)
        c.setLineWidth(1)

    # Register bookmark only on the first checklist page
    if page_number == 1:
        c.bookmarkPage(checklist_destination_id())


def draw_month_page(c: canvas.Canvas, metadata: dict) -> None:
    """Draw the month overview page.

    Args:
        c: ReportLab canvas
        metadata: Month metadata dictionary
    """
    year = metadata["year"]
    month = metadata["month"]
    days = metadata["days"]
    first_day = metadata["first_weekday"]
    month_name = metadata["month_name"]

    # Title
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    title = f"{month_name} {year}"
    title_width = c.stringWidth(title, TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(
        (PAGE_WIDTH - title_width) / 2,
        PAGE_HEIGHT - MARGIN_TOP - 25,
        title,
    )

    # Weekday headers
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    c.setFont(GRID_HEADER_FONT, GRID_HEADER_FONT_SIZE)

    grid_start_y = PAGE_HEIGHT - MARGIN_TOP - TITLE_HEIGHT - 35

    for i, day_name in enumerate(weekdays):
        x = (
            MARGIN_LEFT
            + i * CELL_WIDTH
            + (
                CELL_WIDTH
                - c.stringWidth(day_name, GRID_HEADER_FONT, GRID_HEADER_FONT_SIZE)
            )
            / 2
        )
        c.drawString(x, grid_start_y, day_name)

    # Calculate grid position
    grid_start_y -= GRID_HEADER_HEIGHT + 20

    # Compute number of rows needed
    num_rows = ((first_day + days - 1) // 7) + 1

    # Make cell height fill the available vertical space exactly
    available_height = grid_start_y - MARGIN_BOTTOM
    cell_height = available_height / num_rows

    # Height of the tappable day-number area at the top of each cell
    DAY_LINK_HEIGHT = 40

    # Draw day cells
    c.setFont(GRID_FONT, GRID_FONT_SIZE)

    row = 0
    col = first_day
    day = 1

    while day <= days:
        x = MARGIN_LEFT + col * CELL_WIDTH
        y = grid_start_y - (row + 1) * cell_height

        # Draw cell border
        c.rect(x, y, CELL_WIDTH, cell_height)

        # Draw day number
        day_str = str(day)
        text_width = c.stringWidth(day_str, GRID_FONT, GRID_FONT_SIZE)
        c.drawString(
            x + (CELL_WIDTH - text_width) / 2,
            y + cell_height - 30,
            day_str,
        )

        # Create clickable link covering only the day-number area (top strip)
        dest_id = day_destination_id(year, month, day)
        link_top = y + cell_height
        link_bottom = link_top - DAY_LINK_HEIGHT
        c.linkAbsolute("", dest_id, (x, link_bottom, x + CELL_WIDTH, link_top))

        col += 1
        if col == 7:
            col = 0
            row += 1
        day += 1

    # Todo navigation button (top-right corner)
    c.setFont(NAV_FONT, NAV_FONT_SIZE)
    checklist_btn_x = PAGE_WIDTH - MARGIN_RIGHT - NAV_BUTTON_WIDTH
    checklist_btn_y = PAGE_HEIGHT - MARGIN_TOP - 35
    c.rect(checklist_btn_x, checklist_btn_y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)
    cl_text = "Todo"
    cl_text_width = c.stringWidth(cl_text, NAV_FONT, NAV_FONT_SIZE)
    c.drawString(
        checklist_btn_x + (NAV_BUTTON_WIDTH - cl_text_width) / 2,
        checklist_btn_y + 12,
        cl_text,
    )
    c.linkAbsolute(
        "",
        checklist_destination_id(),
        (
            checklist_btn_x,
            checklist_btn_y,
            checklist_btn_x + NAV_BUTTON_WIDTH,
            checklist_btn_y + NAV_BUTTON_HEIGHT,
        ),
    )

    # Register bookmark for month page
    c.bookmarkPage(month_destination_id())


def _draw_nav_strip(
    c: canvas.Canvas,
    year: int,
    month: int,
    current_day: int,
    week_days: list[int | None],
    y: float,
) -> None:
    """Draw a unified navigation strip: Month + 7 day cells + Checklist.

    All 9 cells share the same height and visual style. The strip spans the
    full content width. Day cells show weekday abbreviation and day number;
    the current day is highlighted. Month and Checklist cells act as
    navigation buttons.

    Args:
        c: ReportLab canvas
        year: Current year
        month: Current month
        current_day: The current day (highlighted)
        week_days: 7-element list from week_days_for_date()
        y: Bottom y-coordinate of the strip
    """
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    content_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    # 9 cells: Month + 7 days + Checklist
    cell_width = content_width / 9

    for col in range(9):
        cell_x = MARGIN_LEFT + col * cell_width
        cell_y = y

        if col == 0:
            # --- Month button cell ---
            c.rect(cell_x, cell_y, cell_width, WEEK_STRIP_CELL_HEIGHT)
            c.setFont(TITLE_FONT, NAV_FONT_SIZE)
            label = "Month"
            lw = c.stringWidth(label, TITLE_FONT, NAV_FONT_SIZE)
            c.drawString(
                cell_x + (cell_width - lw) / 2,
                cell_y + WEEK_STRIP_CELL_HEIGHT / 2 - 6,
                label,
            )
            c.linkAbsolute(
                "",
                month_destination_id(),
                (cell_x, cell_y, cell_x + cell_width, cell_y + WEEK_STRIP_CELL_HEIGHT),
            )

        elif col == 8:
            # --- Todo button cell ---
            c.rect(cell_x, cell_y, cell_width, WEEK_STRIP_CELL_HEIGHT)
            c.setFont(TITLE_FONT, NAV_FONT_SIZE)
            label = "Todo"
            lw = c.stringWidth(label, TITLE_FONT, NAV_FONT_SIZE)
            c.drawString(
                cell_x + (cell_width - lw) / 2,
                cell_y + WEEK_STRIP_CELL_HEIGHT / 2 - 6,
                label,
            )
            c.linkAbsolute(
                "",
                checklist_destination_id(),
                (cell_x, cell_y, cell_x + cell_width, cell_y + WEEK_STRIP_CELL_HEIGHT),
            )

        else:
            # --- Day cell (index 1-7 → weekday 0-6) ---
            day_idx = col - 1
            day_num = week_days[day_idx]

            # Highlight current day
            if day_num is not None and day_num == current_day:
                c.setFillColorRGB(
                    WEEK_STRIP_HIGHLIGHT_GRAY,
                    WEEK_STRIP_HIGHLIGHT_GRAY,
                    WEEK_STRIP_HIGHLIGHT_GRAY,
                )
                c.rect(cell_x, cell_y, cell_width, WEEK_STRIP_CELL_HEIGHT, fill=1)
                c.setFillColorRGB(0, 0, 0)

            # Cell border
            c.rect(cell_x, cell_y, cell_width, WEEK_STRIP_CELL_HEIGHT)

            # Weekday abbreviation at top
            c.setFont(GRID_HEADER_FONT, WEEK_STRIP_WEEKDAY_FONT_SIZE)
            wd_text = weekdays[day_idx]
            wd_width = c.stringWidth(
                wd_text, GRID_HEADER_FONT, WEEK_STRIP_WEEKDAY_FONT_SIZE
            )
            c.drawString(
                cell_x + (cell_width - wd_width) / 2,
                cell_y + WEEK_STRIP_WEEKDAY_TOP_PADDING,
                wd_text,
            )

            if day_num is None:
                continue

            # Day number
            c.setFont(TITLE_FONT, WEEK_STRIP_DAY_FONT_SIZE)
            day_str = str(day_num)
            text_width = c.stringWidth(day_str, TITLE_FONT, WEEK_STRIP_DAY_FONT_SIZE)
            c.drawString(
                cell_x + (cell_width - text_width) / 2,
                cell_y + WEEK_STRIP_CELL_HEIGHT - WEEK_STRIP_DAY_BOTTOM_PADDING,
                day_str,
            )

            # Clickable link for non-current days
            if day_num != current_day:
                dest_id = day_destination_id(year, month, day_num)
                c.linkAbsolute(
                    "",
                    dest_id,
                    (
                        cell_x,
                        cell_y,
                        cell_x + cell_width,
                        cell_y + WEEK_STRIP_CELL_HEIGHT,
                    ),
                )


def draw_daily_page(
    c: canvas.Canvas, metadata: dict, week_days: list[int | None]
) -> None:
    """Draw a daily page.

    Args:
        c: ReportLab canvas
        metadata: Date metadata dictionary
        week_days: 7-element list from week_days_for_date()
    """
    full_date = metadata["full_date"]
    year = metadata["year"]
    month = metadata["month"]
    day = metadata["day"]

    # Title (centered)
    title_y = PAGE_HEIGHT - MARGIN_TOP - 25
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    title_width = c.stringWidth(full_date, TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(
        (PAGE_WIDTH - title_width) / 2,
        title_y,
        full_date,
    )

    # Unified navigation strip below title
    strip_y = title_y - TITLE_HEIGHT - 30
    _draw_nav_strip(c, year, month, day, week_days, strip_y)

    # Body area starts below the nav strip
    body_top_y = strip_y - DAILY_SECTION_GAP
    section_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

    # --- Section 1: Daily Routines (horizontal, one row) ---
    # All 4 routines are laid out side-by-side in a single row.
    routines_row_height = DAILY_CHECKBOX_SIZE + DAILY_SECTION_PADDING * 2
    routines_box_height = (
        DAILY_SECTION_PADDING
        + DAILY_SECTION_TITLE_FONT_SIZE
        + DAILY_SECTION_PADDING
        + routines_row_height
        + DAILY_SECTION_PADDING
    )
    routines_box_y = body_top_y - routines_box_height

    # Box border
    c.rect(MARGIN_LEFT, routines_box_y, section_width, routines_box_height)

    # Section title
    c.setFont(DAILY_SECTION_TITLE_FONT, DAILY_SECTION_TITLE_FONT_SIZE)
    c.drawString(
        MARGIN_LEFT + DAILY_SECTION_PADDING,
        routines_box_y
        + routines_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        + 4,
        "Daily Routines",
    )

    # Routine checkboxes in one horizontal row, evenly spaced
    routines_content_top = (
        routines_box_y
        + routines_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        - DAILY_SECTION_PADDING
    )
    cb_y = (
        routines_content_top
        - routines_row_height
        + (routines_row_height - DAILY_CHECKBOX_SIZE) / 2
    )
    num_routines = len(DAILY_ROUTINES)
    col_width = section_width / num_routines
    c.setFont(DAILY_LABEL_FONT, DAILY_LABEL_FONT_SIZE)
    for idx, label in enumerate(DAILY_ROUTINES):
        col_x = MARGIN_LEFT + idx * col_width
        cb_x = col_x + DAILY_SECTION_PADDING
        c.rect(cb_x, cb_y, DAILY_CHECKBOX_SIZE, DAILY_CHECKBOX_SIZE)
        c.drawString(
            cb_x + DAILY_CHECKBOX_SIZE + 10,
            cb_y + (DAILY_CHECKBOX_SIZE - DAILY_LABEL_FONT_SIZE) / 2 + 2,
            label,
        )

    # --- Section 2: Todo ---
    todo_inner_height = DAILY_TODO_LINES * DAILY_ROW_HEIGHT
    todo_box_height = (
        DAILY_SECTION_PADDING
        + DAILY_SECTION_TITLE_FONT_SIZE
        + DAILY_SECTION_PADDING
        + todo_inner_height
        + DAILY_SECTION_PADDING
    )
    todo_box_y = routines_box_y - DAILY_SECTION_GAP - todo_box_height

    # Box border
    c.rect(MARGIN_LEFT, todo_box_y, section_width, todo_box_height)

    # Section title
    c.setFont(DAILY_SECTION_TITLE_FONT, DAILY_SECTION_TITLE_FONT_SIZE)
    c.drawString(
        MARGIN_LEFT + DAILY_SECTION_PADDING,
        todo_box_y
        + todo_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        + 4,
        "Todo",
    )

    # Todo checkbox rows with writing lines
    todo_content_top = (
        todo_box_y
        + todo_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        - DAILY_SECTION_PADDING
    )
    for idx in range(DAILY_TODO_LINES):
        row_y = todo_content_top - (idx + 1) * DAILY_ROW_HEIGHT
        cb_x = MARGIN_LEFT + DAILY_SECTION_PADDING
        cb_y = row_y + (DAILY_ROW_HEIGHT - DAILY_CHECKBOX_SIZE) / 2
        c.rect(cb_x, cb_y, DAILY_CHECKBOX_SIZE, DAILY_CHECKBOX_SIZE)
        line_x_start = cb_x + DAILY_CHECKBOX_SIZE + 12
        line_x_end = MARGIN_LEFT + section_width - DAILY_SECTION_PADDING
        line_y = cb_y  # align line with bottom edge of checkbox
        c.setLineWidth(0.5)
        c.line(line_x_start, line_y, line_x_end, line_y)
        c.setLineWidth(1)

    # --- Section 3: Notes Index (fills remaining space) ---
    # 10 numbered rows, each linking to the corresponding note page.
    notes_box_y = MARGIN_BOTTOM
    notes_box_height = todo_box_y - DAILY_SECTION_GAP - notes_box_y

    # Box border
    c.rect(MARGIN_LEFT, notes_box_y, section_width, notes_box_height)

    # Section title
    c.setFont(DAILY_SECTION_TITLE_FONT, DAILY_SECTION_TITLE_FONT_SIZE)
    c.drawString(
        MARGIN_LEFT + DAILY_SECTION_PADDING,
        notes_box_y
        + notes_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        + 4,
        "Notes",
    )

    # Index rows: distribute 10 rows evenly in the content area below the title
    index_content_top = (
        notes_box_y
        + notes_box_height
        - DAILY_SECTION_PADDING
        - DAILY_SECTION_TITLE_FONT_SIZE
        - DAILY_SECTION_PADDING
    )
    index_content_height = index_content_top - notes_box_y - DAILY_SECTION_PADDING
    index_row_height = index_content_height / NOTES_PAGES_PER_DAY

    # Width of the page-number label column (e.g. "10.")
    c.setFont(DAILY_LABEL_FONT, DAILY_LABEL_FONT_SIZE)
    label_col_width = c.stringWidth("10. ", DAILY_LABEL_FONT, DAILY_LABEL_FONT_SIZE) + 8

    # Small "→" nav button at the right end of each row
    c.setFont(NAV_FONT, NAV_FONT_SIZE)
    arrow_btn_w = c.stringWidth("\u2192", NAV_FONT, NAV_FONT_SIZE) + 20
    arrow_btn_h = DAILY_LABEL_FONT_SIZE + 8

    line_x_start = MARGIN_LEFT + DAILY_SECTION_PADDING + label_col_width
    # Writing line ends just before the arrow button
    row_right_edge = MARGIN_LEFT + section_width - DAILY_SECTION_PADDING
    line_x_end = row_right_edge - arrow_btn_w - 8

    for idx in range(NOTES_PAGES_PER_DAY):
        note_page_num = idx + 1
        row_top = index_content_top - idx * index_row_height
        row_bottom = row_top - index_row_height
        # Vertical centre of the row for text baseline
        row_mid_y = row_bottom + (index_row_height - DAILY_LABEL_FONT_SIZE) / 2

        # Page-number label (e.g. "1.", "10.")
        c.setFont(DAILY_LABEL_FONT, DAILY_LABEL_FONT_SIZE)
        label = f"{note_page_num}."
        c.drawString(
            MARGIN_LEFT + DAILY_SECTION_PADDING,
            row_mid_y,
            label,
        )

        # Writing line for the topic title
        c.setLineWidth(0.5)
        c.line(line_x_start, row_mid_y, line_x_end, row_mid_y)
        c.setLineWidth(1)

        # "→" button at the right end of the row
        btn_x = row_right_edge - arrow_btn_w
        btn_y = row_bottom + (index_row_height - arrow_btn_h) / 2
        c.rect(btn_x, btn_y, arrow_btn_w, arrow_btn_h)
        c.setFont(NAV_FONT, NAV_FONT_SIZE)
        arrow_label = "\u2192"
        arrow_label_w = c.stringWidth(arrow_label, NAV_FONT, NAV_FONT_SIZE)
        c.drawString(
            btn_x + (arrow_btn_w - arrow_label_w) / 2,
            btn_y + (arrow_btn_h - NAV_FONT_SIZE) / 2,
            arrow_label,
        )
        c.linkAbsolute(
            "",
            notes_destination_id(year, month, day, note_page_num),
            (btn_x, btn_y, btn_x + arrow_btn_w, btn_y + arrow_btn_h),
        )

    # Register bookmark for daily page
    dest_id = day_destination_id(year, month, day)
    c.bookmarkPage(dest_id)


def draw_notes_page(
    c: canvas.Canvas,
    page_number: int,
    total_pages: int,
    date_meta: dict,
) -> None:
    """Draw a ruled note page belonging to a specific daily page.

    Args:
        c: ReportLab canvas
        page_number: Current note page number (1-based)
        total_pages: Total note pages per day
        date_meta: Date metadata dictionary for the parent daily page
    """
    year = date_meta["year"]
    month = date_meta["month"]
    day = date_meta["day"]
    full_date = date_meta["full_date"]

    # Title: "Notes – <full date> (page/total)"
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    title = f"Notes \u2013 {full_date} ({page_number}/{total_pages})"
    title_width = c.stringWidth(title, TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(
        (PAGE_WIDTH - title_width) / 2,
        PAGE_HEIGHT - MARGIN_TOP - 25,
        title,
    )

    # Navigation bar: "Day" button (left) and "Month" button (right)
    nav_y = PAGE_HEIGHT - MARGIN_TOP - TITLE_HEIGHT - NAV_BUTTON_HEIGHT - 20
    nav_center_x = PAGE_WIDTH / 2

    c.setFont(NAV_FONT, NAV_FONT_SIZE)

    # Day button (links back to parent daily page)
    day_btn_x = nav_center_x - NAV_BUTTON_WIDTH - 20
    c.rect(day_btn_x, nav_y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)
    day_text = "Day"
    day_text_width = c.stringWidth(day_text, NAV_FONT, NAV_FONT_SIZE)
    c.drawString(
        day_btn_x + (NAV_BUTTON_WIDTH - day_text_width) / 2,
        nav_y + 12,
        day_text,
    )
    c.linkAbsolute(
        "",
        day_destination_id(year, month, day),
        (day_btn_x, nav_y, day_btn_x + NAV_BUTTON_WIDTH, nav_y + NAV_BUTTON_HEIGHT),
    )

    # Month button
    month_btn_x = nav_center_x + 20
    c.rect(month_btn_x, nav_y, NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)
    month_text = "Month"
    month_text_width = c.stringWidth(month_text, NAV_FONT, NAV_FONT_SIZE)
    c.drawString(
        month_btn_x + (NAV_BUTTON_WIDTH - month_text_width) / 2,
        nav_y + 12,
        month_text,
    )
    c.linkAbsolute(
        "",
        month_destination_id(),
        (month_btn_x, nav_y, month_btn_x + NAV_BUTTON_WIDTH, nav_y + NAV_BUTTON_HEIGHT),
    )

    # Ruled lines filling the body area
    body_top_y = nav_y - 30
    line_x_start = MARGIN_LEFT
    line_x_end = PAGE_WIDTH - MARGIN_RIGHT
    current_line_y = body_top_y
    c.setLineWidth(0.5)
    while current_line_y - DAILY_NOTE_LINE_SPACING >= MARGIN_BOTTOM:
        current_line_y -= DAILY_NOTE_LINE_SPACING
        c.line(line_x_start, current_line_y, line_x_end, current_line_y)
    c.setLineWidth(1)

    # Register bookmark for every note page so index links resolve correctly
    c.bookmarkPage(notes_destination_id(year, month, day, page_number))


def generate_pdf(year: int, month: int, output_path: str) -> None:
    """Generate the planner PDF for a given month/year.

    Args:
        year: The year
        month: The month (1-12)
        output_path: Output file path
    """
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    month_meta = month_metadata(year, month)
    total_days = month_meta["days"]

    # Draw checklist pages (at the very beginning of the document)
    for page_num in range(1, CHECKLIST_TOTAL_PAGES + 1):
        if page_num > 1:
            c.showPage()
        draw_checklist_page(c, page_num, CHECKLIST_TOTAL_PAGES, month_meta)

    # Draw month overview page
    c.showPage()
    draw_month_page(c, month_meta)

    # Draw daily pages
    for day in range(1, total_days + 1):
        c.showPage()

        day_meta = date_metadata(year, month, day)
        week_days = week_days_for_date(year, month, day)

        draw_daily_page(c, day_meta, week_days)

    # Draw note pages (10 per day, grouped by day, appended after all daily pages)
    for day in range(1, total_days + 1):
        day_meta = date_metadata(year, month, day)
        for note_page in range(1, NOTES_PAGES_PER_DAY + 1):
            c.showPage()
            draw_notes_page(c, note_page, NOTES_PAGES_PER_DAY, day_meta)

    c.save()
