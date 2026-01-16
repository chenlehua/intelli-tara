"""Document processing service."""

import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DocumentParseError, NotFoundError
from app.models.document import Document
from app.services.parsers import ParserFactory, ParsedContent


class DocumentService:
    """Service for document processing operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def parse_document(self, document_id: int) -> ParsedContent:
        """Parse a document and update its status.
        
        Args:
            document_id: ID of the document to parse
            
        Returns:
            ParsedContent with extracted content
            
        Raises:
            NotFoundError: If document not found
            DocumentParseError: If parsing fails
        """
        from sqlalchemy import select

        # Get document
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise NotFoundError(f"Document {document_id} not found")

        # Update status to parsing
        document.parse_status = "parsing"
        await self.db.commit()

        try:
            # Get file path
            file_path = f"/tmp/tara-documents/{document.storage_path}"

            if not os.path.exists(file_path):
                raise DocumentParseError(f"Document file not found: {document.storage_path}")

            # Get appropriate parser
            parser = ParserFactory.get_parser(document.file_type)

            if not parser:
                raise DocumentParseError(f"No parser available for file type: {document.file_type}")

            # Parse document
            content = await parser.parse(file_path)

            # Update document with results
            document.parse_status = "completed"
            document.parse_result = content.to_dict()
            document.parse_error = None
            await self.db.commit()

            return content

        except Exception as e:
            # Update document with error
            document.parse_status = "failed"
            document.parse_error = str(e)
            await self.db.commit()
            raise DocumentParseError(str(e))

    async def get_parse_result(self, document_id: int) -> Optional[dict]:
        """Get the parse result for a document.
        
        Args:
            document_id: ID of the document
            
        Returns:
            Parse result dictionary or None
        """
        from sqlalchemy import select

        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            return None

        return document.parse_result
