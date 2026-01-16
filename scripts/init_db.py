#!/usr/bin/env python3
"""Database initialization script.

Creates default roles, permissions, and admin user.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import async_session_factory, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, Role, Permission, UserRole, RolePermission


# Default permissions
DEFAULT_PERMISSIONS = [
    ("project:create", "创建项目", "project", "create"),
    ("project:read", "查看项目", "project", "read"),
    ("project:update", "更新项目", "project", "update"),
    ("project:delete", "删除项目", "project", "delete"),
    ("document:upload", "上传文档", "document", "upload"),
    ("document:read", "查看文档", "document", "read"),
    ("document:delete", "删除文档", "document", "delete"),
    ("asset:create", "创建资产", "asset", "create"),
    ("asset:read", "查看资产", "asset", "read"),
    ("asset:update", "更新资产", "asset", "update"),
    ("asset:delete", "删除资产", "asset", "delete"),
    ("threat:create", "创建威胁", "threat", "create"),
    ("threat:read", "查看威胁", "threat", "read"),
    ("threat:update", "更新威胁", "threat", "update"),
    ("threat:delete", "删除威胁", "threat", "delete"),
    ("report:generate", "生成报告", "report", "generate"),
    ("report:read", "查看报告", "report", "read"),
    ("report:download", "下载报告", "report", "download"),
    ("system:manage", "系统管理", "system", "manage"),
]

# Default roles
DEFAULT_ROLES = {
    "admin": {
        "description": "系统管理员",
        "permissions": ["*"],  # All permissions
    },
    "analyst": {
        "description": "安全分析师",
        "permissions": [
            "project:create", "project:read", "project:update",
            "document:upload", "document:read", "document:delete",
            "asset:create", "asset:read", "asset:update", "asset:delete",
            "threat:create", "threat:read", "threat:update", "threat:delete",
            "report:generate", "report:read", "report:download",
        ],
    },
    "reviewer": {
        "description": "评审人员",
        "permissions": [
            "project:read",
            "document:read",
            "asset:read",
            "threat:read",
            "report:read", "report:download",
        ],
    },
    "viewer": {
        "description": "只读用户",
        "permissions": [
            "project:read",
            "document:read",
            "asset:read",
            "threat:read",
        ],
    },
}


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")


async def init_permissions(session):
    """Initialize default permissions."""
    for code, name, resource, action in DEFAULT_PERMISSIONS:
        result = await session.execute(
            select(Permission).where(Permission.code == code)
        )
        if not result.scalar_one_or_none():
            permission = Permission(
                code=code,
                name=name,
                resource=resource,
                action=action,
            )
            session.add(permission)
    await session.commit()
    print("Permissions initialized.")


async def init_roles(session):
    """Initialize default roles."""
    # Get all permissions
    result = await session.execute(select(Permission))
    all_permissions = {p.code: p for p in result.scalars().all()}

    for role_name, role_config in DEFAULT_ROLES.items():
        # Query with eager loading of permissions
        result = await session.execute(
            select(Role).where(Role.name == role_name).options(selectinload(Role.permissions))
        )
        role = result.scalar_one_or_none()

        if not role:
            role = Role(
                name=role_name,
                description=role_config["description"],
            )
            session.add(role)
            await session.flush()
            # Refresh to get the role with empty permissions list
            await session.refresh(role, ['permissions'])

        # Assign permissions
        for perm_code in role_config["permissions"]:
            if perm_code == "*":
                role.permissions = list(all_permissions.values())
            elif perm_code in all_permissions:
                if all_permissions[perm_code] not in role.permissions:
                    role.permissions.append(all_permissions[perm_code])

    await session.commit()
    print("Roles initialized.")


async def init_admin_user(session):
    """Initialize default admin user."""
    result = await session.execute(
        select(User).where(User.username == "admin").options(selectinload(User.roles))
    )
    admin = result.scalar_one_or_none()

    if not admin:
        # Get admin role
        result = await session.execute(
            select(Role).where(Role.name == "admin")
        )
        admin_role = result.scalar_one()

        admin = User(
            username="admin",
            email="admin@intelli-tara.local",
            password_hash=get_password_hash("admin123"),
            display_name="系统管理员",
            status="active",
        )
        session.add(admin)
        await session.flush()
        await session.refresh(admin, ['roles'])
        admin.roles.append(admin_role)
        await session.commit()
        print("Admin user created (username: admin, password: admin123)")
    else:
        print("Admin user already exists.")


async def main():
    """Main initialization function."""
    print("Initializing database...")

    # Create tables
    await create_tables()

    # Initialize data
    async with async_session_factory() as session:
        await init_permissions(session)
        await init_roles(session)
        await init_admin_user(session)

    print("Database initialization completed.")


if __name__ == "__main__":
    asyncio.run(main())
