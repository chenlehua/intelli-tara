# Intelli-TARA 实现计划

**版本**: 1.0
**日期**: 2026-01-16
**基于文档**: 0001-spec.md

---

## 目录

1. [概述](#1-概述)
2. [实现阶段划分](#2-实现阶段划分)
3. [第一阶段：项目初始化与基础设施](#3-第一阶段项目初始化与基础设施)
4. [第二阶段：核心后端服务](#4-第二阶段核心后端服务)
5. [第三阶段：AI智能体与知识库](#5-第三阶段ai智能体与知识库)
6. [第四阶段：前端应用开发](#6-第四阶段前端应用开发)
7. [第五阶段：系统集成与优化](#7-第五阶段系统集成与优化)
8. [技术栈详细说明](#8-技术栈详细说明)
9. [开发规范](#9-开发规范)

---

## 1. 概述

### 1.1 实现目标

基于需求规格说明书(0001-spec.md)，实现Intelli-TARA智能威胁分析与风险评估平台。本计划采用分阶段迭代开发方式，优先实现P0核心功能，逐步扩展P1/P2功能。

### 1.2 技术栈总览

| 层次 | 技术选型 |
|-----|---------|
| 前端 | Vite + React + TypeScript + TailwindCSS + Zustand |
| 后端 | FastAPI + Python 3.12 + SQLAlchemy + Pydantic |
| 数据库 | MySQL 8.0 + Neo4j 5 + Milvus + Elasticsearch |
| 缓存/队列 | Redis 7 + Kafka |
| 存储 | MinIO |
| AI服务 | 阿里云百炼 Qwen API |
| 部署 | Docker + Docker Compose |

### 1.3 优先级说明

- **P0**: 核心必需功能，必须在第一版本完成
- **P1**: 重要功能，应在后续迭代中完成
- **P2**: 增强功能，根据资源情况安排

---

## 2. 实现阶段划分

```
阶段一: 项目初始化与基础设施
├── 项目结构搭建
├── 开发环境配置
├── 基础设施部署
└── 数据库Schema初始化

阶段二: 核心后端服务
├── 用户认证授权
├── 项目管理模块
├── 文档管理模块
├── 资产管理模块
├── 威胁分析模块
└── 报告生成模块

阶段三: AI智能体与知识库
├── AI客户端封装
├── 文档解析服务
├── 智能资产识别
├── 威胁自动分析
├── 知识库服务
└── 向量检索服务

阶段四: 前端应用开发
├── 基础框架搭建
├── 通用组件库
├── 项目管理页面
├── TARA分析工作台
├── 知识图谱可视化
└── 报告中心

阶段五: 系统集成与优化
├── 端到端集成测试
├── 性能优化
├── 安全加固
└── 部署文档
```

---

## 3. 第一阶段：项目初始化与基础设施

### 3.1 项目结构搭建

#### 3.1.1 创建目录结构

```bash
intelli-tara/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── components/          # 通用组件
│   │   │   ├── common/          # 基础UI组件
│   │   │   └── business/        # 业务组件
│   │   ├── pages/               # 页面组件
│   │   ├── services/            # API服务层
│   │   ├── stores/              # Zustand状态管理
│   │   ├── hooks/               # 自定义Hooks
│   │   ├── types/               # TypeScript类型定义
│   │   ├── styles/              # 全局样式
│   │   ├── utils/               # 工具函数
│   │   ├── constants/           # 常量定义
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/                 # API路由层
│   │   │   └── v1/
│   │   │       ├── endpoints/   # 各模块API端点
│   │   │       ├── deps.py      # 依赖注入
│   │   │       └── router.py    # 路由汇总
│   │   ├── core/                # 核心配置
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── security.py      # 安全相关
│   │   │   └── exceptions.py    # 异常定义
│   │   ├── models/              # SQLAlchemy模型
│   │   ├── schemas/             # Pydantic模型
│   │   ├── services/            # 业务逻辑层
│   │   ├── repositories/        # 数据访问层
│   │   ├── clients/             # 外部服务客户端
│   │   │   ├── ai/              # AI服务客户端
│   │   │   ├── storage/         # 存储客户端
│   │   │   └── graph/           # 图数据库客户端
│   │   ├── tasks/               # 异步任务
│   │   └── utils/               # 工具函数
│   ├── alembic/                 # 数据库迁移
│   ├── tests/                   # 测试
│   ├── pyproject.toml
│   └── main.py
├── deploy/
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.backend
│   │   └── nginx.conf
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── .env.example
├── scripts/                     # 工具脚本
│   ├── init_db.py
│   ├── seed_knowledge.py
│   └── generate_api_docs.py
├── docs/                        # 项目文档
├── specs/                       # 规格文档
├── knowledge/                   # 知识库数据
│   ├── wp29_threats.json
│   ├── stride_patterns.json
│   └── attack_patterns.json
├── Makefile
└── README.md
```

#### 3.1.2 后端项目初始化

```bash
# 步骤1: 创建后端项目
cd backend
uv init

# 步骤2: 添加核心依赖
uv add fastapi uvicorn[standard] pydantic pydantic-settings
uv add sqlalchemy[asyncio] asyncmy alembic
uv add redis aiokafka
uv add neo4j pymilvus elasticsearch[async]
uv add minio python-multipart
uv add python-jose[cryptography] passlib[bcrypt]
uv add httpx tenacity
uv add openpyxl python-docx PyMuPDF python-pptx
uv add pillow

# 步骤3: 添加开发依赖
uv add --dev pytest pytest-asyncio pytest-cov
uv add --dev ruff mypy
uv add --dev pre-commit
```

#### 3.1.3 前端项目初始化

```bash
# 步骤1: 创建Vite项目
cd frontend
npm create vite@latest . -- --template react-ts

# 步骤2: 安装核心依赖
npm install react-router-dom axios zustand @tanstack/react-query
npm install tailwindcss postcss autoprefixer
npm install @headlessui/react @heroicons/react
npm install d3 cytoscape react-cytoscapejs
npm install dayjs lodash-es
npm install react-hook-form zod @hookform/resolvers

# 步骤3: 安装开发依赖
npm install -D @types/lodash-es @types/d3
npm install -D eslint prettier eslint-plugin-react-hooks
npm install -D vitest @testing-library/react
```

### 3.2 开发环境配置

#### 3.2.1 后端配置文件

**app/core/config.py**
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "Intelli-TARA"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 数据库配置
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20

    # Redis配置
    REDIS_URL: str

    # Neo4j配置
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    # Milvus配置
    MILVUS_HOST: str
    MILVUS_PORT: int = 19530

    # Elasticsearch配置
    ELASTICSEARCH_HOST: str

    # MinIO配置
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "tara-documents"

    # Kafka配置
    KAFKA_BOOTSTRAP_SERVERS: str

    # JWT配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Qwen API配置
    QWEN_API_KEY: str
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

#### 3.2.2 Docker Compose开发环境

**deploy/docker-compose.dev.yml**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: tara
      MYSQL_USER: tara
      MYSQL_PASSWORD: tarapass
    volumes:
      - mysql_data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/neo4jpass
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "neo4j", "status"]
      interval: 10s
      timeout: 5s
      retries: 5

  milvus-etcd:
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      ETCD_AUTO_COMPACTION_MODE: revision
      ETCD_AUTO_COMPACTION_RETENTION: "1000"
      ETCD_QUOTA_BACKEND_BYTES: "4294967296"
    volumes:
      - milvus_etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379

  milvus-minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - milvus_minio:/minio_data
    command: minio server /minio_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  milvus:
    image: milvusdb/milvus:v2.3.3
    ports:
      - "19530:19530"
    environment:
      ETCD_ENDPOINTS: milvus-etcd:2379
      MINIO_ADDRESS: milvus-minio:9000
    volumes:
      - milvus_data:/var/lib/milvus
    depends_on:
      - milvus-etcd
      - milvus-minio

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200 || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  kafka:
    image: bitnami/kafka:3.6
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
    volumes:
      - kafka_data:/bitnami/kafka

volumes:
  mysql_data:
  redis_data:
  neo4j_data:
  milvus_etcd:
  milvus_minio:
  milvus_data:
  es_data:
  minio_data:
  kafka_data:
```

### 3.3 数据库Schema初始化

#### 3.3.1 Alembic配置

```bash
cd backend
uv run alembic init alembic
```

#### 3.3.2 创建数据库模型

按照spec中定义的数据模型，创建以下模型文件：

| 文件 | 包含模型 |
|-----|---------|
| `models/user.py` | User, Role, Permission, UserRole, RolePermission |
| `models/project.py` | Project, ProjectVersion, ProjectMember, ProjectConfig |
| `models/document.py` | Document |
| `models/asset.py` | Asset, AssetRelation |
| `models/threat.py` | ThreatScenario, SecurityMitigation |
| `models/report.py` | Report |
| `models/knowledge.py` | KbWp29Threat, KbAttackPattern, KbSecurityRequirement |

#### 3.3.3 初始化迁移

```bash
# 生成迁移脚本
uv run alembic revision --autogenerate -m "Initial schema"

# 执行迁移
uv run alembic upgrade head
```

### 3.4 任务清单

| 序号 | 任务 | 优先级 | 产出物 |
|-----|------|--------|--------|
| 1.1 | 创建项目目录结构 | P0 | 目录结构 |
| 1.2 | 初始化后端项目（pyproject.toml、依赖） | P0 | backend/ |
| 1.3 | 初始化前端项目（package.json、Vite配置） | P0 | frontend/ |
| 1.4 | 创建Docker Compose开发环境配置 | P0 | docker-compose.dev.yml |
| 1.5 | 配置后端核心设置（config.py） | P0 | app/core/config.py |
| 1.6 | 创建SQLAlchemy数据模型 | P0 | app/models/*.py |
| 1.7 | 配置Alembic并生成初始迁移 | P0 | alembic/ |
| 1.8 | 创建Makefile构建脚本 | P0 | Makefile |
| 1.9 | 配置代码质量工具（ruff, prettier） | P1 | 配置文件 |
| 1.10 | 编写开发环境启动文档 | P1 | docs/development.md |

---

## 4. 第二阶段：核心后端服务

### 4.1 用户认证授权模块

#### 4.1.1 实现内容

| 功能 | 说明 | 优先级 |
|-----|------|--------|
| 用户登录 | JWT Token生成 | P0 |
| 用户登出 | Token失效处理 | P0 |
| Token刷新 | Refresh Token机制 | P0 |
| 密码加密 | bcrypt加密存储 | P0 |
| RBAC权限 | 角色权限校验 | P0 |

#### 4.1.2 文件结构

```
app/
├── api/v1/endpoints/auth.py       # 认证API端点
├── core/security.py               # 安全工具函数
├── services/auth_service.py       # 认证业务逻辑
├── schemas/auth.py                # 认证相关Schema
└── repositories/user_repository.py # 用户数据访问
```

#### 4.1.3 核心代码示例

**app/core/security.py**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
```

### 4.2 项目管理模块

#### 4.2.1 实现内容

| 功能ID | 功能 | 优先级 |
|--------|------|--------|
| PM-001 | 创建项目 | P0 |
| PM-002 | 项目配置 | P0 |
| PM-003 | 项目列表 | P0 |
| PM-004 | 项目详情 | P0 |
| PM-006 | 项目导出 | P0 |
| PM-101 | 创建版本 | P0 |
| PM-102 | 版本列表 | P0 |

#### 4.2.2 文件结构

```
app/
├── api/v1/endpoints/projects.py   # 项目API端点
├── services/project_service.py    # 项目业务逻辑
├── schemas/project.py             # 项目相关Schema
└── repositories/project_repository.py
```

### 4.3 文档管理模块

#### 4.3.1 实现内容

| 功能ID | 功能 | 优先级 |
|--------|------|--------|
| DP-001 | 文档上传 | P0 |
| DP-002 | 支持多格式 | P0 |
| DP-004 | 文档管理 | P0 |
| DP-005 | 文档分类 | P0 |
| DP-101 | OCR识别 | P0 |
| DP-102 | 架构图解析 | P0 |
| DP-103 | 表格解析 | P0 |
| DP-104 | 文本提取 | P0 |

#### 4.3.2 文件结构

```
app/
├── api/v1/endpoints/documents.py
├── services/document_service.py
├── services/parsers/              # 文档解析器
│   ├── base.py                    # 解析器基类
│   ├── pdf_parser.py
│   ├── word_parser.py
│   ├── excel_parser.py
│   ├── ppt_parser.py
│   └── image_parser.py
├── schemas/document.py
├── clients/storage/minio_client.py
└── repositories/document_repository.py
```

#### 4.3.3 文档解析器设计

```python
# app/services/parsers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ParsedContent:
    text_blocks: List[str]
    tables: List[List[List[str]]]
    images: List[bytes]
    metadata: dict

class BaseParser(ABC):
    @abstractmethod
    async def parse(self, file_path: str) -> ParsedContent:
        pass

    @abstractmethod
    def supports(self, file_type: str) -> bool:
        pass

class ParserFactory:
    _parsers: List[BaseParser] = []

    @classmethod
    def register(cls, parser: BaseParser):
        cls._parsers.append(parser)

    @classmethod
    def get_parser(cls, file_type: str) -> Optional[BaseParser]:
        for parser in cls._parsers:
            if parser.supports(file_type):
                return parser
        return None
```

### 4.4 资产管理模块

#### 4.4.1 实现内容

| 功能ID | 功能 | 优先级 |
|--------|------|--------|
| AI-001 | 资产提取 | P0 |
| AI-002 | 资产分类 | P0 |
| AI-003 | 属性标注 | P0 |
| AI-004 | 关系识别 | P0 |
| AI-101 | 资产列表 | P0 |
| AI-102 | 资产编辑 | P0 |
| AI-103 | 资产新增 | P0 |
| AI-104 | 资产删除 | P0 |

#### 4.4.2 文件结构

```
app/
├── api/v1/endpoints/assets.py
├── services/asset_service.py
├── services/asset_identifier.py   # AI资产识别服务
├── schemas/asset.py
├── clients/graph/neo4j_client.py  # 图数据库客户端
└── repositories/asset_repository.py
```

### 4.5 威胁分析模块

#### 4.5.1 实现内容

| 功能ID | 功能 | 优先级 |
|--------|------|--------|
| TA-001 | 威胁生成 | P0 |
| TA-002 | 攻击路径 | P0 |
| TA-003 | WP29映射 | P0 |
| TA-101~104 | 攻击可行性评估 | P0 |
| TA-105 | 可行性计算 | P0 |
| TA-201~205 | 影响分析 | P0 |
| TA-301~303 | 风险评估 | P0 |
| TA-401~403 | 安全措施生成 | P0 |

#### 4.5.2 文件结构

```
app/
├── api/v1/endpoints/threats.py
├── services/threat_service.py
├── services/threat_analyzer.py    # AI威胁分析服务
├── services/risk_calculator.py    # 风险计算服务
├── schemas/threat.py
└── repositories/threat_repository.py
```

#### 4.5.3 风险计算器

```python
# app/services/risk_calculator.py
from enum import Enum
from typing import Tuple

class AttackVector(Enum):
    PHYSICAL = 0
    LOCAL = 1
    ADJACENT = 2
    NETWORK = 3

class AttackComplexity(Enum):
    HIGH = 0
    LOW = 1

class PrivilegesRequired(Enum):
    HIGH = 0
    LOW = 1
    NONE = 2

class UserInteraction(Enum):
    REQUIRED = 0
    NONE = 1

class RiskCalculator:
    # 攻击可行性映射表
    FEASIBILITY_MAP = {
        # (V, C, P, U) -> 可行性等级 (0=极低, 1=低, 2=中, 3=高)
        # 简化示例，实际需要完整映射
    }

    # 风险等级矩阵
    RISK_MATRIX = [
        [1, 1, 1, 2],  # 极低可行性
        [1, 1, 2, 3],  # 低可行性
        [1, 2, 3, 4],  # 中可行性
        [2, 3, 4, 5],  # 高可行性
    ]

    @classmethod
    def calculate_feasibility(
        cls,
        attack_vector: AttackVector,
        complexity: AttackComplexity,
        privileges: PrivilegesRequired,
        user_interaction: UserInteraction
    ) -> Tuple[int, str]:
        """计算攻击可行性等级"""
        # 实现攻击可行性计算逻辑
        pass

    @classmethod
    def calculate_impact(
        cls,
        safety: int,
        financial: int,
        operational: int,
        privacy: int
    ) -> Tuple[int, str]:
        """计算影响等级"""
        value = max(safety, financial, operational, privacy)
        labels = ["Negligible", "Moderate", "Major", "Severe"]
        return value, labels[value]

    @classmethod
    def calculate_risk_level(
        cls,
        feasibility: int,
        impact: int
    ) -> Tuple[int, str]:
        """计算风险等级"""
        level = cls.RISK_MATRIX[feasibility][impact]
        labels = {1: "可接受", 2: "低", 3: "中", 4: "高", 5: "严重"}
        return level, labels[level]
```

### 4.6 报告生成模块

#### 4.6.1 实现内容

| 功能ID | 功能 | 优先级 |
|--------|------|--------|
| RC-001 | 生成报告 | P0 |
| RC-002 | 报告预览 | P0 |
| RC-003 | 报告下载 | P0 |
| RC-101 | 报告列表 | P0 |
| RC-102 | 报告版本 | P0 |

#### 4.6.2 文件结构

```
app/
├── api/v1/endpoints/reports.py
├── services/report_service.py
├── services/report_generator.py   # Excel报告生成器
├── schemas/report.py
└── repositories/report_repository.py
```

#### 4.6.3 报告生成器

```python
# app/services/report_generator.py
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from typing import List
from app.models.project import Project
from app.models.asset import Asset
from app.models.threat import ThreatScenario

class TARAReportGenerator:
    def __init__(self):
        self.wb = Workbook()
        self._setup_styles()

    def _setup_styles(self):
        self.header_font = Font(bold=True, size=11)
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

    async def generate(
        self,
        project: Project,
        assets: List[Asset],
        threats: List[ThreatScenario]
    ) -> str:
        """生成TARA报告"""
        self._create_cover_sheet(project)
        self._create_definition_sheet(project)
        self._create_asset_sheet(assets)
        self._create_attack_tree_sheet(project)
        self._create_tara_result_sheet(threats)

        # 删除默认Sheet
        if "Sheet" in self.wb.sheetnames:
            del self.wb["Sheet"]

        # 保存文件
        file_path = f"/tmp/reports/{project.id}_TARA_Report.xlsx"
        self.wb.save(file_path)
        return file_path

    def _create_cover_sheet(self, project: Project):
        ws = self.wb.create_sheet("封面", 0)
        # 实现封面内容

    def _create_definition_sheet(self, project: Project):
        ws = self.wb.create_sheet("相关定义", 1)
        # 实现相关定义内容

    def _create_asset_sheet(self, assets: List[Asset]):
        ws = self.wb.create_sheet("资产列表", 2)

        # 表头
        headers = ["资产ID", "资产名称", "分类", "备注",
                   "真实性", "完整性", "不可抵赖性", "机密性", "可用性", "权限"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border

        # 数据行
        for row, asset in enumerate(assets, 2):
            ws.cell(row=row, column=1, value=asset.asset_id)
            ws.cell(row=row, column=2, value=asset.name)
            ws.cell(row=row, column=3, value=asset.category)
            ws.cell(row=row, column=4, value=asset.remarks)
            ws.cell(row=row, column=5, value="√" if asset.authenticity else "")
            ws.cell(row=row, column=6, value="√" if asset.integrity else "")
            ws.cell(row=row, column=7, value="√" if asset.non_repudiation else "")
            ws.cell(row=row, column=8, value="√" if asset.confidentiality else "")
            ws.cell(row=row, column=9, value="√" if asset.availability else "")
            ws.cell(row=row, column=10, value="√" if asset.authorization else "")

    def _create_attack_tree_sheet(self, project: Project):
        ws = self.wb.create_sheet("攻击树分析", 3)
        # 插入攻击树图片

    def _create_tara_result_sheet(self, threats: List[ThreatScenario]):
        ws = self.wb.create_sheet("TARA分析结果", 4)

        # 表头（按spec中的列定义）
        headers = [
            "资产ID", "资产名称", "细分类", "分类", "安全属性", "STRIDE模型",
            "潜在威胁和损害场景", "攻击路径", "来源", "WP29映射",
            "攻击向量", "攻击复杂度", "权限需求", "用户交互", "可行性计算",
            "Safety", "Financial", "Operational", "Privacy", "影响等级",
            "风险等级", "处置决策", "安全目标", "安全需求", "WP29控制"
        ]

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.border = self.border

        # 数据行
        for row, threat in enumerate(threats, 2):
            # 填充威胁数据
            pass
```

### 4.7 任务清单

| 序号 | 任务 | 优先级 | 产出物 |
|-----|------|--------|--------|
| 2.1 | 实现JWT认证（登录/登出/刷新） | P0 | auth相关代码 |
| 2.2 | 实现RBAC权限中间件 | P0 | 权限装饰器 |
| 2.3 | 实现项目CRUD API | P0 | projects端点 |
| 2.4 | 实现项目版本管理 | P0 | versions端点 |
| 2.5 | 实现文档上传（MinIO集成） | P0 | documents端点 |
| 2.6 | 实现PDF解析器 | P0 | pdf_parser.py |
| 2.7 | 实现Word解析器 | P0 | word_parser.py |
| 2.8 | 实现Excel解析器 | P0 | excel_parser.py |
| 2.9 | 实现资产CRUD API | P0 | assets端点 |
| 2.10 | 实现威胁CRUD API | P0 | threats端点 |
| 2.11 | 实现风险计算服务 | P0 | risk_calculator.py |
| 2.12 | 实现报告生成服务 | P0 | report_generator.py |
| 2.13 | 实现统一响应格式 | P0 | response模型 |
| 2.14 | 实现全局异常处理 | P0 | exception_handlers.py |
| 2.15 | 编写API单元测试 | P1 | tests/ |

---

## 5. 第三阶段：AI智能体与知识库

### 5.1 AI客户端封装

#### 5.1.1 实现内容

| 功能 | 说明 | 优先级 |
|-----|------|--------|
| 文本生成 | qwen-max调用 | P0 |
| 多模态理解 | qwen-vl-max调用 | P0 |
| OCR识别 | qwen-ocr调用 | P0 |
| 向量嵌入 | text-embedding-v3调用 | P0 |

#### 5.1.2 文件结构

```
app/clients/ai/
├── __init__.py
├── base.py              # AI客户端基类
├── qwen_client.py       # Qwen API客户端
├── prompts/             # 提示词模板
│   ├── asset_identification.py
│   ├── threat_analysis.py
│   ├── architecture_understanding.py
│   └── security_measure.py
└── schemas.py           # AI响应Schema
```

#### 5.1.3 Qwen客户端实现

```python
# app/clients/ai/qwen_client.py
import httpx
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings

settings = get_settings()

class QwenClient:
    def __init__(self):
        self.base_url = settings.QWEN_BASE_URL
        self.api_key = settings.QWEN_API_KEY
        self.client = httpx.AsyncClient(timeout=60.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def chat_completion(
        self,
        messages: List[dict],
        model: str = "qwen-max",
        temperature: float = 0.7,
        response_format: Optional[str] = None
    ) -> str:
        """文本对话补全"""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def vision_completion(
        self,
        image_url: str,
        prompt: str,
        model: str = "qwen-vl-max"
    ) -> str:
        """多模态视觉理解"""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": model, "messages": messages}
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def embedding(
        self,
        text: str,
        model: str = "text-embedding-v3"
    ) -> List[float]:
        """文本向量化"""
        response = await self.client.post(
            f"{self.base_url}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": model, "input": text}
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
```

### 5.2 智能资产识别服务

#### 5.2.1 实现逻辑

```python
# app/services/asset_identifier.py
from typing import List
from app.clients.ai.qwen_client import QwenClient
from app.clients.ai.prompts.asset_identification import ASSET_IDENTIFICATION_PROMPT
from app.schemas.asset import AssetCreate
import json

class AssetIdentifier:
    def __init__(self, qwen_client: QwenClient):
        self.client = qwen_client

    async def identify_from_text(self, text: str) -> List[AssetCreate]:
        """从文本中识别资产"""
        messages = [
            {"role": "system", "content": ASSET_IDENTIFICATION_PROMPT},
            {"role": "user", "content": f"请从以下文档内容中识别资产:\n\n{text}"}
        ]

        response = await self.client.chat_completion(
            messages=messages,
            model="qwen-max",
            temperature=0.3,
            response_format="json"
        )

        assets_data = json.loads(response)
        return [AssetCreate(**asset) for asset in assets_data["assets"]]

    async def identify_from_architecture(self, image_url: str) -> List[AssetCreate]:
        """从架构图中识别资产"""
        response = await self.client.vision_completion(
            image_url=image_url,
            prompt="""分析这张汽车电子架构图，识别其中的所有资产。
            对于每个资产，请提供:
            1. 资产ID (如HW-001, SW-001等)
            2. 资产名称
            3. 资产分类 (硬件/软件/数据/接口)
            4. 资产描述
            5. 安全属性 (真实性/完整性/不可抵赖性/机密性/可用性/授权性)

            请以JSON格式输出。"""
        )

        assets_data = json.loads(response)
        return [AssetCreate(**asset) for asset in assets_data["assets"]]
```

### 5.3 智能威胁分析服务

```python
# app/services/threat_analyzer.py
from typing import List
from app.clients.ai.qwen_client import QwenClient
from app.clients.ai.prompts.threat_analysis import THREAT_ANALYSIS_PROMPT
from app.schemas.threat import ThreatCreate
from app.schemas.asset import Asset
import json

class ThreatAnalyzer:
    def __init__(self, qwen_client: QwenClient):
        self.client = qwen_client

    async def analyze_threats(self, asset: Asset) -> List[ThreatCreate]:
        """基于STRIDE模型分析资产威胁"""
        messages = [
            {"role": "system", "content": THREAT_ANALYSIS_PROMPT},
            {"role": "user", "content": f"""
请对以下资产进行威胁分析:

资产信息:
- ID: {asset.asset_id}
- 名称: {asset.name}
- 分类: {asset.category}
- 描述: {asset.description}
- 安全属性: 真实性={asset.authenticity}, 完整性={asset.integrity},
  机密性={asset.confidentiality}, 可用性={asset.availability}

请基于STRIDE模型，针对每个相关的安全属性生成威胁场景。
对于每个威胁，请提供:
1. STRIDE类型
2. 威胁描述
3. 损害场景
4. 攻击路径
5. 攻击可行性评估 (攻击向量/复杂度/权限需求/用户交互)
6. 影响评估 (Safety/Financial/Operational/Privacy)
7. 建议的安全措施

请以JSON格式输出。
"""}
        ]

        response = await self.client.chat_completion(
            messages=messages,
            model="qwen-max",
            temperature=0.5,
            response_format="json"
        )

        threats_data = json.loads(response)
        return [ThreatCreate(**threat) for threat in threats_data["threats"]]
```

### 5.4 知识库服务

#### 5.4.1 知识库数据初始化

```python
# scripts/seed_knowledge.py
import json
from app.models.knowledge import KbWp29Threat, KbAttackPattern

async def seed_wp29_threats(session):
    """导入WP29威胁库"""
    with open("knowledge/wp29_threats.json", "r", encoding="utf-8") as f:
        threats = json.load(f)

    for threat in threats:
        db_threat = KbWp29Threat(
            code=threat["code"],
            category=threat["category"],
            subcategory=threat["subcategory"],
            threat_description_en=threat["threat_en"],
            threat_description_zh=threat["threat_zh"],
            mitigation_en=threat["mitigation_en"],
            mitigation_zh=threat["mitigation_zh"]
        )
        session.add(db_threat)

    await session.commit()

async def seed_attack_patterns(session):
    """导入攻击模式库"""
    with open("knowledge/attack_patterns.json", "r", encoding="utf-8") as f:
        patterns = json.load(f)

    for pattern in patterns:
        db_pattern = KbAttackPattern(
            pattern_id=pattern["id"],
            name=pattern["name"],
            description=pattern["description"],
            prerequisites=pattern["prerequisites"],
            attack_steps=pattern["attack_steps"],
            mitigations=pattern["mitigations"],
            related_cwe=json.dumps(pattern["related_cwe"]),
            related_capec=pattern["related_capec"]
        )
        session.add(db_pattern)

    await session.commit()
```

#### 5.4.2 向量检索服务

```python
# app/services/vector_service.py
from typing import List, Tuple
from pymilvus import Collection, connections
from app.clients.ai.qwen_client import QwenClient
from app.core.config import get_settings

settings = get_settings()

class VectorService:
    def __init__(self, qwen_client: QwenClient):
        self.qwen = qwen_client
        connections.connect(host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
        self.doc_collection = Collection("document_embeddings")
        self.kb_collection = Collection("knowledge_embeddings")

    async def index_document(self, doc_id: int, content: str, project_id: int):
        """索引文档内容"""
        # 分块处理
        chunks = self._split_text(content, chunk_size=500, overlap=50)

        for idx, chunk in enumerate(chunks):
            embedding = await self.qwen.embedding(chunk)
            self.doc_collection.insert([
                [doc_id * 10000 + idx],  # id
                [project_id],
                [doc_id],
                [idx],
                [chunk],
                [embedding]
            ])

    async def search_similar(
        self,
        query: str,
        project_id: int,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """搜索相似内容"""
        query_embedding = await self.qwen.embedding(query)

        results = self.doc_collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=top_k,
            expr=f"project_id == {project_id}",
            output_fields=["content"]
        )

        return [(hit.entity.get("content"), hit.score) for hit in results[0]]

    def _split_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """文本分块"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks
```

### 5.5 知识图谱服务

```python
# app/clients/graph/neo4j_client.py
from neo4j import AsyncGraphDatabase
from typing import List, Dict, Any
from app.core.config import get_settings

settings = get_settings()

class Neo4jClient:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    async def create_asset_node(self, asset: Dict[str, Any]) -> str:
        """创建资产节点"""
        query = """
        CREATE (a:Asset {
            id: $id,
            name: $name,
            category: $category,
            subcategory: $subcategory,
            description: $description,
            project_id: $project_id
        })
        RETURN a.id as id
        """
        async with self.driver.session() as session:
            result = await session.run(query, **asset)
            record = await result.single()
            return record["id"]

    async def create_asset_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        properties: Dict[str, Any] = None
    ):
        """创建资产关系"""
        props = properties or {}
        query = f"""
        MATCH (s:Asset {{id: $source_id}})
        MATCH (t:Asset {{id: $target_id}})
        CREATE (s)-[r:{relation_type} $props]->(t)
        RETURN type(r) as relation
        """
        async with self.driver.session() as session:
            await session.run(query, source_id=source_id, target_id=target_id, props=props)

    async def get_asset_graph(self, project_id: int) -> Dict[str, Any]:
        """获取项目资产图谱"""
        query = """
        MATCH (a:Asset {project_id: $project_id})
        OPTIONAL MATCH (a)-[r]->(b:Asset {project_id: $project_id})
        RETURN a, r, b
        """
        async with self.driver.session() as session:
            result = await session.run(query, project_id=project_id)
            nodes = []
            edges = []
            async for record in result:
                nodes.append(dict(record["a"]))
                if record["r"] and record["b"]:
                    edges.append({
                        "source": record["a"]["id"],
                        "target": record["b"]["id"],
                        "type": record["r"].type
                    })
            return {"nodes": nodes, "edges": edges}

    async def find_attack_paths(
        self,
        start_asset_id: str,
        end_asset_id: str,
        max_depth: int = 5
    ) -> List[List[str]]:
        """查找攻击路径"""
        query = """
        MATCH path = shortestPath(
            (start:Asset {id: $start_id})-[*..{max_depth}]->(end:Asset {id: $end_id})
        )
        RETURN [n IN nodes(path) | n.id] as path
        """
        async with self.driver.session() as session:
            result = await session.run(
                query,
                start_id=start_asset_id,
                end_id=end_asset_id,
                max_depth=max_depth
            )
            paths = []
            async for record in result:
                paths.append(record["path"])
            return paths
```

### 5.6 任务清单

| 序号 | 任务 | 优先级 | 产出物 |
|-----|------|--------|--------|
| 3.1 | 实现Qwen API客户端 | P0 | qwen_client.py |
| 3.2 | 编写资产识别提示词 | P0 | prompts/asset_identification.py |
| 3.3 | 编写威胁分析提示词 | P0 | prompts/threat_analysis.py |
| 3.4 | 实现资产识别服务 | P0 | asset_identifier.py |
| 3.5 | 实现威胁分析服务 | P0 | threat_analyzer.py |
| 3.6 | 实现Neo4j客户端 | P0 | neo4j_client.py |
| 3.7 | 实现知识图谱服务 | P0 | graph_service.py |
| 3.8 | 实现Milvus向量服务 | P0 | vector_service.py |
| 3.9 | 准备WP29威胁库数据 | P0 | wp29_threats.json |
| 3.10 | 准备攻击模式库数据 | P0 | attack_patterns.json |
| 3.11 | 实现知识库初始化脚本 | P0 | seed_knowledge.py |
| 3.12 | 实现知识库检索API | P0 | knowledge端点 |
| 3.13 | 实现对话交互API | P1 | agent端点 |
| 3.14 | 编写AI服务单元测试 | P1 | tests/ |

---

## 6. 第四阶段：前端应用开发

### 6.1 基础框架搭建

#### 6.1.1 项目配置

**vite.config.ts**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        risk: {
          critical: '#dc2626',
          high: '#ea580c',
          medium: '#ca8a04',
          low: '#16a34a',
          acceptable: '#6b7280',
        }
      },
    },
  },
  plugins: [],
}
```

#### 6.1.2 路由配置

**src/App.tsx**
```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from '@/components/common/Layout'
import Login from '@/pages/Login'
import Dashboard from '@/pages/Dashboard'
import Projects from '@/pages/Projects'
import ProjectDetail from '@/pages/ProjectDetail'
import Analysis from '@/pages/Analysis'
import Reports from '@/pages/Reports'
import Settings from '@/pages/Settings'
import { useAuthStore } from '@/stores/authStore'

const queryClient = new QueryClient()

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="projects" element={<Projects />} />
            <Route path="projects/:id" element={<ProjectDetail />} />
            <Route path="projects/:id/analysis" element={<Analysis />} />
            <Route path="reports" element={<Reports />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
```

### 6.2 通用组件库

#### 6.2.1 组件清单

| 组件 | 说明 | 优先级 |
|-----|------|--------|
| Button | 按钮组件 | P0 |
| Input | 输入框组件 | P0 |
| Select | 选择器组件 | P0 |
| Modal | 模态框组件 | P0 |
| Table | 表格组件 | P0 |
| Card | 卡片组件 | P0 |
| Toast | 消息提示 | P0 |
| Loading | 加载状态 | P0 |
| Tabs | 标签页 | P0 |
| Dropdown | 下拉菜单 | P0 |
| Pagination | 分页组件 | P0 |
| FileUploader | 文件上传 | P0 |

#### 6.2.2 业务组件清单

| 组件 | 说明 | 优先级 |
|-----|------|--------|
| AssetList | 资产列表 | P0 |
| AssetForm | 资产表单 | P0 |
| ThreatTable | 威胁表格 | P0 |
| ThreatForm | 威胁表单 | P0 |
| RiskMatrix | 风险矩阵 | P0 |
| AttackTree | 攻击树图 | P0 |
| GraphViewer | 知识图谱视图 | P0 |
| DocumentUploader | 文档上传器 | P0 |
| ReportPreview | 报告预览 | P0 |
| ProgressSteps | 进度步骤 | P0 |

### 6.3 状态管理

#### 6.3.1 Store定义

**src/stores/authStore.ts**
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  username: string
  email: string
  roles: string[]
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  setAuth: (user: User, accessToken: string, refreshToken: string) => void
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      setAuth: (user, accessToken, refreshToken) =>
        set({ user, accessToken, refreshToken, isAuthenticated: true }),
      clearAuth: () =>
        set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
)
```

**src/stores/projectStore.ts**
```typescript
import { create } from 'zustand'

interface Project {
  id: number
  name: string
  status: string
  // ...
}

interface ProjectState {
  currentProject: Project | null
  setCurrentProject: (project: Project | null) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  setCurrentProject: (project) => set({ currentProject: project }),
}))
```

### 6.4 API服务层

**src/services/api.ts**
```typescript
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

// 请求拦截器
api.interceptors.request.use((config) => {
  const { accessToken } = useAuthStore.getState()
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    if (error.response?.status === 401) {
      // Token过期，尝试刷新
      const { refreshToken, setAuth, clearAuth } = useAuthStore.getState()
      if (refreshToken) {
        try {
          const res = await axios.post('/api/v1/auth/refresh', { refresh_token: refreshToken })
          setAuth(res.data.user, res.data.access_token, res.data.refresh_token)
          // 重试原请求
          error.config.headers.Authorization = `Bearer ${res.data.access_token}`
          return api.request(error.config)
        } catch {
          clearAuth()
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
```

**src/services/projectService.ts**
```typescript
import api from './api'
import { Project, ProjectCreate, ProjectUpdate } from '@/types/project'

export const projectService = {
  list: (params?: { page?: number; pageSize?: number; status?: string }) =>
    api.get<{ items: Project[]; total: number }>('/projects', { params }),

  get: (id: number) =>
    api.get<Project>(`/projects/${id}`),

  create: (data: ProjectCreate) =>
    api.post<Project>('/projects', data),

  update: (id: number, data: ProjectUpdate) =>
    api.put<Project>(`/projects/${id}`, data),

  delete: (id: number) =>
    api.delete(`/projects/${id}`),
}
```

### 6.5 页面开发

#### 6.5.1 仪表盘页面

```typescript
// src/pages/Dashboard.tsx
import { useQuery } from '@tanstack/react-query'
import { Card } from '@/components/common/Card'
import { RiskMatrix } from '@/components/business/RiskMatrix'
import { projectService } from '@/services/projectService'

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => projectService.getStats(),
  })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">仪表盘</h1>

      {/* 统计卡片 */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <div className="text-sm text-gray-500">项目总数</div>
          <div className="text-3xl font-bold">{stats?.projectCount || 0}</div>
        </Card>
        <Card>
          <div className="text-sm text-gray-500">资产总数</div>
          <div className="text-3xl font-bold">{stats?.assetCount || 0}</div>
        </Card>
        <Card>
          <div className="text-sm text-gray-500">威胁总数</div>
          <div className="text-3xl font-bold">{stats?.threatCount || 0}</div>
        </Card>
        <Card>
          <div className="text-sm text-gray-500">高风险项</div>
          <div className="text-3xl font-bold text-red-500">{stats?.highRiskCount || 0}</div>
        </Card>
      </div>

      {/* 风险矩阵 */}
      <Card>
        <h2 className="text-lg font-semibold mb-4">风险分布</h2>
        <RiskMatrix data={stats?.riskDistribution} />
      </Card>
    </div>
  )
}
```

#### 6.5.2 TARA分析工作台

```typescript
// src/pages/Analysis.tsx
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { Tabs } from '@/components/common/Tabs'
import { DocumentUploader } from '@/components/business/DocumentUploader'
import { AssetList } from '@/components/business/AssetList'
import { ThreatTable } from '@/components/business/ThreatTable'
import { GraphViewer } from '@/components/business/GraphViewer'

const tabs = [
  { key: 'documents', label: '文档管理' },
  { key: 'assets', label: '资产识别' },
  { key: 'threats', label: '威胁分析' },
  { key: 'graph', label: '知识图谱' },
]

export default function Analysis() {
  const { id: projectId } = useParams<{ id: string }>()
  const [activeTab, setActiveTab] = useState('documents')

  return (
    <div className="space-y-4">
      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

      <div className="bg-white rounded-lg shadow p-6">
        {activeTab === 'documents' && (
          <DocumentUploader projectId={Number(projectId)} />
        )}
        {activeTab === 'assets' && (
          <AssetList projectId={Number(projectId)} />
        )}
        {activeTab === 'threats' && (
          <ThreatTable projectId={Number(projectId)} />
        )}
        {activeTab === 'graph' && (
          <GraphViewer projectId={Number(projectId)} />
        )}
      </div>
    </div>
  )
}
```

### 6.6 知识图谱可视化

```typescript
// src/components/business/GraphViewer.tsx
import { useEffect, useRef } from 'react'
import CytoscapeComponent from 'react-cytoscapejs'
import { useQuery } from '@tanstack/react-query'
import { graphService } from '@/services/graphService'

interface GraphViewerProps {
  projectId: number
}

export function GraphViewer({ projectId }: GraphViewerProps) {
  const cyRef = useRef<cytoscape.Core | null>(null)

  const { data: graphData } = useQuery({
    queryKey: ['project-graph', projectId],
    queryFn: () => graphService.getProjectGraph(projectId),
  })

  const elements = graphData ? [
    ...graphData.nodes.map(node => ({
      data: { id: node.id, label: node.name, category: node.category },
    })),
    ...graphData.edges.map(edge => ({
      data: { source: edge.source, target: edge.target, label: edge.type },
    })),
  ] : []

  const stylesheet = [
    {
      selector: 'node',
      style: {
        'background-color': '#3b82f6',
        'label': 'data(label)',
        'color': '#1f2937',
        'text-valign': 'bottom',
        'text-margin-y': 5,
      },
    },
    {
      selector: 'node[category="hardware"]',
      style: { 'background-color': '#10b981' },
    },
    {
      selector: 'node[category="software"]',
      style: { 'background-color': '#8b5cf6' },
    },
    {
      selector: 'node[category="data"]',
      style: { 'background-color': '#f59e0b' },
    },
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#9ca3af',
        'target-arrow-color': '#9ca3af',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        'label': 'data(label)',
        'font-size': 10,
      },
    },
  ]

  return (
    <div className="h-[600px] border rounded-lg">
      <CytoscapeComponent
        elements={elements}
        stylesheet={stylesheet}
        layout={{ name: 'cose' }}
        style={{ width: '100%', height: '100%' }}
        cy={(cy) => { cyRef.current = cy }}
      />
    </div>
  )
}
```

### 6.7 任务清单

| 序号 | 任务 | 优先级 | 产出物 |
|-----|------|--------|--------|
| 4.1 | 初始化Vite项目配置 | P0 | vite.config.ts |
| 4.2 | 配置TailwindCSS | P0 | tailwind.config.js |
| 4.3 | 配置路由（react-router） | P0 | App.tsx |
| 4.4 | 实现通用UI组件 | P0 | components/common/ |
| 4.5 | 实现认证Store | P0 | stores/authStore.ts |
| 4.6 | 实现API服务层 | P0 | services/ |
| 4.7 | 实现登录页面 | P0 | pages/Login.tsx |
| 4.8 | 实现仪表盘页面 | P0 | pages/Dashboard.tsx |
| 4.9 | 实现项目列表页面 | P0 | pages/Projects.tsx |
| 4.10 | 实现项目详情页面 | P0 | pages/ProjectDetail.tsx |
| 4.11 | 实现TARA分析工作台 | P0 | pages/Analysis.tsx |
| 4.12 | 实现资产列表组件 | P0 | components/business/AssetList.tsx |
| 4.13 | 实现威胁表格组件 | P0 | components/business/ThreatTable.tsx |
| 4.14 | 实现风险矩阵组件 | P0 | components/business/RiskMatrix.tsx |
| 4.15 | 实现知识图谱组件 | P0 | components/business/GraphViewer.tsx |
| 4.16 | 实现文档上传组件 | P0 | components/business/DocumentUploader.tsx |
| 4.17 | 实现报告中心页面 | P0 | pages/Reports.tsx |
| 4.18 | 实现设置页面 | P1 | pages/Settings.tsx |
| 4.19 | 编写前端单元测试 | P1 | tests/ |

---

## 7. 第五阶段：系统集成与优化

### 7.1 端到端集成测试

#### 7.1.1 测试场景

| 场景 | 测试内容 | 优先级 |
|-----|---------|--------|
| 用户登录流程 | 登录、Token刷新、登出 | P0 |
| 项目创建流程 | 创建项目、配置、版本管理 | P0 |
| 文档解析流程 | 上传、解析、预览 | P0 |
| 资产识别流程 | AI识别、手动编辑、确认 | P0 |
| 威胁分析流程 | AI分析、风险评估、措施生成 | P0 |
| 报告生成流程 | 生成、预览、下载 | P0 |

#### 7.1.2 测试工具

- 后端: pytest + pytest-asyncio
- 前端: Vitest + Testing Library
- E2E: Playwright

### 7.2 性能优化

#### 7.2.1 后端优化

| 优化项 | 措施 |
|-------|------|
| 数据库查询 | 添加索引、优化N+1查询 |
| 缓存 | Redis缓存热点数据 |
| 异步任务 | Kafka异步处理文档解析、AI分析 |
| 连接池 | 配置合理的数据库连接池大小 |

#### 7.2.2 前端优化

| 优化项 | 措施 |
|-------|------|
| 代码分割 | 路由级别懒加载 |
| 状态缓存 | React Query缓存API响应 |
| 虚拟滚动 | 大列表使用虚拟滚动 |
| 资源压缩 | Gzip压缩静态资源 |

### 7.3 安全加固

| 安全项 | 措施 |
|-------|------|
| 认证安全 | JWT密钥轮换、Token黑名单 |
| 接口安全 | 请求频率限制、参数校验 |
| 数据安全 | 敏感数据加密、SQL注入防护 |
| 审计日志 | 关键操作记录、异常监控 |

### 7.4 部署配置

#### 7.4.1 生产环境配置

**deploy/docker-compose.yml**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - frontend
      - backend

  frontend:
    build:
      context: ../frontend
      dockerfile: ../deploy/docker/Dockerfile.frontend
    expose:
      - "80"

  backend:
    build:
      context: ../backend
      dockerfile: ../deploy/docker/Dockerfile.backend
    expose:
      - "8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - NEO4J_URI=${NEO4J_URI}
      - NEO4J_USER=${NEO4J_USER}
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - MILVUS_HOST=${MILVUS_HOST}
      - ELASTICSEARCH_HOST=${ELASTICSEARCH_HOST}
      - MINIO_ENDPOINT=${MINIO_ENDPOINT}
      - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
      - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
      - KAFKA_BOOTSTRAP_SERVERS=${KAFKA_BOOTSTRAP_SERVERS}
      - QWEN_API_KEY=${QWEN_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - mysql
      - redis
      - neo4j
      - milvus
      - elasticsearch
      - minio
      - kafka

  # ... 其他服务配置
```

### 7.5 任务清单

| 序号 | 任务 | 优先级 | 产出物 |
|-----|------|--------|--------|
| 5.1 | 编写端到端测试用例 | P0 | tests/e2e/ |
| 5.2 | 执行性能测试 | P1 | 性能报告 |
| 5.3 | 数据库索引优化 | P0 | 迁移脚本 |
| 5.4 | 实现Redis缓存 | P0 | cache_service.py |
| 5.5 | 实现异步任务处理 | P0 | tasks/ |
| 5.6 | 前端代码分割优化 | P0 | vite配置 |
| 5.7 | 安全加固 | P0 | 安全中间件 |
| 5.8 | 编写部署文档 | P0 | docs/deployment.md |
| 5.9 | 配置CI/CD | P1 | .github/workflows/ |
| 5.10 | 编写用户手册 | P1 | docs/user-guide.md |

---

## 8. 技术栈详细说明

### 8.1 后端技术栈

| 技术 | 版本 | 用途 |
|-----|------|------|
| Python | 3.12 | 运行环境 |
| FastAPI | 0.109+ | Web框架 |
| Uvicorn | 0.27+ | ASGI服务器 |
| SQLAlchemy | 2.0+ | ORM |
| Pydantic | 2.5+ | 数据验证 |
| Alembic | 1.13+ | 数据库迁移 |
| python-jose | 3.3+ | JWT处理 |
| passlib | 1.7+ | 密码加密 |
| httpx | 0.26+ | HTTP客户端 |
| openpyxl | 3.1+ | Excel处理 |
| PyMuPDF | 1.23+ | PDF处理 |
| neo4j | 5.15+ | Neo4j驱动 |
| pymilvus | 2.3+ | Milvus客户端 |
| elasticsearch | 8.11+ | ES客户端 |
| aiokafka | 0.10+ | Kafka客户端 |
| minio | 7.2+ | MinIO客户端 |

### 8.2 前端技术栈

| 技术 | 版本 | 用途 |
|-----|------|------|
| React | 18.2+ | UI框架 |
| TypeScript | 5.3+ | 类型系统 |
| Vite | 5.0+ | 构建工具 |
| React Router | 6.21+ | 路由 |
| TailwindCSS | 3.4+ | CSS框架 |
| Zustand | 4.4+ | 状态管理 |
| React Query | 5.17+ | 数据获取 |
| Axios | 1.6+ | HTTP客户端 |
| D3.js | 7.8+ | 数据可视化 |
| Cytoscape.js | 3.28+ | 图可视化 |
| React Hook Form | 7.49+ | 表单处理 |
| Zod | 3.22+ | Schema验证 |

### 8.3 基础设施

| 组件 | 版本 | 用途 |
|-----|------|------|
| MySQL | 8.0 | 关系数据库 |
| Redis | 7.2 | 缓存 |
| Neo4j | 5.x | 图数据库 |
| Milvus | 2.3 | 向量数据库 |
| Elasticsearch | 8.11 | 全文搜索 |
| MinIO | Latest | 对象存储 |
| Kafka | 3.6 | 消息队列 |
| Nginx | Alpine | 反向代理 |

---

## 9. 开发规范

### 9.1 代码规范

#### 9.1.1 Python代码规范

- 遵循PEP 8规范
- 使用ruff进行代码检查和格式化
- 类型注解完整
- 文档字符串使用Google风格

```python
# ruff配置 pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

#### 9.1.2 TypeScript代码规范

- 遵循ESLint推荐规则
- 使用Prettier格式化
- 严格类型检查
- 组件使用函数式组件

```javascript
// .eslintrc.cjs
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
}
```

### 9.2 Git规范

#### 9.2.1 分支规范

| 分支 | 用途 |
|-----|------|
| main | 生产环境代码 |
| develop | 开发主分支 |
| feature/* | 功能分支 |
| bugfix/* | 缺陷修复分支 |
| release/* | 发布分支 |

#### 9.2.2 提交信息规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型(type):
- feat: 新功能
- fix: 缺陷修复
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

### 9.3 API规范

- 遵循RESTful设计
- 统一响应格式
- 合理的HTTP状态码
- 完整的错误信息

### 9.4 测试规范

- 单元测试覆盖率 > 80%
- 关键业务逻辑必须有测试
- 使用mock隔离外部依赖

---

## 附录

### A. 环境变量清单

```bash
# 应用配置
APP_NAME=Intelli-TARA
DEBUG=false

# 数据库
DATABASE_URL=mysql+asyncmy://user:pass@localhost:3306/tara

# Redis
REDIS_URL=redis://localhost:6379/0

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# Elasticsearch
ELASTICSEARCH_HOST=http://localhost:9200

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=tara-documents

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Qwen API
QWEN_API_KEY=your-api-key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
```

### B. 常用命令

```bash
# 启动开发环境
make dev

# 运行测试
make test

# 构建生产版本
make build

# 部署
make deploy

# 数据库迁移
cd backend && uv run alembic upgrade head

# 初始化知识库
cd backend && uv run python scripts/seed_knowledge.py
```

### C. 参考资源

- FastAPI文档: https://fastapi.tiangolo.com/
- React文档: https://react.dev/
- TailwindCSS文档: https://tailwindcss.com/docs
- Neo4j文档: https://neo4j.com/docs/
- Milvus文档: https://milvus.io/docs/
- 阿里云百炼: https://help.aliyun.com/document_detail/2712195.html
