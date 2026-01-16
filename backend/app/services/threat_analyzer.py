"""AI-powered threat analysis service."""

import json
from typing import Any, Dict, List, Optional

from app.clients.ai.qwen_client import QwenClient
from app.clients.ai.prompts.threat_analysis import (
    THREAT_ANALYSIS_PROMPT,
    THREAT_ANALYSIS_FOR_ASSET_PROMPT,
)
from app.core.exceptions import AIServiceError
from app.models.asset import Asset
from app.schemas.threat import MitigationCreate, ThreatCreate
from app.services.risk_calculator import RiskCalculator


class ThreatAnalyzer:
    """Service for AI-powered threat analysis."""

    def __init__(self, qwen_client: Optional[QwenClient] = None):
        """Initialize the threat analyzer.
        
        Args:
            qwen_client: Optional QwenClient instance
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

    async def analyze_asset(self, asset: Asset) -> List[Dict[str, Any]]:
        """Analyze threats for a specific asset.
        
        Args:
            asset: Asset to analyze
            
        Returns:
            List of threat data dicts with threat and mitigation info
        """
        client = await self._get_client()

        # Build prompt with asset info
        asset_prompt = THREAT_ANALYSIS_FOR_ASSET_PROMPT.format(
            asset_id=asset.asset_id,
            asset_name=asset.name,
            category=asset.category,
            subcategory=asset.subcategory or "N/A",
            description=asset.description or "N/A",
            authenticity=asset.authenticity,
            integrity=asset.integrity,
            non_repudiation=asset.non_repudiation,
            confidentiality=asset.confidentiality,
            availability=asset.availability,
            authorization=asset.authorization,
        )

        messages = [
            {"role": "system", "content": THREAT_ANALYSIS_PROMPT},
            {"role": "user", "content": asset_prompt}
        ]

        try:
            response = await client.chat_completion(
                messages=messages,
                model="qwen-max",
                temperature=0.5,
                response_format="json",
            )

            threats_data = self._parse_json_response(response)
            threats_list = threats_data.get("threats", [])

            # Process each threat
            result = []
            for i, threat_data in enumerate(threats_list):
                threat = self._create_threat(threat_data, asset.id, i + 1)
                mitigation = self._create_mitigation(threat_data)
                result.append({
                    "threat": threat,
                    "mitigation": mitigation,
                })

            return result

        except Exception as e:
            raise AIServiceError(f"Threat analysis failed: {str(e)}")

    async def analyze_assets_batch(
        self,
        assets: List[Asset]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """Analyze threats for multiple assets.
        
        Args:
            assets: List of assets to analyze
            
        Returns:
            Dict mapping asset ID to list of threat data
        """
        results = {}
        for asset in assets:
            try:
                threats = await self.analyze_asset(asset)
                results[asset.id] = threats
            except Exception as e:
                # Log error but continue with other assets
                results[asset.id] = []

        return results

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response."""
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

    def _create_threat(
        self,
        data: Dict[str, Any],
        asset_id: int,
        index: int
    ) -> ThreatCreate:
        """Create ThreatCreate object from parsed data."""
        threat_id = data.get("threat_id", f"T-{index:03d}")

        # Map STRIDE type
        stride_map = {
            "Spoofing": "S", "欺骗": "S", "S": "S",
            "Tampering": "T", "篡改": "T", "T": "T",
            "Repudiation": "R", "抵赖": "R", "R": "R",
            "Information Disclosure": "I", "信息泄露": "I", "I": "I",
            "Denial of Service": "D", "拒绝服务": "D", "D": "D",
            "Elevation of Privilege": "E", "权限提升": "E", "E": "E",
        }
        stride_type = stride_map.get(data.get("stride_type", ""), "S")

        # Map security attribute
        attr_map = {
            "S": "Authenticity",
            "T": "Integrity",
            "R": "Non-repudiation",
            "I": "Confidentiality",
            "D": "Availability",
            "E": "Authorization",
        }

        return ThreatCreate(
            asset_id=asset_id,
            threat_id=threat_id,
            security_attribute=data.get("security_attribute", attr_map.get(stride_type, "")),
            stride_type=stride_type,
            threat_description=data.get("threat_description", ""),
            damage_scenario=data.get("damage_scenario"),
            attack_path=data.get("attack_path"),
            source_reference=data.get("source_reference"),
            wp29_mapping=data.get("wp29_mapping"),
            attack_vector=data.get("attack_vector"),
            attack_complexity=data.get("attack_complexity"),
            privileges_required=data.get("privileges_required"),
            user_interaction=data.get("user_interaction"),
            impact_safety=data.get("impact_safety"),
            impact_financial=data.get("impact_financial"),
            impact_operational=data.get("impact_operational"),
            impact_privacy=data.get("impact_privacy"),
        )

    def _create_mitigation(self, data: Dict[str, Any]) -> Optional[MitigationCreate]:
        """Create MitigationCreate object from parsed data."""
        if not any([
            data.get("security_goal"),
            data.get("security_requirement"),
            data.get("wp29_control"),
        ]):
            return None

        return MitigationCreate(
            security_goal=data.get("security_goal"),
            security_requirement=data.get("security_requirement"),
            wp29_control_mapping=data.get("wp29_control"),
            implementation_status="planned",
        )
