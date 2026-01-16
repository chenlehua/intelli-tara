"""Knowledge base service."""

from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KbAttackPattern, KbSecurityRequirement, KbWp29Threat


class KnowledgeService:
    """Service for accessing knowledge base data."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_wp29_threats(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[KbWp29Threat]:
        """Get WP29 threats from knowledge base.
        
        Args:
            category: Optional category filter
            search: Optional search term
            
        Returns:
            List of WP29 threat records
        """
        query = select(KbWp29Threat)

        if category:
            query = query.where(KbWp29Threat.category == category)

        if search:
            query = query.where(
                KbWp29Threat.threat_description_zh.contains(search) |
                KbWp29Threat.threat_description_en.contains(search)
            )

        result = await self.db.execute(query.order_by(KbWp29Threat.code))
        return list(result.scalars().all())

    async def get_wp29_threat_by_code(self, code: str) -> Optional[KbWp29Threat]:
        """Get a specific WP29 threat by code.
        
        Args:
            code: WP29 threat code (e.g., "4.3.1")
            
        Returns:
            WP29 threat record or None
        """
        result = await self.db.execute(
            select(KbWp29Threat).where(KbWp29Threat.code == code)
        )
        return result.scalar_one_or_none()

    async def get_attack_patterns(
        self,
        search: Optional[str] = None,
    ) -> List[KbAttackPattern]:
        """Get attack patterns from knowledge base.
        
        Args:
            search: Optional search term
            
        Returns:
            List of attack pattern records
        """
        query = select(KbAttackPattern)

        if search:
            query = query.where(
                KbAttackPattern.name.contains(search) |
                KbAttackPattern.description.contains(search)
            )

        result = await self.db.execute(query.order_by(KbAttackPattern.pattern_id))
        return list(result.scalars().all())

    async def get_attack_pattern_by_id(self, pattern_id: str) -> Optional[KbAttackPattern]:
        """Get a specific attack pattern by ID.
        
        Args:
            pattern_id: Attack pattern ID
            
        Returns:
            Attack pattern record or None
        """
        result = await self.db.execute(
            select(KbAttackPattern).where(KbAttackPattern.pattern_id == pattern_id)
        )
        return result.scalar_one_or_none()

    async def get_security_requirements(
        self,
        category: Optional[str] = None,
        stride_type: Optional[str] = None,
    ) -> List[KbSecurityRequirement]:
        """Get security requirement templates.
        
        Args:
            category: Optional category filter
            stride_type: Optional STRIDE type filter
            
        Returns:
            List of security requirement templates
        """
        query = select(KbSecurityRequirement)

        if category:
            query = query.where(KbSecurityRequirement.category == category)

        if stride_type:
            query = query.where(KbSecurityRequirement.related_stride == stride_type)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search_knowledge(
        self,
        query_text: str,
        knowledge_type: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search across all knowledge bases.
        
        Args:
            query_text: Search query
            knowledge_type: Optional filter by knowledge type
            limit: Maximum results per type
            
        Returns:
            Dict with results grouped by knowledge type
        """
        results = {
            "wp29_threats": [],
            "attack_patterns": [],
            "security_requirements": [],
        }

        if not knowledge_type or knowledge_type == "wp29_threats":
            threats = await self.get_wp29_threats(search=query_text)
            results["wp29_threats"] = [
                {
                    "code": t.code,
                    "category": t.category,
                    "threat_zh": t.threat_description_zh,
                    "threat_en": t.threat_description_en,
                    "mitigation_zh": t.mitigation_zh,
                }
                for t in threats[:limit]
            ]

        if not knowledge_type or knowledge_type == "attack_patterns":
            patterns = await self.get_attack_patterns(search=query_text)
            results["attack_patterns"] = [
                {
                    "id": p.pattern_id,
                    "name": p.name,
                    "description": p.description,
                    "mitigations": p.mitigations,
                }
                for p in patterns[:limit]
            ]

        if not knowledge_type or knowledge_type == "security_requirements":
            reqs = await self.get_security_requirements()
            # Filter by search text
            filtered = [
                r for r in reqs
                if query_text.lower() in (r.requirement_template or "").lower() or
                   query_text.lower() in (r.category or "").lower()
            ]
            results["security_requirements"] = [
                {
                    "category": r.category,
                    "template": r.requirement_template,
                    "stride": r.related_stride,
                }
                for r in filtered[:limit]
            ]

        return results

    async def get_mitigation_suggestions(
        self,
        stride_type: str,
        threat_description: str,
    ) -> List[Dict[str, str]]:
        """Get mitigation suggestions based on threat info.
        
        Args:
            stride_type: STRIDE threat type
            threat_description: Description of the threat
            
        Returns:
            List of mitigation suggestions
        """
        suggestions = []

        # Get relevant security requirements
        reqs = await self.get_security_requirements(stride_type=stride_type)
        for req in reqs:
            suggestions.append({
                "source": "security_requirements",
                "category": req.category,
                "suggestion": req.requirement_template,
            })

        # Search WP29 for related mitigations
        wp29_threats = await self.get_wp29_threats(search=threat_description[:50])
        for threat in wp29_threats[:3]:
            if threat.mitigation_zh:
                suggestions.append({
                    "source": "wp29",
                    "code": threat.code,
                    "suggestion": threat.mitigation_zh,
                })

        return suggestions
