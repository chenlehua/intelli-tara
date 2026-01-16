"""Base parser interface and factory."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ParsedContent:
    """Parsed document content."""

    text_blocks: List[str] = field(default_factory=list)
    tables: List[List[List[str]]] = field(default_factory=list)
    images: List[bytes] = field(default_factory=list)
    image_urls: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text_blocks": self.text_blocks,
            "tables": self.tables,
            "images": [f"<image:{len(img)} bytes>" for img in self.images],
            "image_urls": self.image_urls,
            "metadata": self.metadata,
        }


class BaseParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    async def parse(self, file_path: str) -> ParsedContent:
        """Parse a document file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            ParsedContent object with extracted content
        """
        pass

    @abstractmethod
    def supports(self, file_type: str) -> bool:
        """Check if this parser supports the given file type.
        
        Args:
            file_type: File extension (e.g., 'pdf', 'docx')
            
        Returns:
            True if supported, False otherwise
        """
        pass


class ParserFactory:
    """Factory for getting appropriate document parser."""

    _parsers: List[BaseParser] = []

    @classmethod
    def register(cls, parser: BaseParser) -> None:
        """Register a parser instance."""
        cls._parsers.append(parser)

    @classmethod
    def get_parser(cls, file_type: str) -> Optional[BaseParser]:
        """Get a parser that supports the given file type.
        
        Args:
            file_type: File extension (without dot)
            
        Returns:
            Parser instance or None if no parser supports this type
        """
        file_type = file_type.lower().lstrip('.')
        for parser in cls._parsers:
            if parser.supports(file_type):
                return parser
        return None

    @classmethod
    def supported_types(cls) -> List[str]:
        """Get list of all supported file types."""
        types = set()
        for parser in cls._parsers:
            # Each parser should define its supported types
            pass
        return list(types)
