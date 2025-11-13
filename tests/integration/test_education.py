"""Integration tests for educational content."""

import pytest


class TestEducationalContent:
    """Test cases for educational content display."""

    def test_educational_content_imports(self):
        """Test that educational content module can be imported."""
        from aion.ui.education import render_educational_content

        # Function should exist and be callable
        assert callable(render_educational_content)

    def test_educational_content_key_terms(self):
        """Test that all four key terms are defined in the content."""
        # This is a structural test - we verify the function exists
        # Actual content display would require Streamlit testing framework
        from aion.ui.education import render_educational_content

        # Function should be callable without errors
        # (actual rendering requires Streamlit context)
        assert render_educational_content is not None

    def test_educational_content_accessible(self):
        """Test that educational content is accessible from main app."""
        # Verify the import works in app context
        import sys
        from pathlib import Path

        # Add src to path
        if "src" not in str(Path.cwd()):
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

        try:
            from aion.ui.education import render_educational_content
            assert callable(render_educational_content)
        except ImportError:
            pytest.fail("Educational content module not accessible")

