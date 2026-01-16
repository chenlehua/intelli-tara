"""Authentication API endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.v1.deps import CurrentUser, DbSession
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User, Role
from app.schemas.common import ResponseModel, Token
from app.schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=ResponseModel[dict])
async def login(
    login_data: UserLogin,
    db: DbSession
):
    """User login endpoint."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.username == login_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active",
        )

    # Update last login time
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    # Generate tokens
    token_data = {"sub": str(user.id), "username": user.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return ResponseModel(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                display_name=user.display_name,
                avatar_url=user.avatar_url,
                status=user.status,
                roles=[role.name for role in user.roles],
                created_at=user.created_at,
                last_login_at=user.last_login_at,
            ).model_dump()
        }
    )


@router.post("/register", response_model=ResponseModel[UserResponse])
async def register(
    user_data: UserCreate,
    db: DbSession
):
    """User registration endpoint."""
    # Check if username exists
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Get default role
    result = await db.execute(select(Role).where(Role.name == "viewer"))
    default_role = result.scalar_one_or_none()

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        display_name=user_data.display_name,
        status="active",
    )
    if default_role:
        user.roles.append(default_role)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return ResponseModel(
        data=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            status=user.status,
            roles=[role.name for role in user.roles] if user.roles else [],
            created_at=user.created_at,
        )
    )


@router.post("/refresh", response_model=ResponseModel[Token])
async def refresh_token(
    refresh_token: str,
    db: DbSession
):
    """Refresh access token using refresh token."""
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Generate new tokens
    token_data = {"sub": str(user.id), "username": user.username}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return ResponseModel(
        data=Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
    )


@router.post("/logout", response_model=ResponseModel)
async def logout(current_user: CurrentUser):
    """User logout endpoint."""
    # In a production environment, you would add the token to a blacklist
    return ResponseModel(message="Logged out successfully")


@router.get("/profile", response_model=ResponseModel[UserResponse])
async def get_profile(
    current_user: CurrentUser,
    db: DbSession
):
    """Get current user profile."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == current_user.id)
    )
    user = result.scalar_one()

    return ResponseModel(
        data=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            status=user.status,
            roles=[role.name for role in user.roles],
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
    )
