"""Asset management API endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.v1.deps import CurrentUser, DbSession
from app.models.asset import Asset, AssetRelation
from app.models.project import Project
from app.schemas.asset import (
    AssetCreate,
    AssetGraphResponse,
    AssetRelationCreate,
    AssetRelationResponse,
    AssetResponse,
    AssetUpdate,
)
from app.schemas.common import PaginatedResponse, ResponseModel

router = APIRouter(prefix="/projects/{project_id}/assets", tags=["Assets"])


@router.get("", response_model=ResponseModel[PaginatedResponse[AssetResponse]])
async def list_assets(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    confirmed: Optional[bool] = None,
):
    """List all assets in a project."""
    query = select(Asset).where(Asset.project_id == project_id)

    if category:
        query = query.where(Asset.category == category)

    if confirmed is not None:
        query = query.where(Asset.is_confirmed == confirmed)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(Asset.asset_id).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    assets = result.scalars().all()

    items = [AssetResponse.model_validate(a) for a in assets]

    return ResponseModel(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )


@router.post("", response_model=ResponseModel[AssetResponse])
async def create_asset(
    project_id: int,
    asset_data: AssetCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create a new asset."""
    # Check project exists
    result = await db.execute(select(Project).where(Project.id == project_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Check if asset_id exists in project
    result = await db.execute(
        select(Asset).where(
            Asset.project_id == project_id,
            Asset.asset_id == asset_data.asset_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset ID already exists in this project",
        )

    asset = Asset(
        project_id=project_id,
        is_ai_generated=False,
        **asset_data.model_dump(),
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)

    return ResponseModel(data=AssetResponse.model_validate(asset))


@router.get("/{asset_id}", response_model=ResponseModel[AssetResponse])
async def get_asset(
    project_id: int,
    asset_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get asset details."""
    result = await db.execute(
        select(Asset).where(
            Asset.id == asset_id,
            Asset.project_id == project_id,
        )
    )
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return ResponseModel(data=AssetResponse.model_validate(asset))


@router.put("/{asset_id}", response_model=ResponseModel[AssetResponse])
async def update_asset(
    project_id: int,
    asset_id: int,
    asset_data: AssetUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update an asset."""
    result = await db.execute(
        select(Asset).where(
            Asset.id == asset_id,
            Asset.project_id == project_id,
        )
    )
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    update_data = asset_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    await db.commit()
    await db.refresh(asset)

    return ResponseModel(data=AssetResponse.model_validate(asset))


@router.delete("/{asset_id}", response_model=ResponseModel)
async def delete_asset(
    project_id: int,
    asset_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete an asset."""
    result = await db.execute(
        select(Asset).where(
            Asset.id == asset_id,
            Asset.project_id == project_id,
        )
    )
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    await db.delete(asset)
    await db.commit()

    return ResponseModel(message="Asset deleted successfully")


@router.post("/{asset_id}/confirm", response_model=ResponseModel)
async def confirm_asset(
    project_id: int,
    asset_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Confirm an AI-generated asset."""
    result = await db.execute(
        select(Asset).where(
            Asset.id == asset_id,
            Asset.project_id == project_id,
        )
    )
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    asset.is_confirmed = True
    await db.commit()

    return ResponseModel(message="Asset confirmed successfully")


@router.get("/graph", response_model=ResponseModel[AssetGraphResponse])
async def get_asset_graph(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get asset relationship graph."""
    # Get all assets
    result = await db.execute(
        select(Asset).where(Asset.project_id == project_id)
    )
    assets = result.scalars().all()

    # Get all relations
    result = await db.execute(
        select(AssetRelation)
        .options(
            selectinload(AssetRelation.source_asset),
            selectinload(AssetRelation.target_asset),
        )
        .where(AssetRelation.project_id == project_id)
    )
    relations = result.scalars().all()

    nodes = [
        {
            "id": str(a.id),
            "name": a.name,
            "category": a.category,
            "subcategory": a.subcategory,
        }
        for a in assets
    ]

    edges = [
        {
            "source": str(r.source_asset_id),
            "target": str(r.target_asset_id),
            "type": r.relation_type,
            "protocol": r.protocol,
        }
        for r in relations
    ]

    return ResponseModel(
        data=AssetGraphResponse(nodes=nodes, edges=edges)
    )


@router.post("/relations", response_model=ResponseModel[AssetRelationResponse])
async def create_asset_relation(
    project_id: int,
    relation_data: AssetRelationCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create an asset relation."""
    relation = AssetRelation(
        project_id=project_id,
        **relation_data.model_dump(),
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)

    # Get asset names
    result = await db.execute(
        select(AssetRelation)
        .options(
            selectinload(AssetRelation.source_asset),
            selectinload(AssetRelation.target_asset),
        )
        .where(AssetRelation.id == relation.id)
    )
    relation = result.scalar_one()

    return ResponseModel(
        data=AssetRelationResponse(
            id=relation.id,
            project_id=relation.project_id,
            source_asset_id=relation.source_asset_id,
            target_asset_id=relation.target_asset_id,
            relation_type=relation.relation_type,
            protocol=relation.protocol,
            description=relation.description,
            source_asset_name=relation.source_asset.name if relation.source_asset else None,
            target_asset_name=relation.target_asset.name if relation.target_asset else None,
        )
    )


@router.post("/identify", response_model=ResponseModel)
async def identify_assets(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    document_id: Optional[int] = None,
):
    """AI-based asset identification from documents."""
    # TODO: Implement AI-based asset identification
    return ResponseModel(
        message="Asset identification started",
        data={"task_id": "placeholder-task-id"}
    )
