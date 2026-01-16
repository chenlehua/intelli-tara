"""Threat analysis API endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.v1.deps import CurrentUser, DbSession
from app.models.asset import Asset
from app.models.threat import SecurityMitigation, ThreatScenario
from app.schemas.common import PaginatedResponse, ResponseModel
from app.schemas.threat import (
    MitigationCreate,
    MitigationResponse,
    MitigationUpdate,
    RiskMatrixResponse,
    ThreatCreate,
    ThreatResponse,
    ThreatUpdate,
)
from app.services.risk_calculator import RiskCalculator

router = APIRouter(prefix="/projects/{project_id}/threats", tags=["Threats"])


@router.get("", response_model=ResponseModel[PaginatedResponse[ThreatResponse]])
async def list_threats(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    asset_id: Optional[int] = None,
    stride_type: Optional[str] = None,
    risk_level: Optional[int] = None,
    confirmed: Optional[bool] = None,
):
    """List all threats in a project."""
    query = (
        select(ThreatScenario)
        .options(
            selectinload(ThreatScenario.asset),
            selectinload(ThreatScenario.mitigations),
        )
        .where(ThreatScenario.project_id == project_id)
    )

    if asset_id:
        query = query.where(ThreatScenario.asset_id == asset_id)

    if stride_type:
        query = query.where(ThreatScenario.stride_type == stride_type)

    if risk_level is not None:
        query = query.where(ThreatScenario.risk_level == risk_level)

    if confirmed is not None:
        query = query.where(ThreatScenario.is_confirmed == confirmed)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(ThreatScenario.threat_id).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    threats = result.scalars().all()

    items = [
        ThreatResponse(
            id=t.id,
            project_id=t.project_id,
            version_id=t.version_id,
            asset_id=t.asset_id,
            asset_name=t.asset.name if t.asset else None,
            threat_id=t.threat_id,
            security_attribute=t.security_attribute,
            stride_type=t.stride_type,
            threat_description=t.threat_description,
            damage_scenario=t.damage_scenario,
            attack_path=t.attack_path,
            source_reference=t.source_reference,
            wp29_mapping=t.wp29_mapping,
            attack_vector=t.attack_vector,
            attack_complexity=t.attack_complexity,
            privileges_required=t.privileges_required,
            user_interaction=t.user_interaction,
            attack_feasibility=t.attack_feasibility,
            attack_feasibility_value=t.attack_feasibility_value,
            impact_safety=t.impact_safety,
            impact_financial=t.impact_financial,
            impact_operational=t.impact_operational,
            impact_privacy=t.impact_privacy,
            impact_level=t.impact_level,
            impact_level_value=t.impact_level_value,
            risk_level=t.risk_level,
            risk_level_label=t.risk_level_label,
            treatment_decision=t.treatment_decision,
            is_ai_generated=t.is_ai_generated,
            is_confirmed=t.is_confirmed,
            created_at=t.created_at,
            updated_at=t.updated_at,
            mitigations=[MitigationResponse.model_validate(m) for m in t.mitigations],
        )
        for t in threats
    ]

    return ResponseModel(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )


@router.post("", response_model=ResponseModel[ThreatResponse])
async def create_threat(
    project_id: int,
    threat_data: ThreatCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create a new threat."""
    # Check asset exists
    result = await db.execute(
        select(Asset).where(
            Asset.id == threat_data.asset_id,
            Asset.project_id == project_id,
        )
    )
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    threat = ThreatScenario(
        project_id=project_id,
        is_ai_generated=False,
        **threat_data.model_dump(),
    )

    # Calculate risk
    threat = RiskCalculator.calculate_and_update_threat(threat)

    db.add(threat)
    await db.commit()
    await db.refresh(threat)

    return ResponseModel(
        data=ThreatResponse(
            id=threat.id,
            project_id=threat.project_id,
            asset_id=threat.asset_id,
            asset_name=asset.name,
            threat_id=threat.threat_id,
            security_attribute=threat.security_attribute,
            stride_type=threat.stride_type,
            threat_description=threat.threat_description,
            damage_scenario=threat.damage_scenario,
            attack_path=threat.attack_path,
            attack_vector=threat.attack_vector,
            attack_complexity=threat.attack_complexity,
            privileges_required=threat.privileges_required,
            user_interaction=threat.user_interaction,
            attack_feasibility=threat.attack_feasibility,
            attack_feasibility_value=threat.attack_feasibility_value,
            impact_safety=threat.impact_safety,
            impact_financial=threat.impact_financial,
            impact_operational=threat.impact_operational,
            impact_privacy=threat.impact_privacy,
            impact_level=threat.impact_level,
            impact_level_value=threat.impact_level_value,
            risk_level=threat.risk_level,
            risk_level_label=threat.risk_level_label,
            treatment_decision=threat.treatment_decision,
            is_ai_generated=threat.is_ai_generated,
            is_confirmed=threat.is_confirmed,
            created_at=threat.created_at,
            mitigations=[],
        )
    )


@router.get("/{threat_id}", response_model=ResponseModel[ThreatResponse])
async def get_threat(
    project_id: int,
    threat_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get threat details."""
    result = await db.execute(
        select(ThreatScenario)
        .options(
            selectinload(ThreatScenario.asset),
            selectinload(ThreatScenario.mitigations),
        )
        .where(
            ThreatScenario.id == threat_id,
            ThreatScenario.project_id == project_id,
        )
    )
    threat = result.scalar_one_or_none()

    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found",
        )

    return ResponseModel(
        data=ThreatResponse(
            id=threat.id,
            project_id=threat.project_id,
            asset_id=threat.asset_id,
            asset_name=threat.asset.name if threat.asset else None,
            threat_id=threat.threat_id,
            security_attribute=threat.security_attribute,
            stride_type=threat.stride_type,
            threat_description=threat.threat_description,
            damage_scenario=threat.damage_scenario,
            attack_path=threat.attack_path,
            source_reference=threat.source_reference,
            wp29_mapping=threat.wp29_mapping,
            attack_vector=threat.attack_vector,
            attack_complexity=threat.attack_complexity,
            privileges_required=threat.privileges_required,
            user_interaction=threat.user_interaction,
            attack_feasibility=threat.attack_feasibility,
            attack_feasibility_value=threat.attack_feasibility_value,
            impact_safety=threat.impact_safety,
            impact_financial=threat.impact_financial,
            impact_operational=threat.impact_operational,
            impact_privacy=threat.impact_privacy,
            impact_level=threat.impact_level,
            impact_level_value=threat.impact_level_value,
            risk_level=threat.risk_level,
            risk_level_label=threat.risk_level_label,
            treatment_decision=threat.treatment_decision,
            is_ai_generated=threat.is_ai_generated,
            is_confirmed=threat.is_confirmed,
            created_at=threat.created_at,
            updated_at=threat.updated_at,
            mitigations=[MitigationResponse.model_validate(m) for m in threat.mitigations],
        )
    )


@router.put("/{threat_id}", response_model=ResponseModel[ThreatResponse])
async def update_threat(
    project_id: int,
    threat_id: int,
    threat_data: ThreatUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update a threat."""
    result = await db.execute(
        select(ThreatScenario)
        .options(selectinload(ThreatScenario.asset))
        .where(
            ThreatScenario.id == threat_id,
            ThreatScenario.project_id == project_id,
        )
    )
    threat = result.scalar_one_or_none()

    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found",
        )

    update_data = threat_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(threat, field, value)

    # Recalculate risk
    threat = RiskCalculator.calculate_and_update_threat(threat)

    await db.commit()
    await db.refresh(threat)

    return ResponseModel(
        data=ThreatResponse(
            id=threat.id,
            project_id=threat.project_id,
            asset_id=threat.asset_id,
            asset_name=threat.asset.name if threat.asset else None,
            threat_id=threat.threat_id,
            security_attribute=threat.security_attribute,
            stride_type=threat.stride_type,
            threat_description=threat.threat_description,
            damage_scenario=threat.damage_scenario,
            attack_path=threat.attack_path,
            attack_vector=threat.attack_vector,
            attack_complexity=threat.attack_complexity,
            privileges_required=threat.privileges_required,
            user_interaction=threat.user_interaction,
            attack_feasibility=threat.attack_feasibility,
            attack_feasibility_value=threat.attack_feasibility_value,
            impact_safety=threat.impact_safety,
            impact_financial=threat.impact_financial,
            impact_operational=threat.impact_operational,
            impact_privacy=threat.impact_privacy,
            impact_level=threat.impact_level,
            impact_level_value=threat.impact_level_value,
            risk_level=threat.risk_level,
            risk_level_label=threat.risk_level_label,
            treatment_decision=threat.treatment_decision,
            is_ai_generated=threat.is_ai_generated,
            is_confirmed=threat.is_confirmed,
            created_at=threat.created_at,
            updated_at=threat.updated_at,
            mitigations=[],
        )
    )


@router.delete("/{threat_id}", response_model=ResponseModel)
async def delete_threat(
    project_id: int,
    threat_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete a threat."""
    result = await db.execute(
        select(ThreatScenario).where(
            ThreatScenario.id == threat_id,
            ThreatScenario.project_id == project_id,
        )
    )
    threat = result.scalar_one_or_none()

    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found",
        )

    await db.delete(threat)
    await db.commit()

    return ResponseModel(message="Threat deleted successfully")


@router.post("/{threat_id}/mitigations", response_model=ResponseModel[MitigationResponse])
async def add_mitigation(
    project_id: int,
    threat_id: int,
    mitigation_data: MitigationCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Add a mitigation to a threat."""
    result = await db.execute(
        select(ThreatScenario).where(
            ThreatScenario.id == threat_id,
            ThreatScenario.project_id == project_id,
        )
    )
    threat = result.scalar_one_or_none()

    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found",
        )

    mitigation = SecurityMitigation(
        threat_id=threat_id,
        **mitigation_data.model_dump(),
    )
    db.add(mitigation)
    await db.commit()
    await db.refresh(mitigation)

    return ResponseModel(data=MitigationResponse.model_validate(mitigation))


@router.get("/risk-matrix", response_model=ResponseModel[RiskMatrixResponse])
async def get_risk_matrix(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get risk matrix for the project."""
    result = await db.execute(
        select(ThreatScenario).where(ThreatScenario.project_id == project_id)
    )
    threats = result.scalars().all()

    # Initialize 4x4 matrix (feasibility x impact)
    matrix = [[0] * 4 for _ in range(4)]
    threat_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for t in threats:
        if t.attack_feasibility_value is not None and t.impact_level_value is not None:
            feas_idx = min(t.attack_feasibility_value, 3)
            impact_idx = min(t.impact_level_value, 3)
            matrix[feas_idx][impact_idx] += 1

        if t.risk_level:
            if t.risk_level in threat_counts:
                threat_counts[t.risk_level] += 1

    high_risk_count = threat_counts.get(4, 0) + threat_counts.get(5, 0)

    return ResponseModel(
        data=RiskMatrixResponse(
            matrix=matrix,
            threat_counts=threat_counts,
            total_threats=len(threats),
            high_risk_count=high_risk_count,
        )
    )


@router.post("/analyze", response_model=ResponseModel)
async def analyze_threats(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    asset_id: Optional[int] = None,
):
    """AI-based threat analysis for assets."""
    # TODO: Implement AI-based threat analysis
    return ResponseModel(
        message="Threat analysis started",
        data={"task_id": "placeholder-task-id"}
    )
