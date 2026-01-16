"""
Tests for document parsers.
"""
import pytest
import sys
sys.path.insert(0, '.')

from app.services.parsers.base import ParserFactory


class TestParserFactory:
    """Tests for ParserFactory class."""

    def test_get_parser_for_pdf(self):
        """Test getting parser for PDF files."""
        parser = ParserFactory.get_parser("pdf")
        assert parser is not None
        assert parser.supported_extensions == ["pdf"]

    def test_get_parser_for_word(self):
        """Test getting parser for Word files."""
        parser = ParserFactory.get_parser("docx")
        assert parser is not None
        assert "docx" in parser.supported_extensions

    def test_get_parser_for_excel(self):
        """Test getting parser for Excel files."""
        parser = ParserFactory.get_parser("xlsx")
        assert parser is not None
        assert "xlsx" in parser.supported_extensions

    def test_get_parser_for_image(self):
        """Test getting parser for image files."""
        parser = ParserFactory.get_parser("png")
        assert parser is not None
        assert "png" in parser.supported_extensions

    def test_get_parser_unsupported(self):
        """Test getting parser for unsupported file type."""
        parser = ParserFactory.get_parser("xyz")
        assert parser is None

    def test_supported_extensions(self):
        """Test getting all supported extensions."""
        extensions = ParserFactory.get_supported_extensions()
        assert "pdf" in extensions
        assert "docx" in extensions
        assert "xlsx" in extensions
        assert "png" in extensions
        assert "jpg" in extensions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
