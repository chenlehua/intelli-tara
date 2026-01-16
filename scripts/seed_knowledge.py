#!/usr/bin/env python3
"""Knowledge base seeding script.

Loads WP29 threats, STRIDE patterns, and attack patterns into the database.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import select
from app.core.database import async_session_factory
from app.models.knowledge import KbWp29Threat, KbAttackPattern, KbSecurityRequirement


KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


async def load_wp29_threats(session):
    """Load WP29 threats from JSON file."""
    file_path = KNOWLEDGE_DIR / "wp29_threats.json"
    if not file_path.exists():
        print(f"Warning: {file_path} not found")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        threats = json.load(f)

    count = 0
    for threat in threats:
        result = await session.execute(
            select(KbWp29Threat).where(KbWp29Threat.code == threat["code"])
        )
        if not result.scalar_one_or_none():
            db_threat = KbWp29Threat(
                code=threat["code"],
                category=threat.get("category"),
                subcategory=threat.get("subcategory"),
                threat_description_en=threat.get("threat_en"),
                threat_description_zh=threat.get("threat_zh"),
                mitigation_en=threat.get("mitigation_en"),
                mitigation_zh=threat.get("mitigation_zh"),
            )
            session.add(db_threat)
            count += 1

    await session.commit()
    print(f"Loaded {count} WP29 threats.")


async def load_attack_patterns(session):
    """Load attack patterns from JSON file."""
    file_path = KNOWLEDGE_DIR / "attack_patterns.json"
    if not file_path.exists():
        print(f"Warning: {file_path} not found")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        patterns = json.load(f)

    count = 0
    for pattern in patterns:
        result = await session.execute(
            select(KbAttackPattern).where(KbAttackPattern.pattern_id == pattern["id"])
        )
        if not result.scalar_one_or_none():
            db_pattern = KbAttackPattern(
                pattern_id=pattern["id"],
                name=pattern.get("name", ""),
                description=pattern.get("description"),
                prerequisites=pattern.get("prerequisites"),
                attack_steps=pattern.get("attack_steps"),
                mitigations=pattern.get("mitigations"),
                related_cwe=pattern.get("related_cwe"),
                related_capec=pattern.get("related_capec"),
            )
            session.add(db_pattern)
            count += 1

    await session.commit()
    print(f"Loaded {count} attack patterns.")


async def load_security_requirements(session):
    """Load security requirement templates."""
    templates = [
        {
            "category": "Authentication",
            "requirement_template": "The system shall implement strong authentication mechanisms to verify user/entity identity.",
            "description": "认证机制安全需求模板",
            "related_stride": "S",
        },
        {
            "category": "Integrity",
            "requirement_template": "The system shall implement integrity protection mechanisms to detect unauthorized modifications.",
            "description": "完整性保护安全需求模板",
            "related_stride": "T",
        },
        {
            "category": "Logging",
            "requirement_template": "The system shall log all security-relevant events with sufficient detail for forensic analysis.",
            "description": "日志记录安全需求模板",
            "related_stride": "R",
        },
        {
            "category": "Encryption",
            "requirement_template": "The system shall encrypt sensitive data in transit and at rest using approved cryptographic algorithms.",
            "description": "加密保护安全需求模板",
            "related_stride": "I",
        },
        {
            "category": "Availability",
            "requirement_template": "The system shall implement mechanisms to ensure service availability and resilience against denial of service attacks.",
            "description": "可用性保护安全需求模板",
            "related_stride": "D",
        },
        {
            "category": "Authorization",
            "requirement_template": "The system shall implement role-based access control to enforce the principle of least privilege.",
            "description": "授权控制安全需求模板",
            "related_stride": "E",
        },
    ]

    count = 0
    for template in templates:
        result = await session.execute(
            select(KbSecurityRequirement).where(
                KbSecurityRequirement.category == template["category"]
            )
        )
        if not result.scalar_one_or_none():
            db_req = KbSecurityRequirement(
                category=template["category"],
                requirement_template=template["requirement_template"],
                description=template.get("description"),
                related_stride=template.get("related_stride"),
            )
            session.add(db_req)
            count += 1

    await session.commit()
    print(f"Loaded {count} security requirement templates.")


async def main():
    """Main seeding function."""
    print("Seeding knowledge base...")

    async with async_session_factory() as session:
        await load_wp29_threats(session)
        await load_attack_patterns(session)
        await load_security_requirements(session)

    print("Knowledge base seeding completed.")


if __name__ == "__main__":
    asyncio.run(main())
