"""Document parsers package."""

from app.services.parsers.base import BaseParser, ParsedContent, ParserFactory
from app.services.parsers.pdf_parser import PDFParser
from app.services.parsers.word_parser import WordParser
from app.services.parsers.excel_parser import ExcelParser
from app.services.parsers.image_parser import ImageParser

# Register parsers
ParserFactory.register(PDFParser())
ParserFactory.register(WordParser())
ParserFactory.register(ExcelParser())
ParserFactory.register(ImageParser())

__all__ = [
    "BaseParser",
    "ParsedContent",
    "ParserFactory",
    "PDFParser",
    "WordParser",
    "ExcelParser",
    "ImageParser",
]
