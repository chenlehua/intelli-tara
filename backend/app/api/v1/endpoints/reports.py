"""Report generation API endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.v1.deps import CurrentUser, DbSession
from app.models.project import Project
from app.models.report import Report
from app.schemas.common import PaginatedResponse, ResponseModel
from app.schemas.report import ReportGenerateRequest, ReportResponse

router = APIRouter(prefix="/projects/{project_id}/reports", tags=["Reports"])


@router.get("", response_model=ResponseModel[PaginatedResponse[ReportResponse]])
async def list_reports(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all reports in a project."""
    query = (
        select(Report)
        .options(selectinload(Report.generator))
        .where(Report.project_id == project_id)
    )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(Report.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    reports = result.scalars().all()

    items = [
        ReportResponse(
            id=r.id,
            project_id=r.project_id,
            version_id=r.version_id,
            report_number=r.report_number,
            title=r.title,
            report_version=r.report_version,
            status=r.status,
            storage_path=r.storage_path,
            file_size=r.file_size,
            generated_by=r.generated_by,
            generator_name=r.generator.display_name or r.generator.username if r.generator else None,
            author=r.author,
            reviewer=r.reviewer,
            approver=r.approver,
            error_message=r.error_message,
            created_at=r.created_at,
        )
        for r in reports
    ]

    return ResponseModel(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )


@router.post("/generate", response_model=ResponseModel[ReportResponse])
async def generate_report(
    project_id: int,
    request: ReportGenerateRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    """Generate a TARA report."""
    # Check project exists
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Create report record
    report = Report(
        project_id=project_id,
        version_id=request.version_id,
        title=request.title or f"{project.name} TARA Report",
        report_version=request.report_version or "1.0",
        status="generating",
        generated_by=current_user.id,
        author=request.author,
        reviewer=request.reviewer,
        approver=request.approver,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    # TODO: Trigger async report generation task
    # For now, just mark as completed with placeholder
    report.status = "completed"
    report.storage_path = f"projects/{project_id}/reports/report_{report.id}.xlsx"
    await db.commit()

    return ResponseModel(
        data=ReportResponse(
            id=report.id,
            project_id=report.project_id,
            version_id=report.version_id,
            report_number=report.report_number,
            title=report.title,
            report_version=report.report_version,
            status=report.status,
            storage_path=report.storage_path,
            file_size=report.file_size,
            generated_by=report.generated_by,
            generator_name=current_user.display_name or current_user.username,
            author=report.author,
            reviewer=report.reviewer,
            approver=report.approver,
            created_at=report.created_at,
        )
    )


@router.get("/{report_id}", response_model=ResponseModel[ReportResponse])
async def get_report(
    project_id: int,
    report_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get report details."""
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.generator))
        .where(
            Report.id == report_id,
            Report.project_id == project_id,
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    return ResponseModel(
        data=ReportResponse(
            id=report.id,
            project_id=report.project_id,
            version_id=report.version_id,
            report_number=report.report_number,
            title=report.title,
            report_version=report.report_version,
            status=report.status,
            storage_path=report.storage_path,
            file_size=report.file_size,
            generated_by=report.generated_by,
            generator_name=report.generator.display_name or report.generator.username if report.generator else None,
            author=report.author,
            reviewer=report.reviewer,
            approver=report.approver,
            error_message=report.error_message,
            created_at=report.created_at,
        )
    )


@router.get("/{report_id}/download")
async def download_report(
    project_id: int,
    report_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Download a report file."""
    result = await db.execute(
        select(Report).where(
            Report.id == report_id,
            Report.project_id == project_id,
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.status != "completed" or not report.storage_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report is not ready for download",
        )

    # TODO: Get file from MinIO
    # For now, return placeholder
    file_path = f"/tmp/tara-documents/{report.storage_path}"

    import os
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found",
        )

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{report.title}.xlsx",
    )


@router.delete("/{report_id}", response_model=ResponseModel)
async def delete_report(
    project_id: int,
    report_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete a report."""
    result = await db.execute(
        select(Report).where(
            Report.id == report_id,
            Report.project_id == project_id,
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    # TODO: Delete file from storage

    await db.delete(report)
    await db.commit()

    return ResponseModel(message="Report deleted successfully")
