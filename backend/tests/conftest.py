"""
Pytest configuration and fixtures for testing.
"""
import asyncio
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import sys
sys.path.insert(0, '.')

from main import app
from app.core.database import get_db, Base
from app.core.security import get_password_hash, create_access_token


# Test database URL - using SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "display_name": "Test User",
    }


@pytest.fixture
def auth_headers(test_user_data):
    """Authentication headers for test requests."""
    token = create_access_token({"sub": test_user_data["username"], "user_id": 1})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_project_data():
    """Test project data."""
    return {
        "name": "Test Project",
        "code": "TP-001",
        "description": "A test project for TARA analysis",
    }


@pytest.fixture
def test_asset_data():
    """Test asset data."""
    return {
        "asset_id": "AST-001",
        "name": "Test ECU",
        "category": "hardware",
        "subcategory": "ECU",
        "description": "Test Electronic Control Unit",
        "authenticity": True,
        "integrity": True,
        "confidentiality": True,
        "availability": True,
    }


@pytest.fixture
def test_threat_data():
    """Test threat data."""
    return {
        "threat_id": "THR-001",
        "security_attribute": "Confidentiality",
        "stride_type": "I",
        "threat_description": "Unauthorized access to ECU data",
        "damage_scenario": "Attacker gains access to sensitive vehicle data",
        "attack_path": "Network -> ECU -> Data extraction",
        "attack_vector": "Network",
        "attack_complexity": "Low",
        "privileges_required": "None",
        "user_interaction": "None",
        "impact_safety": "None",
        "impact_financial": "Moderate",
        "impact_operational": "Low",
        "impact_privacy": "High",
    }
