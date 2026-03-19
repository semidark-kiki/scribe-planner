# AGENTS.md

Operational guide for agentic coding tools in this repository.

## Project Snapshot

- Project type: Python CLI that generates a monthly Kindle Scribe planner PDF.
- Primary spec: `docs/plan/POC-PRD.md`.
- Main entrypoint: `main.py`.
- Core package: `planner/` (`cli.py`, `model.py`, `layout.py`, `navigation.py`, `generator.py`).
- Tests live in `tests/` using `pytest`.

## Local Rule Files

Checked in this repo and currently not present:

- `.cursorrules`
- `.cursor/rules/`
- `.github/copilot-instructions.md`

If any of these files appear later, treat them as higher-priority local instructions than this file.

## Source of Truth

- Prefer `docs/plan/POC-PRD.md` for functional behavior and acceptance criteria.
- If code and PRD conflict, follow PRD unless the user explicitly overrides it.
- Keep PoC scope intact: month overview + daily pages + internal PDF navigation.

## Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Notes:

- `requirements.txt` includes runtime deps and `pytest`.
- If a future `requirements-dev.txt` appears, install it too.

## Build and Run Commands

Primary artifact-generation command:

```bash
python main.py --year 2026 --month 3
```

Custom output path example:

```bash
python main.py --year 2026 --month 3 --output output/2026-03-planner.pdf
```

If packaging metadata (`pyproject.toml` or `setup.cfg`) is added in the future:

```bash
python -m build
```

## Lint / Format / Type Check

Run from repository root:

```bash
ruff check .
ruff format .
mypy .
```

If only one file changed, use targeted checks first:

```bash
ruff check planner/generator.py
mypy planner/generator.py
```

## Test Commands

Run full test suite:

```bash
pytest
```

Verbose fail-fast run:

```bash
pytest -x -vv
```

Run tests matching keyword expression:

```bash
pytest -k "leap and february"
```

Run a single test file:

```bash
pytest tests/test_generator.py
```

Run a single test function (important for fast iteration):

```bash
pytest tests/test_generator.py::test_creates_expected_page_count
```

Run a single test class:

```bash
pytest tests/test_cli.py::TestCLI
```

If the project ever switches to `unittest`, use:

```bash
python -m unittest discover -s tests -p "test_*.py"
python -m unittest tests.test_generator.TestPlanner.test_page_count
```

## Code Style Guidelines

Target Python 3.11+ style and typing.

### Imports

- Group imports: standard library, third-party, local package.
- Use absolute imports within `planner` modules.
- Do not use wildcard imports.
- Remove unused imports and keep import lists minimal.

### Formatting

- Follow PEP 8 and rely on formatter behavior.
- Keep lines near 88-100 chars.
- Prefer readable, composable helper functions over long monolithic blocks.
- Keep diffs focused; do not do unrelated formatting churn.

### Types

- Add type hints for public functions and non-trivial internals.
- Prefer concrete built-ins like `list[str]`, `dict[str, int]`.
- Use `dataclass` or `TypedDict` for structured payloads when appropriate.
- Avoid `Any` unless required by a boundary (library API, dynamic data).

### Naming

- Modules/files: `snake_case`.
- Functions/variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Tests should describe behavior (e.g., `test_first_day_has_no_prev_link`).

### Error Handling

- Validate CLI arguments early and fail with clear messages.
- Raise specific exceptions instead of broad `Exception`.
- Do not silently swallow errors.
- Convert expected user-facing failures into deterministic CLI output.

### Logging and CLI Output

- Use `logging` in reusable modules when diagnostic detail is useful.
- Keep CLI stdout concise and user-focused.
- Keep output deterministic so tests can assert reliably.

### Testing Standards

- Add or update tests for every behavior change.
- Cover month-length and leap-year edge cases.
- Verify navigation constraints (month/day links, first-day Prev, last-day Next).
- Prefer behavior assertions over implementation-detail assertions.

### PDF Domain Constraints

- All daily pages must share one consistent layout.
- Month page day cells must link to correct daily pages.
- Daily navigation links must never target missing destinations.
- Output should remain usable on Kindle Scribe portrait dimensions.

## PDF Visualization and Analysis

For visual verification of PDF changes (font sizes, layout, colors, etc.):

```bash
# Convert PDF pages to PNG images (150 DPI for good detail)
pdftoppm -png -r 150 output/your-planner.pdf output/page

# List generated pages
ls -lh output/page-*.png

# View specific pages (e.g., first 5 pages)
# Then analyze the images for visual correctness
```

**Use cases:**
- Verify font size changes before/after modifications
- Check layout alignment and spacing
- Validate color schemes and button styles
- Inspect hyperlink areas and visual hierarchy
- Debug rendering issues on Kindle Scribe

**Example workflow for font changes:**
1. Generate test PDF: `python main.py --year 2026 --month 3 --output output/test.pdf`
2. Convert to images: `pdftoppm -png -r 150 output/test.pdf output/page`
3. Inspect key pages:
   - `page-001.png` → First checklist/Todo page
   - `page-003.png` → Month overview (check day names/numbers)
   - `page-004.png` → Daily page (check week strip fonts)
4. Compare with previous version if needed

## Agent Workflow Expectations

- Read `docs/plan/POC-PRD.md` before significant changes.
- Keep changes scoped to the task; avoid speculative refactors.
- Run relevant lint/tests for touched code before finishing when possible.
- If a command fails due to missing environment/tooling, report command + error clearly.
- Do not modify unrelated files or generated artifacts unless requested.
- Update this file when tooling, workflow, or local rule files change.
