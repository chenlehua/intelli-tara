"""PDF document parser using PyMuPDF."""

import io
from typing import List

import fitz  # PyMuPDF

from app.services.parsers.base import BaseParser, ParsedContent


class PDFParser(BaseParser):
    """Parser for PDF documents."""

    @property
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions."""
        return ['pdf']

    async def parse(self, file_path: str) -> ParsedContent:
        """Parse a PDF document.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            ParsedContent with extracted text, tables, and images
        """
        result = ParsedContent()
        
        try:
            doc = fitz.open(file_path)
            result.metadata = {
                "page_count": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
            }

            for page_num, page in enumerate(doc):
                # Extract text
                text = page.get_text()
                if text.strip():
                    result.text_blocks.append(text)

                # Extract tables
                tables = self._extract_tables(page)
                result.tables.extend(tables)

                # Extract images
                images = self._extract_images(doc, page)
                result.images.extend(images)

            doc.close()

        except Exception as e:
            result.metadata["error"] = str(e)

        return result

    def _extract_tables(self, page: fitz.Page) -> List[List[List[str]]]:
        """Extract tables from a PDF page."""
        tables = []
        try:
            # Use PyMuPDF's table detection
            found_tables = page.find_tables()
            for table in found_tables:
                table_data = table.extract()
                if table_data:
                    tables.append(table_data)
        except Exception:
            pass
        return tables

    def _extract_images(self, doc: fitz.Document, page: fitz.Page) -> List[bytes]:
        """Extract images from a PDF page."""
        images = []
        try:
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                if base_image:
                    image_bytes = base_image.get("image")
                    if image_bytes:
                        images.append(image_bytes)
        except Exception:
            pass
        return images
