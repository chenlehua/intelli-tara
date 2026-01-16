"""Project management API endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.v1.deps import CurrentUser, DbSession
from app.models.project import Project, ProjectConfig, ProjectMember, ProjectVersion
from app.models.asset import Asset
from app.models.threat import ThreatScenario
from app.models.report import Report
from app.schemas.common import PaginatedResponse, ResponseModel
from app.schemas.project import (
    ProjectConfigUpdate,
    ProjectCreate,
    ProjectListResponse,
    ProjectMemberAdd,
    ProjectMemberResponse,
    ProjectResponse,
    ProjectStatsResponse,
    ProjectUpdate,
    ProjectVersionCreate,
    ProjectVersionResponse,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=ResponseModel[PaginatedResponse[ProjectListResponse]])
async def list_projects(
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    """List all projects accessible by the current user."""
    query = (
        select(Project)
        .options(selectinload(Project.owner))
        .where(
            (Project.owner_id == current_user.id) |
            (Project.members.any(ProjectMember.user_id == current_user.id))
        )
    )

    if status:
        query = query.where(Project.status == status)

    if search:
        query = query.where(Project.name.contains(search))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(Project.updated_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    projects = result.scalars().all()

    items = [
        ProjectListResponse(
            id=p.id,
            name=p.name,
            code=p.code,
            status=p.status,
            owner_name=p.owner.display_name or p.owner.username if p.owner else None,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in projects
    ]

    return ResponseModel(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )


@router.post("", response_model=ResponseModel[ProjectResponse])
async def create_project(
    project_data: ProjectCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create a new project."""
    # Check if project code exists
    if project_data.code:
        result = await db.execute(select(Project).where(Project.code == project_data.code))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project code already exists",
            )

    project = Project(
        name=project_data.name,
        code=project_data.code,
        description=project_data.description,
        owner_id=current_user.id,
        status="draft",
    )
    db.add(project)
    await db.flush()

    # Create default config
    config = ProjectConfig(project_id=project.id)
    db.add(config)

    # Add owner as project member
    member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role="owner",
    )
    db.add(member)

    await db.commit()
    await db.refresh(project)

    return ResponseModel(
        data=ProjectResponse(
            id=project.id,
            name=project.name,
            code=project.code,
            description=project.description,
            status=project.status,
            owner_id=project.owner_id,
            owner_name=current_user.display_name or current_user.username,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
    )


@router.get("/stats", response_model=ResponseModel[ProjectStatsResponse])
async def get_project_stats(
    current_user: CurrentUser,
    db: DbSession,
):
    """Get project statistics for the current user."""
    # Count projects
    project_count = (await db.execute(
        select(func.count(Project.id)).where(
            (Project.owner_id == current_user.id) |
            (Project.members.any(ProjectMember.user_id == current_user.id))
        )
    )).scalar() or 0

    # Count assets
    asset_count = (await db.execute(
        select(func.count(Asset.id))
        .join(Project)
        .where(
            (Project.owner_id == current_user.id) |
            (Project.members.any(ProjectMember.user_id == current_user.id))
        )
    )).scalar() or 0

    # Count threats
    threat_count = (await db.execute(
        select(func.count(ThreatScenario.id))
        .join(Project)
        .where(
            (Project.owner_id == current_user.id) |
            (Project.members.any(ProjectMember.user_id == current_user.id))
        )
    )).scalar() or 0

    # Count high risk threats (risk_level >= 4)
    high_risk_count = (await db.execute(
        select(func.count(ThreatScenario.id))
        .join(Project)
        .where(
            (Project.owner_id == current_user.id) |
            (Project.members.any(ProjectMember.user_id == current_user.id))
        )
        .where(ThreatScenario.risk_level >= 4)
    )).scalar() or 0

    return ResponseModel(
        data=ProjectStatsResponse(
            project_count=project_count,
            asset_count=asset_count,
            threat_count=threat_count,
            high_risk_count=high_risk_count,
        )
    )


@router.get("/{project_id}", response_model=ResponseModel[ProjectResponse])
async def get_project(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get project details."""
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.owner))
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Check access
    if project.owner_id != current_user.id:
        member_check = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id,
            )
        )
        if not member_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

    # Count related entities
    asset_count = (await db.execute(
        select(func.count(Asset.id)).where(Asset.project_id == project_id)
    )).scalar() or 0

    threat_count = (await db.execute(
        select(func.count(ThreatScenario.id)).where(ThreatScenario.project_id == project_id)
    )).scalar() or 0

    report_count = (await db.execute(
        select(func.count(Report.id)).where(Report.project_id == project_id)
    )).scalar() or 0

    return ResponseModel(
        data=ProjectResponse(
            id=project.id,
            name=project.name,
            code=project.code,
            description=project.description,
            status=project.status,
            owner_id=project.owner_id,
            owner_name=project.owner.display_name or project.owner.username if project.owner else None,
            created_at=project.created_at,
            updated_at=project.updated_at,
            asset_count=asset_count,
            threat_count=threat_count,
            report_count=report_count,
        )
    )


@router.put("/{project_id}", response_model=ResponseModel[ProjectResponse])
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update project details."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Check if user is owner or admin
    if project.owner_id != current_user.id:
        member_check = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id,
                ProjectMember.role.in_(["owner", "admin"]),
            )
        )
        if not member_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

    # Update fields
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    return ResponseModel(
        data=ProjectResponse(
            id=project.id,
            name=project.name,
            code=project.code,
            description=project.description,
            status=project.status,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
    )


@router.delete("/{project_id}", response_model=ResponseModel)
async def delete_project(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete a project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can delete the project",
        )

    await db.delete(project)
    await db.commit()

    return ResponseModel(message="Project deleted successfully")


@router.put("/{project_id}/config", response_model=ResponseModel)
async def update_project_config(
    project_id: int,
    config_data: ProjectConfigUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update project configuration."""
    result = await db.execute(
        select(ProjectConfig).where(ProjectConfig.project_id == project_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project config not found",
        )

    update_data = config_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)

    await db.commit()

    return ResponseModel(message="Project config updated successfully")


@router.post("/{project_id}/versions", response_model=ResponseModel[ProjectVersionResponse])
async def create_version(
    project_id: int,
    version_data: ProjectVersionCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create a new project version."""
    # Check if version exists
    result = await db.execute(
        select(ProjectVersion).where(
            ProjectVersion.project_id == project_id,
            ProjectVersion.version == version_data.version,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Version already exists",
        )

    version = ProjectVersion(
        project_id=project_id,
        version=version_data.version,
        description=version_data.description,
        created_by=current_user.id,
        status="active",
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)

    return ResponseModel(
        data=ProjectVersionResponse(
            id=version.id,
            project_id=version.project_id,
            version=version.version,
            description=version.description,
            status=version.status,
            created_by=version.created_by,
            created_at=version.created_at,
        )
    )


@router.get("/{project_id}/versions", response_model=ResponseModel[list[ProjectVersionResponse]])
async def list_versions(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """List all versions of a project."""
    result = await db.execute(
        select(ProjectVersion)
        .where(ProjectVersion.project_id == project_id)
        .order_by(ProjectVersion.created_at.desc())
    )
    versions = result.scalars().all()

    return ResponseModel(
        data=[
            ProjectVersionResponse(
                id=v.id,
                project_id=v.project_id,
                version=v.version,
                description=v.description,
                status=v.status,
                created_by=v.created_by,
                created_at=v.created_at,
            )
            for v in versions
        ]
    )


@router.get("/{project_id}/members", response_model=ResponseModel[list[ProjectMemberResponse]])
async def list_members(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """List all members of a project."""
    result = await db.execute(
        select(ProjectMember)
        .options(selectinload(ProjectMember.user))
        .where(ProjectMember.project_id == project_id)
    )
    members = result.scalars().all()

    return ResponseModel(
        data=[
            ProjectMemberResponse(
                user_id=m.user_id,
                username=m.user.username,
                display_name=m.user.display_name,
                role=m.role,
                joined_at=m.joined_at,
            )
            for m in members
        ]
    )


@router.post("/{project_id}/members", response_model=ResponseModel)
async def add_member(
    project_id: int,
    member_data: ProjectMemberAdd,
    current_user: CurrentUser,
    db: DbSession,
):
    """Add a member to the project."""
    # Check if already a member
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == member_data.user_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member",
        )

    member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role=member_data.role,
    )
    db.add(member)
    await db.commit()

    return ResponseModel(message="Member added successfully")
