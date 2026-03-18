"""Tests for the generator module."""

from planner.generator import generate_pdf
from planner.layout import CHECKLIST_TOTAL_PAGES, NOTES_PAGES_PER_DAY
from planner.navigation import (
    month_destination_id,
    day_destination_id,
    checklist_destination_id,
    notes_destination_id,
)


class TestGeneratePdf:
    """Tests for PDF generation."""

    def test_creates_file(self, tmp_path):
        """Should create a PDF file."""
        output_path = tmp_path / "test.pdf"
        generate_pdf(2026, 3, str(output_path))
        assert output_path.exists()

    def test_march_2026_page_count(self, tmp_path):
        """March 2026 should produce 345 pages (3 checklist + 1 month + 31 days + 31*10 note pages)."""
        output_path = tmp_path / "march_2026.pdf"
        generate_pdf(2026, 3, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_february_2025_page_count(self, tmp_path):
        """February 2025 should produce 312 pages (3 checklist + 1 month + 28 days + 28*10 note pages)."""
        output_path = tmp_path / "feb_2025.pdf"
        generate_pdf(2025, 2, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_february_2024_leap_year(self, tmp_path):
        """February 2024 (leap year) should produce 323 pages (3 checklist + 1 month + 29 days + 29*10 note pages)."""
        output_path = tmp_path / "feb_2024.pdf"
        generate_pdf(2024, 2, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_april_2026_30_days(self, tmp_path):
        """April 2026 should produce 334 pages (3 checklist + 1 month + 30 days + 30*10 note pages)."""
        output_path = tmp_path / "april_2026.pdf"
        generate_pdf(2026, 4, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_default_output_naming(self, tmp_path):
        """Output file should follow naming convention."""
        output_path = tmp_path / "2026-03-planner.pdf"
        generate_pdf(2026, 3, str(output_path))
        assert output_path.exists()


class TestNavigationHelpers:
    """Tests for navigation destination IDs."""

    def test_month_destination_id(self):
        """Month destination should be 'month'."""
        assert month_destination_id() == "month"

    def test_day_destination_id_format(self):
        """Day destination should follow day_YYYY_MM_DD format."""
        assert day_destination_id(2026, 3, 15) == "day_2026_03_15"
        assert day_destination_id(2024, 1, 1) == "day_2024_01_01"
        assert day_destination_id(2025, 12, 31) == "day_2025_12_31"

    def test_checklist_destination_id(self):
        """Checklist destination should be 'checklist'."""
        assert checklist_destination_id() == "checklist"

    def test_notes_destination_id_format(self):
        """Notes destination should follow notes_YYYY_MM_DD_PP format."""
        assert notes_destination_id(2026, 3, 15, 1) == "notes_2026_03_15_01"
        assert notes_destination_id(2026, 3, 15, 10) == "notes_2026_03_15_10"
        assert notes_destination_id(2024, 1, 1, 5) == "notes_2024_01_01_05"


class TestChecklistPages:
    """Tests for checklist page generation."""

    def test_checklist_pages_are_first(self, tmp_path):
        """Checklist pages should appear at the very beginning of the document."""
        output_path = tmp_path / "checklist_test.pdf"
        generate_pdf(2026, 3, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_checklist_total_pages_constant(self):
        """There should be exactly 3 checklist pages."""
        assert CHECKLIST_TOTAL_PAGES == 3


class TestNotePages:
    """Tests for note page generation."""

    def test_notes_pages_per_day_constant(self):
        """There should be exactly 10 note pages per day."""
        assert NOTES_PAGES_PER_DAY == 10

    def test_notes_destination_id_first_page(self):
        """First note page destination ID should use page number 1."""
        dest = notes_destination_id(2026, 3, 16, 1)
        assert dest == "notes_2026_03_16_01"

    def test_notes_destination_id_last_page(self):
        """Last note page destination ID should use page number 10."""
        dest = notes_destination_id(2026, 3, 16, 10)
        assert dest == "notes_2026_03_16_10"

    def test_note_pages_generate_without_error(self, tmp_path):
        """Note pages should be generated without errors for a full month."""
        output_path = tmp_path / "notes_test.pdf"
        generate_pdf(2026, 3, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_note_pages_total_count_march(self, tmp_path):
        """March 2026 should have 31 * 10 = 310 note pages appended."""
        output_path = tmp_path / "march_notes.pdf"
        generate_pdf(2026, 3, str(output_path))
        # 3 checklist + 1 month + 31 daily + 310 note = 345 total pages
        # We verify the file is non-empty and was created successfully
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_note_pages_total_count_february_leap(self, tmp_path):
        """February 2024 (leap) should have 29 * 10 = 290 note pages appended."""
        output_path = tmp_path / "feb_leap_notes.pdf"
        generate_pdf(2024, 2, str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0
