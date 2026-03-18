## Project: Kindle Scribe Monthly Planner PDF Generator (PoC) - Implementation Plan

This document outlines the implementation plan for the PoC described in `POC-PRD.md`.

---

## 1. Objective

Build a Python proof of concept that generates a **hyperlinked monthly planner PDF** optimized for **Kindle Scribe**.

The PoC must:
- generate the planner fully in code
- create a single PDF for a given month/year
- include one **month overview page**
- include one **daily page for every day in the month**
- ensure **all daily pages have the same layout**
- support **internal PDF hyperlinks** for navigation

---

## 2. Project Structure

```
scribe-planner/
  main.py
  requirements.txt
  README.md
  AGENTS.md
  planner/
    __init__.py
    cli.py
    model.py
    layout.py
    navigation.py
    generator.py
  tests/
    __init__.py
    test_model.py
    test_cli.py
    test_generator.py
  docs/
    plan/
      POC-PRD.md
      POC-IMPLEMENTATION-PLAN.md
```

**Module responsibilities:**
- `main.py`: executable entry point
- `planner/cli.py`: argument parsing and validation
- `planner/model.py`: calendar/date logic (days in month, first weekday, date metadata)
- `planner/layout.py`: constants and page layout values (page size, margins, fonts)
- `planner/navigation.py`: bookmark naming + link target helpers
- `planner/generator.py`: PDF generation and navigation links

---

## 3. Implementation Phases

### Phase 1: Scaffold + CLI Contract

**Goals:**
- Set up project structure and dependencies
- Implement CLI argument parsing
- Validate inputs
- Define output file naming

**Tasks:**
1. Create `requirements.txt` with `reportlab`
2. Create `planner/__init__.py`
3. Implement `planner/cli.py`:
   - Parse `--year` (required, int)
   - Parse `--month` (required, int, 1-12)
   - Parse `--output` (optional, defaults to `YYYY-MM-planner.pdf`)
   - Validate inputs with clear error messages
4. Create `main.py` entry point
5. Write basic tests:
   - `tests/test_cli.py`: missing args, invalid month, default output naming

**Acceptance:**
- `python main.py --year 2026 --month 13` fails with validation error
- `python main.py --year 2026 --month 3` creates `2026-03-planner.pdf` (even if empty/minimal PDF)

---

### Phase 2: Domain Model

**Goals:**
- Compute month metadata needed for rendering
- Build calendar grid representation
- Generate deterministic bookmark IDs

**Tasks:**
1. Implement `planner/model.py`:
   - `days_in_month(year, month) -> int`
   - `first_weekday(year, month) -> int` (0=Monday or 6=Sunday based on library convention)
   - `month_metadata(year, month) -> dict` with days, first_weekday, year, month
   - `date_metadata(year, month, day) -> dict` with full date, weekday name, etc.
2. Implement `planner/navigation.py`:
   - `month_destination_id() -> str` returns `"month"`
   - `day_destination_id(year, month, day) -> str` returns `"day_YYYY_MM_DD"`
3. Write tests:
   - `tests/test_model.py`: leap year, 28/29/30/31 day months, first weekday calculations

**Acceptance:**
- Feb 2024 (leap) returns 29 days
- Feb 2025 (non-leap) returns 28 days
- April 2026 returns 30 days
- January 2026 returns 31 days

---

### Phase 3: Layout Constants

**Goals:**
- Define Kindle Scribe-suitable page dimensions
- Establish consistent margins and section positions
- Ensure daily page uniformity

**Tasks:**
1. Implement `planner/layout.py`:
   - Page size: `PAGE_WIDTH = 1404`, `PAGE_HEIGHT = 1872`
   - Margins: top, bottom, left, right
   - Title area height
   - Navigation row height and positions
   - Section boxes (Tasks, Meetings, Notes) dimensions and positions
   - Font sizes and styles
   - Month grid: cell size, rows, columns, header height
2. Keep all values in one place for future config-driven layout

**Acceptance:**
- Layout constants are centralized
- Portrait ratio is maintained (~0.75 aspect)

---

### Phase 4: PDF Rendering

**Goals:**
- Draw month overview page
- Draw daily page template
- Render pages in correct order

**Tasks:**
1. Implement `planner/generator.py`:
   - `generate_pdf(year, month, output_path) -> None`
   - `draw_month_page(canvas, metadata) -> None`
   - `draw_daily_page(canvas, metadata) -> None`
2. Month page:
   - Centered month/year title
   - Weekday headers
   - Calendar grid with day numbers
   - Blank cells for non-month days
3. Daily page:
   - Full date title (e.g., "Monday, March 16, 2026")
   - Navigation labels: Prev, Month, Next
   - Three sections: Tasks, Meetings, Notes (outlined regions)
4. Page order:
   - Page 1: month overview
   - Page 2: day 1
   - Page 3: day 2
   - ...
   - Page N+1: last day

**Acceptance:**
- PDF opens in standard reader
- Page count = 1 + number_of_days
- All daily pages visually identical in structure

---

### Phase 5: Navigation Wiring

**Goals:**
- Register named destinations (bookmarks)
- Add clickable link rectangles
- Handle edge cases for first/last day

**Tasks:**
1. In `planner/generator.py`:
   - Register month bookmark on page 1
   - Register day bookmark on each daily page using `day_destination_id`
   - Add link rectangles on month page day cells targeting day destinations
   - Add link rectangles on daily page navigation:
     - `Month` always links to page 1
     - `Prev` links to previous day page (or omit/disable for first day)
     - `Next` links to next day page (or omit/disable for last day)
2. Use `reportlab` PDF link annotation API

**Acceptance:**
- Clicking day N on month page navigates to day N page
- Clicking `Month` on any daily page returns to month overview
- First day has no broken `Prev` link
- Last day has no broken `Next` link

---

### Phase 6: Tests

**Goals:**
- Verify correctness across edge cases
- Ensure navigation behavior is testable where possible

**Tasks:**
1. `tests/test_model.py`:
   - `test_days_in_month_february_non_leap`
   - `test_days_in_month_february_leap`
   - `test_days_in_month_april_30_days`
   - `test_days_in_month_january_31_days`
   - `test_first_weekday_varies`
2. `tests/test_cli.py`:
   - `test_missing_year_fails`
   - `test_missing_month_fails`
   - `test_invalid_month_fails`
   - `test_default_output_naming`
3. `tests/test_generator.py`:
   - `test_creates_expected_page_count_march_2026` (32 pages)
   - `test_creates_expected_page_count_february_2025` (29 pages)
   - `test_creates_expected_page_count_february_2024` (30 pages)
   - `test_creates_expected_page_count_april_2026` (31 pages)
   - `test_first_day_has_no_prev_link` (where testable)
   - `test_last_day_has_no_next_link` (where testable)

**Acceptance:**
- `pytest -x -vv` passes
- All edge cases covered

---

### Phase 7: Documentation + Polish

**Goals:**
- Provide setup and usage instructions
- Clean up code for maintainability

**Tasks:**
1. Write `README.md`:
   - Project overview
   - Setup instructions
   - Usage examples
   - Output description
2. Add docstrings to modules
3. Ensure error messages are user-friendly
4. Verify PDF output quality on sample months

**Acceptance:**
- User can set up and run tool following README
- Output PDF is legible and navigation works

---

## 4. Test Commands (Reference)

**Run all tests:**
```bash
pytest -x -vv
```

**Run a single test file:**
```bash
pytest tests/test_generator.py
```

**Run a single test function:**
```bash
pytest tests/test_generator.py::test_creates_expected_page_count_march_2026
```

**Run tests by keyword:**
```bash
pytest -k "leap and february"
```

**Smoke test generation:**
```bash
python main.py --year 2026 --month 3
```

---

## 5. Acceptance Checklist

- [ ] CLI with `--year`, `--month`, `--output`
- [ ] Input validation (invalid month rejected)
- [ ] Default output filename `YYYY-MM-planner.pdf`
- [ ] Month overview page with clickable day cells
- [ ] Daily pages with uniform layout
- [ ] Daily pages include: full date, Prev/Month/Next, Tasks/Meetings/Notes
- [ ] Page order: month first, then day 1..N
- [ ] Internal links: month→days, days→month, prev/next where applicable
- [ ] No broken links on first/last day
- [ ] Works for 28/29/30/31 day months
- [ ] PDF opens in standard readers
- [ ] Tests pass
- [ ] README with setup and usage

---

## 6. Future-Proofing Notes

Design decisions should support later additions:
- Keep layout constants in one place for config migration
- Keep rendering logic separate from link logic
- Avoid hard-coded positions where possible
- Preserve extensibility for template-based rendering

---

## 7. Out of Scope (PoC)

- Custom PDF templates
- Weekly pages
- Notes pages separate from daily pages
- Yearly planner generation
- GUI/web app
- Advanced styling/themes
- Configuration UI
- Cloud/device integrations

---

## 8. Dependencies

**Core:**
- `reportlab` - PDF generation with bookmarks and links

**Testing:**
- `pytest` - test runner

**Optional (dev):**
- `ruff` - linting and formatting
- `mypy` - type checking
