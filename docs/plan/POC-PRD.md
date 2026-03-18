## Project: Kindle Scribe Monthly Planner PDF Generator (PoC)

## 1. Objective

Build a Python proof of concept that generates a **hyperlinked monthly planner PDF** optimized for **Kindle Scribe**.

The PoC must:
- generate the planner fully in code
- create a single PDF for a given month/year
- include one **month overview page**
- include one **daily page for every day in the month**
- ensure **all daily pages have the same layout**
- support **internal PDF hyperlinks** for navigation

This is a PoC for later expansion into a more configurable planner generator that may support custom PDF templates.

---

## 2. Primary Use Case

User runs a command like:

```bash
python main.py --year 2026 --month 3
```

The tool generates:

```text
2026-03-planner.pdf
```

The resulting PDF should contain:
- page 1: month overview
- page 2..N: one daily page per day of the month

The PDF must support:
- month page → daily page links
- daily page → previous day
- daily page → next day
- daily page → month overview

---

## 3. Scope

## In Scope
- Python CLI tool
- month/year input
- single PDF output
- code-rendered PDF generation
- month overview page
- daily pages
- internal hyperlinks
- same daily layout for weekdays and weekends

## Out of Scope
- custom PDF templates
- weekly pages
- notes pages separate from daily pages
- yearly planner generation
- GUI/web app
- advanced styling/themes
- configuration UI
- cloud/device integrations

---

## 4. Functional Requirements

## 4.1 Inputs
Required CLI inputs:
- `--year`
- `--month`

Optional CLI input:
- `--output`

Examples:
```bash
python main.py --year 2026 --month 3
python main.py --year 2026 --month 3 --output output/2026-03-planner.pdf
```

## 4.2 Output
Generate one PDF file.

Default filename format if no output path is provided:
```text
YYYY-MM-planner.pdf
```

Example:
```text
2026-03-planner.pdf
```

## 4.3 PDF Page Order
The generated PDF must be ordered as follows:
1. month overview page
2. daily page for day 1
3. daily page for day 2
4. ...
5. daily page for last day of month

Example for March 2026:
- page 1 = month overview
- page 2 = March 1
- page 32 = March 31

## 4.4 Month Overview Page Requirements
Must include:
- month name and year as title
- weekday headers
- calendar grid for the selected month
- visible day numbers for valid days only

Must support internal links:
- clicking day `N` navigates to daily page for day `N`

May leave non-month calendar cells blank.

## 4.5 Daily Page Requirements
Each daily page must include:
- full date title, e.g. `Monday, March 16, 2026`
- same layout for all days
- visible navigation controls/labels:
  - `Prev`
  - `Month`
  - `Next`

Each daily page must also include at minimum these content sections:
- `Tasks`
- `Meetings`
- `Notes`

These can be simple outlined regions or labeled blocks.

## 4.6 Daily Page Uniformity
All daily pages must use the same structure and visual layout.
No special weekend layout.

## 4.7 Navigation Requirements
Internal PDF navigation must include:

### On month page
- every valid day cell links to corresponding daily page

### On daily pages
- `Month` links to month overview
- `Prev` links to previous day if current page is not the first day
- `Next` links to next day if current page is not the last day

For the first day:
- `Prev` must not create a broken link

For the last day:
- `Next` must not create a broken link

Acceptable behavior:
- render label without link
- visually disable label
- omit link while keeping label visible

---

## 5. Non-Functional Requirements

## 5.1 Device Suitability
Output should be usable on Kindle Scribe in portrait orientation.

Use a page size/aspect ratio suitable for Kindle Scribe-like display.

Suggested default:
- width = 1404
- height = 1872

Exact dimensions may be adjusted if the chosen PDF library works better with another unit system, but portrait ratio should remain similar.

## 5.2 Usability
- font sizes should be readable on e-ink
- clickable regions should be large enough to tap comfortably
- layout should be simple and uncluttered

## 5.3 Reliability
The generated PDF must:
- open in standard PDF readers
- preserve internal navigation
- work for any valid month/year

## 5.4 Maintainability
Code structure should support future enhancements, especially:
- replacing code-rendered pages with user-supplied templates
- adding more page types
- adding config-driven layout

---

## 6. Technical Guidance

## 6.1 Language
Use Python.

## 6.2 Recommended Libraries
Preferred:
- `reportlab`

Rationale:
- can draw PDF pages directly
- supports bookmarks / named destinations
- supports internal link rectangles

Optional later:
- `pypdf` for advanced PDF merging/manipulation, not required for PoC

## 6.3 Rendering Strategy
Use a single PDF generation flow that:
1. creates the month overview page
2. creates all daily pages
3. registers named destinations/bookmarks
4. adds internal link rectangles targeting those destinations
5. writes the final PDF

Suggested bookmark naming:
- `month`
- `day_YYYY_MM_DD`

Example:
- `day_2026_03_01`
- `day_2026_03_02`

---

## 7. Suggested Architecture

Use modular code. At minimum separate:

## 7.1 CLI / entry point
Responsible for:
- parsing arguments
- validating inputs
- invoking planner generation

## 7.2 Calendar / planner model
Responsible for:
- determining number of days in month
- calculating calendar grid placement
- generating date metadata for each day

## 7.3 PDF rendering
Responsible for:
- drawing month page
- drawing daily pages
- drawing sections and labels

## 7.4 Navigation/link handling
Responsible for:
- bookmark names
- link target mapping
- adding clickable regions

This separation is important for future template support.

---

## 8. Suggested File Structure

A simple recommended structure:

```text
planner_poc/
  main.py
  requirements.txt
  README.md
  planner/
    __init__.py
    generator.py
    layout.py
    model.py
    cli.py
```

Possible responsibilities:
- `main.py`: executable entry point
- `planner/cli.py`: argument parsing and validation
- `planner/model.py`: calendar/date logic
- `planner/layout.py`: constants and page layout values
- `planner/generator.py`: PDF generation and navigation links

If the agent prefers a simpler structure for the PoC, fewer files are acceptable, but the code should still be logically separated.

---

## 9. Visual/Layout Guidance

Keep design minimal and functional.

## 9.1 Month Overview Page
Include:
- centered month/year title
- weekday row
- calendar grid with day numbers
- clickable day cells for valid dates

## 9.2 Daily Page
Include:
- top header with full date
- navigation row with:
  - Prev
  - Month
  - Next
- three main labeled sections:
  - Tasks
  - Meetings
  - Notes

Suggested relative structure:
- header near top
- nav near top or bottom, but consistent
- Tasks box in upper body
- Meetings box in middle
- Notes box as the largest lower section

Do not over-design; clarity is more important than styling.

---

## 10. Edge Cases to Handle

The implementation must correctly handle:
- 28-day months
- 29-day February in leap years
- 30-day months
- 31-day months
- months beginning on any weekday

Must also handle:
- first day has no previous link
- last day has no next link

Input validation:
- reject invalid month values
- reject missing required args
- handle invalid output path gracefully if possible

---

## 11. Acceptance Criteria

The implementation is complete when all of the following are true:

### Generation
- Running the CLI with valid `--year` and `--month` generates a PDF file successfully.

### Structure
- The PDF contains exactly:
  - 1 month overview page
  - 1 daily page for each day in the selected month

### Layout
- All daily pages use the same layout.
- Daily pages include:
  - full date title
  - Tasks section
  - Meetings section
  - Notes section
  - Prev / Month / Next labels

### Navigation
- Each valid day on the month page links to the correct daily page.
- Each daily page links back to the month page.
- Each middle daily page links correctly to both previous and next days.
- First day has no broken previous link.
- Last day has no broken next link.

### Compatibility
- Output PDF opens in standard PDF readers.
- Internal links function in supported readers.
- Output is reasonably usable on Kindle Scribe.

---

## 12. Implementation Constraints

- Do not use external PDF templates in the PoC.
- Do not implement weekly pages.
- Do not implement a GUI.
- Do not overcomplicate styling.
- Prioritize correctness and clean navigation over appearance.
- Keep code extensible for future template-based rendering.

---

## 13. Recommended Development Plan

## Phase 1
Implement CLI and basic PDF generation:
- parse month/year
- generate month page
- generate daily pages
- save PDF

## Phase 2
Add internal bookmarks and links:
- month page day-cell links
- daily page navigation links

## Phase 3
Improve readability/usability:
- refine spacing
- adjust font sizes
- enlarge clickable areas

## Phase 4
Basic cleanup:
- README
- requirements.txt
- light code organization

---

## 14. Deliverables

Required:
1. Python source code
2. `requirements.txt`
3. runnable CLI entry point
4. generated PDF output for a sample month
5. README with setup and run instructions

Preferred:
- clean module separation
- basic comments/docstrings
- simple validation and helpful error messages

---

## 15. Example Acceptance Test Cases

## Test Case 1: 31-day month
Command:
```bash
python main.py --year 2026 --month 3
```

Expected:
- PDF generated
- 32 total pages
- month page links day 1..31 correctly
- daily page nav works

## Test Case 2: 30-day month
Command:
```bash
python main.py --year 2026 --month 4
```

Expected:
- 31 total pages
- days 1..30 only
- no day 31 cell link

## Test Case 3: non-leap February
Command:
```bash
python main.py --year 2025 --month 2
```

Expected:
- 29 total pages
- days 1..28 only

## Test Case 4: leap-year February
Command:
```bash
python main.py --year 2024 --month 2
```

Expected:
- 30 total pages
- days 1..29 only

## Test Case 5: invalid month
Command:
```bash
python main.py --year 2026 --month 13
```

Expected:
- validation error
- no PDF generated

---

## 16. Future-Proofing Notes

Design the code so that future versions can introduce:

### 16.1 Template-based rendering
Later, daily/month rendering may use:
- user-supplied month template PDF
- user-supplied daily template PDF
- overlayed text and internal links

### 16.2 Config-driven layout
Future versions may define:
- page size
- text coordinates
- section positions
- link rectangles
- fonts/styles

### 16.3 Additional pages
Potential future additions:
- notes pages
- weekly pages
- IT-specific pages
- project pages

### 16.4 IT-focused daily layout
Future daily page sections may include:
- priorities
- tickets/incidents
- deployments
- blockers
- follow-ups
- on-call notes

The PoC architecture should not block these changes.

---

## 17. Final Instruction to Coding Agent

Implement a **minimal but clean** PoC that proves:
- monthly planner generation
- same-layout daily pages
- internal PDF hyperlink navigation
- Kindle Scribe-friendly output

Favor:
- simplicity
- correctness
- modularity

Do not optimize for advanced design or configurability yet.
