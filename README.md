# Kindle Scribe Personal Planner PDF Generator

A Python CLI tool that generates hyperlinked monthly planner PDFs optimized for the Kindle Scribe.

## Features

- Generate monthly planner PDFs with one month overview page and daily pages
- Internal PDF hyperlinks for navigation between pages
- Kindle Scribe-optimized portrait layout (1404 x 1872 points)
- Consistent daily page layout for all days
- Navigation strip with Month and Checklist buttons on each daily page
- Week navigation bar showing all 7 days of the week
- Daily Routines section with checkboxes
- Todo section with checkboxes and writing lines
- Notes index with 10 numbered pages per day
- Checklist pages with 15 items per page (3 pages total)

## Requirements

- Python 3.11+

### Runtime Dependencies

- reportlab

### Development Dependencies

- pytest
- ruff
- mypy

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Generate a planner PDF for a specific month:

```bash
python main.py --year 2026 --month 3
```

This creates `2026-03-planner.pdf` by default.

### Custom Output Path

```bash
python main.py --year 2026 --month 3 --output output/march_2026.pdf
```

### Command Line Arguments

- `--year`: Year for the planner (required, e.g., 2026)
- `--month`: Month for the planner (required, 1-12)
- `--output`: Output file path (optional, defaults to `YYYY-MM-planner.pdf`)

## Output

The generated PDF includes:

1. **Month Overview Page**: Calendar grid with clickable day cells and Checklist button
2. **Daily Pages**: One page per day with:
   - Full date title (e.g., "March 15, 2026")
   - Navigation strip with Month button, 7-day week view, and Checklist button
   - Daily Routines section (Check Calendar, Check Email, Book Times, Take a Break)
   - Todo section with 7 checkboxes and writing lines
   - Notes index with 10 numbered pages linking to note pages
3. **Checklist Pages**: 3 pages with 15 empty checkboxes and writing lines each
4. **Note Pages**: 10 ruled pages per day for free-form notes

### Navigation

- Click day numbers on the month page to jump to that day's page
- Use Month button on any page to return to month overview
- Use Checklist button to jump to checklist pages
- Click week day cells in the navigation strip to jump to adjacent days
- Click note page numbers to jump to corresponding note pages

## Examples

```bash
# March 2026 (31 days)
python main.py --year 2026 --month 3

# February 2024 (leap year, 29 days)
python main.py --year 2024 --month 2

# February 2025 (28 days)
python main.py --year 2025 --month 2

# April 2026 (30 days)
python main.py --year 2026 --month 4
```

## Running Tests

```bash
pytest -x -vv
```

Run a specific test:

```bash
pytest tests/test_model.py::test_february_leap_29_days
```

## Development

### Linting and Type Checking

```bash
ruff check .
ruff format .
mypy .
```

## Project Structure

```
.
├── .gitattributes        # Line ending configuration
├── AGENTS.md             # Agent instructions
├── LICENSE               # MIT license
├── README.md             # This file
├── main.py               # Entry point
├── output/               # Generated PDFs
├── planner/
│   ├── __init__.py
│   ├── cli.py            # CLI argument parsing
│   ├── generator.py      # PDF generation
│   ├── layout.py         # Page layout constants
│   ├── model.py          # Calendar/date logic
│   └── navigation.py     # Bookmark/link helpers
├── requirements.txt      # Dependencies
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_generator.py
    └── test_model.py
```

## License

This project is licensed under the **Business Source License 1.1 (BSL 1.1)**.

### What This Means

- **Free for personal use**: You can use this tool for your own planner generation
- **Free for internal business use**: You can use it within your company for internal operations
- **No competing products**: You cannot offer a competing planner generation service or product
- **Future open source**: On 2030-01-01, the code will automatically convert to Apache License 2.0

### Commercial Licensing

If you want to use this software for a competing product or service, please contact the author for a commercial license.

See [`LICENSE`](LICENSE) for the full text.
