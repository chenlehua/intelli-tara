"""Document management API endpoints."""

import os
import uuid
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status

from app.api.v1.deps import CurrentUser, DbSession
from app.core.config import get_settings
from app.models.document import Document
from app.models.project import Project
from app.schemas.common import PaginatedResponse, ResponseModel
from app.schemas.document import DocumentResponse, DocumentUpdate

router = APIRouter(prefix="/projects/{project_id}/documents", tags=["Documents"])

settings = get_settings()


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return os.path.splitext(filename)[1].lower()


def validate_file_type(filename: str) -> bool:
    """Validate if file type is allowed."""
    ext = get_file_extension(filename)
    return ext in settings.ALLOWED_EXTENSIONS


@router.get("", response_model=ResponseModel[PaginatedResponse[DocumentResponse]])
async def list_documents(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
):
    """List all documents in a project."""
    from sqlalchemy import func, select
    from sqlalchemy.orm import selectinload

    query = (
        select(Document)
        .options(selectinload(Document.uploader))
        .where(Document.project_id == project_id)
    )

    if category:
        query = query.where(Document.category == category)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(Document.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    documents = result.scalars().all()

    items = [
        DocumentResponse(
            id=d.id,
            project_id=d.project_id,
            version_id=d.version_id,
            name=d.name,
            original_name=d.original_name,
            file_type=d.file_type,
            file_size=d.file_size,
            category=d.category,
            parse_status=d.parse_status,
            uploaded_by=d.uploaded_by,
            uploader_name=d.uploader.display_name or d.uploader.username if d.uploader else None,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )
        for d in documents
    ]

    return ResponseModel(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )


@router.post("", response_model=ResponseModel[DocumentResponse])
async def upload_document(
    project_id: int,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
    category: str = Form(default="other"),
):
    """Upload a document to a project."""
    from sqlalchemy import select

    # Check project exists
    result = await db.execute(select(Project).where(Project.id == project_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Validate file type
    if not validate_file_type(file.filename or ""):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}",
        )

    # Generate storage path
    file_ext = get_file_extension(file.filename or "")
    storage_name = f"{uuid.uuid4()}{file_ext}"
    storage_path = f"projects/{project_id}/documents/{storage_name}"

    # Read file content
    content = await file.read()
    file_size = len(content)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size ({settings.MAX_UPLOAD_SIZE} bytes)",
        )

    # TODO: Upload to MinIO storage
    # For now, save to local filesystem
    local_dir = f"/tmp/tara-documents/projects/{project_id}/documents"
    os.makedirs(local_dir, exist_ok=True)
    with open(f"/tmp/tara-documents/{storage_path}", "wb") as f:
        f.write(content)

    # Create document record
    document = Document(
        project_id=project_id,
        name=file.filename or storage_name,
        original_name=file.filename or storage_name,
        file_type=file_ext.lstrip("."),
        file_size=file_size,
        storage_path=storage_path,
        category=category,
        parse_status="pending",
        uploaded_by=current_user.id,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    return ResponseModel(
        data=DocumentResponse(
            id=document.id,
            project_id=document.project_id,
            version_id=document.version_id,
            name=document.name,
            original_name=document.original_name,
            file_type=document.file_type,
            file_size=document.file_size,
            category=document.category,
            parse_status=document.parse_status,
            uploaded_by=document.uploaded_by,
            created_at=document.created_at,
        )
    )


@router.delete("/{document_id}", response_model=ResponseModel)
async def delete_document(
    project_id: int,
    document_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete a document."""
    from sqlalchemy import select

    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.project_id == project_id,
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # TODO: Delete from MinIO storage
    # For now, delete from local filesystem
    try:
        local_path = f"/tmp/tara-documents/{document.storage_path}"
        if os.path.exists(local_path):
            os.remove(local_path)
    except Exception:
        pass

    await db.delete(document)
    await db.commit()

    return ResponseModel(message="Document deleted successfully")


@router.post("/{document_id}/parse", response_model=ResponseModel)
async def parse_document(
    project_id: int,
    document_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Parse a document to extract content."""
    from sqlalchemy import select

    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.project_id == project_id,
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Update status to parsing
    document.parse_status = "parsing"
    await db.commit()

    # TODO: Trigger async parsing task
    # For now, just mark as completed
    document.parse_status = "completed"
    document.parse_result = {
        "text_blocks": ["Document content will be parsed here"],
        "tables": [],
        "images": [],
        "metadata": {"pages": 1},
    }
    await db.commit()

    return ResponseModel(message="Document parsing started")


@router.get("/{document_id}/parse-result", response_model=ResponseModel)
async def get_parse_result(
    project_id: int,
    document_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get document parse result."""
    from sqlalchemy import select

    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.project_id == project_id,
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return ResponseModel(
        data={
            "document_id": document.id,
            "status": document.parse_status,
            "result": document.parse_result,
            "error": document.parse_error,
        }
    )
