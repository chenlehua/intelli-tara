"""AI-powered asset identification service."""

import json
from typing import Any, Dict, List, Optional

from app.clients.ai.qwen_client import QwenClient
from app.clients.ai.prompts.asset_identification import (
    ASSET_IDENTIFICATION_PROMPT,
    ASSET_IDENTIFICATION_FROM_ARCHITECTURE_PROMPT,
)
from app.core.exceptions import AIServiceError
from app.schemas.asset import AssetCreate


class AssetIdentifier:
    """Service for AI-powered asset identification."""

    def __init__(self, qwen_client: Optional[QwenClient] = None):
        """Initialize the asset identifier.
        
        Args:
            qwen_client: Optional QwenClient instance. If not provided,
                        a new one will be created.
        """
        self._client = qwen_client
        self._owns_client = qwen_client is None

    async def _get_client(self) -> QwenClient:
        """Get or create the Qwen client."""
        if self._client is None:
            self._client = QwenClient()
        return self._client

    async def close(self):
        """Close resources."""
        if self._owns_client and self._client is not None:
            await self._client.close()

    async def identify_from_text(self, text: str) -> List[AssetCreate]:
        """Identify assets from text content.
        
        Args:
            text: Document text content
            
        Returns:
            List of identified assets
        """
        client = await self._get_client()

        messages = [
            {"role": "system", "content": ASSET_IDENTIFICATION_PROMPT},
            {"role": "user", "content": f"请从以下文档内容中识别资产:\n\n{text[:10000]}"}
        ]

        try:
            response = await client.chat_completion(
                messages=messages,
                model="qwen-max",
                temperature=0.3,
                response_format="json",
            )

            # Parse response
            assets_data = self._parse_json_response(response)
            assets_list = assets_data.get("assets", [])

            return [self._create_asset(asset) for asset in assets_list]

        except Exception as e:
            raise AIServiceError(f"Asset identification failed: {str(e)}")

    async def identify_from_architecture(
        self,
        image_bytes: bytes,
        mime_type: str = "image/png"
    ) -> Dict[str, Any]:
        """Identify assets and relations from an architecture diagram.
        
        Args:
            image_bytes: Image file content
            mime_type: MIME type of the image
            
        Returns:
            Dict with 'assets' and 'relations' lists
        """
        client = await self._get_client()

        # Convert image to data URL
        image_url = client.image_to_data_url(image_bytes, mime_type)

        try:
            response = await client.vision_completion(
                image_url=image_url,
                prompt=ASSET_IDENTIFICATION_FROM_ARCHITECTURE_PROMPT,
                model="qwen-vl-max",
                temperature=0.3,
            )

            # Parse response
            result = self._parse_json_response(response)

            assets = [self._create_asset(a) for a in result.get("assets", [])]
            relations = result.get("relations", [])

            return {"assets": assets, "relations": relations}

        except Exception as e:
            raise AIServiceError(f"Architecture analysis failed: {str(e)}")

    async def identify_from_parsed_content(
        self,
        parsed_content: Dict[str, Any]
    ) -> List[AssetCreate]:
        """Identify assets from parsed document content.
        
        Args:
            parsed_content: Parsed document content dict
            
        Returns:
            List of identified assets
        """
        # Combine text blocks
        text_content = "\n\n".join(parsed_content.get("text_blocks", []))

        # Process tables
        table_content = ""
        for table in parsed_content.get("tables", []):
            for row in table:
                table_content += " | ".join(str(cell) for cell in row) + "\n"

        combined_content = f"{text_content}\n\n{table_content}"

        return await self.identify_from_text(combined_content)

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response.
        
        The response may contain markdown code blocks.
        """
        # Try to extract JSON from code blocks
        content = response.strip()

        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            if end > start:
                content = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            if end > start:
                content = content[start:end].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise AIServiceError(f"Failed to parse AI response as JSON: {str(e)}")

    def _create_asset(self, data: Dict[str, Any]) -> AssetCreate:
        """Create AssetCreate object from parsed data."""
        # Map Chinese category names to English if needed
        category_map = {
            "硬件资产": "Hardware",
            "软件资产": "Software",
            "数据资产": "Data",
            "接口资产": "Interface",
            "外部实体": "External",
        }

        category = data.get("category", "Other")
        if category in category_map:
            category = category_map[category]

        return AssetCreate(
            asset_id=data.get("asset_id", ""),
            name=data.get("name", ""),
            category=category,
            subcategory=data.get("subcategory"),
            description=data.get("description"),
            remarks=data.get("remarks"),
            authenticity=data.get("authenticity", False),
            integrity=data.get("integrity", False),
            non_repudiation=data.get("non_repudiation", False),
            confidentiality=data.get("confidentiality", False),
            availability=data.get("availability", False),
            authorization=data.get("authorization", False),
        )
