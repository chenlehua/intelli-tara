"""FastAPI application entry point."""

import time
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import BaseAPIException
from app.core.middleware import SecurityHeadersMiddleware, RequestLoggingMiddleware

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# OpenAPI schema customization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
## Intelli-TARA API

智能威胁分析与风险评估平台 API 文档。

### 主要功能
- **项目管理**: 创建和管理 TARA 分析项目
- **文档解析**: 上传和解析技术文档
- **资产识别**: AI 驱动的资产自动识别
- **威胁分析**: 基于 STRIDE 模型的威胁分析
- **风险评估**: ISO 21434 标准的风险评估
- **报告生成**: 自动生成 TARA 分析报告

### 认证方式
使用 Bearer Token 认证，通过 `/api/v1/auth/login` 获取 token。

### 标准遵循
- ISO/SAE 21434:2021
- UN R155
- WP.29 Cybersecurity Requirements
        """,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add tags
    openapi_schema["tags"] = [
        {"name": "auth", "description": "用户认证相关接口"},
        {"name": "projects", "description": "项目管理相关接口"},
        {"name": "documents", "description": "文档管理相关接口"},
        {"name": "assets", "description": "资产管理相关接口"},
        {"name": "threats", "description": "威胁分析相关接口"},
        {"name": "reports", "description": "报告生成相关接口"},
        {"name": "knowledge", "description": "知识库相关接口"},
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent Threat Analysis and Risk Assessment Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Custom OpenAPI schema
app.openapi = custom_openapi

# Add middleware (order matters - last added is first executed)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=200,  # Always return 200 for business errors
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
            "timestamp": int(time.time() * 1000),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "code": 10001,
            "message": str(exc) if settings.DEBUG else "Internal server error",
            "data": None,
            "timestamp": int(time.time() * 1000),
        },
    )


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Welcome to Intelli-TARA API",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
