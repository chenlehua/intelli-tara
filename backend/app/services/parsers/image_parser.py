"""Image parser for OCR and visual understanding."""

import base64
import io
from typing import Optional

from PIL import Image

from app.services.parsers.base import BaseParser, ParsedContent


class ImageParser(BaseParser):
    """Parser for image files using OCR and visual understanding."""

    @property
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions."""
        return ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp']

    async def parse(self, file_path: str) -> ParsedContent:
        """Parse an image file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            ParsedContent with image data
        """
        result = ParsedContent()

        try:
            # Load image
            with open(file_path, 'rb') as f:
                image_bytes = f.read()

            result.images.append(image_bytes)

            # Get image metadata
            img = Image.open(io.BytesIO(image_bytes))
            result.metadata = {
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
                "width": img.width,
                "height": img.height,
            }

            # Convert to base64 for API calls
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            result.metadata["base64_preview"] = base64_image[:100] + "..."

        except Exception as e:
            result.metadata["error"] = str(e)

        return result

    @staticmethod
    def image_to_base64(image_bytes: bytes) -> str:
        """Convert image bytes to base64 string."""
        return base64.b64encode(image_bytes).decode('utf-8')

    @staticmethod
    def create_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
        """Create a data URL from image bytes."""
        base64_data = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:{mime_type};base64,{base64_data}"
