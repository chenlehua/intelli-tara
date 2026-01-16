"""Knowledge base API endpoints."""

from typing import Optional

from fastapi import APIRouter, Query

from app.api.v1.deps import CurrentUser, DbSession
from app.schemas.common import ResponseModel
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.get("/wp29-threats", response_model=ResponseModel)
async def list_wp29_threats(
    current_user: CurrentUser,
    db: DbSession,
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    """List WP29 threats from knowledge base."""
    service = KnowledgeService(db)
    threats = await service.get_wp29_threats(category=category, search=search)

    return ResponseModel(
        data=[
            {
                "code": t.code,
                "category": t.category,
                "subcategory": t.subcategory,
                "threat_en": t.threat_description_en,
                "threat_zh": t.threat_description_zh,
                "mitigation_en": t.mitigation_en,
                "mitigation_zh": t.mitigation_zh,
            }
            for t in threats
        ]
    )


@router.get("/wp29-threats/{code}", response_model=ResponseModel)
async def get_wp29_threat(
    code: str,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get a specific WP29 threat by code."""
    service = KnowledgeService(db)
    threat = await service.get_wp29_threat_by_code(code)

    if not threat:
        return ResponseModel(code=40001, message="WP29 threat not found")

    return ResponseModel(
        data={
            "code": threat.code,
            "category": threat.category,
            "subcategory": threat.subcategory,
            "threat_en": threat.threat_description_en,
            "threat_zh": threat.threat_description_zh,
            "mitigation_en": threat.mitigation_en,
            "mitigation_zh": threat.mitigation_zh,
        }
    )


@router.get("/attack-patterns", response_model=ResponseModel)
async def list_attack_patterns(
    current_user: CurrentUser,
    db: DbSession,
    search: Optional[str] = None,
):
    """List attack patterns from knowledge base."""
    service = KnowledgeService(db)
    patterns = await service.get_attack_patterns(search=search)

    return ResponseModel(
        data=[
            {
                "id": p.pattern_id,
                "name": p.name,
                "description": p.description,
                "prerequisites": p.prerequisites,
                "attack_steps": p.attack_steps,
                "mitigations": p.mitigations,
                "related_cwe": p.related_cwe,
                "related_capec": p.related_capec,
            }
            for p in patterns
        ]
    )


@router.get("/attack-patterns/{pattern_id}", response_model=ResponseModel)
async def get_attack_pattern(
    pattern_id: str,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get a specific attack pattern by ID."""
    service = KnowledgeService(db)
    pattern = await service.get_attack_pattern_by_id(pattern_id)

    if not pattern:
        return ResponseModel(code=40001, message="Attack pattern not found")

    return ResponseModel(
        data={
            "id": pattern.pattern_id,
            "name": pattern.name,
            "description": pattern.description,
            "prerequisites": pattern.prerequisites,
            "attack_steps": pattern.attack_steps,
            "mitigations": pattern.mitigations,
            "related_cwe": pattern.related_cwe,
            "related_capec": pattern.related_capec,
        }
    )


@router.get("/security-requirements", response_model=ResponseModel)
async def list_security_requirements(
    current_user: CurrentUser,
    db: DbSession,
    category: Optional[str] = None,
    stride_type: Optional[str] = None,
):
    """List security requirement templates."""
    service = KnowledgeService(db)
    reqs = await service.get_security_requirements(
        category=category,
        stride_type=stride_type
    )

    return ResponseModel(
        data=[
            {
                "id": r.id,
                "category": r.category,
                "template": r.requirement_template,
                "description": r.description,
                "stride": r.related_stride,
            }
            for r in reqs
        ]
    )


@router.get("/search", response_model=ResponseModel)
async def search_knowledge(
    current_user: CurrentUser,
    db: DbSession,
    q: str = Query(..., min_length=1),
    type: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50),
):
    """Search across all knowledge bases."""
    service = KnowledgeService(db)
    results = await service.search_knowledge(
        query_text=q,
        knowledge_type=type,
        limit=limit
    )

    return ResponseModel(data=results)


@router.get("/mitigation-suggestions", response_model=ResponseModel)
async def get_mitigation_suggestions(
    current_user: CurrentUser,
    db: DbSession,
    stride_type: str = Query(..., pattern="^[STRIDE]$"),
    threat_description: str = Query(..., min_length=1),
):
    """Get mitigation suggestions for a threat."""
    service = KnowledgeService(db)
    suggestions = await service.get_mitigation_suggestions(
        stride_type=stride_type,
        threat_description=threat_description
    )

    return ResponseModel(data=suggestions)
