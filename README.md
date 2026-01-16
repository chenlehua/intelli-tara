# Intelli-TARA

智能威胁分析与风险评估平台 (Intelligent Threat Analysis and Risk Assessment Platform)

基于 ISO/SAE 21434 标准，结合 AI 智能体技术，实现汽车网络安全威胁分析与风险评估的自动化。

## 功能特性

- **自动化文档解析**: 支持 PDF、Word、Excel、PPT、图片等多种格式
- **智能资产识别**: 基于 AI 从文档中自动识别和分类资产
- **知识图谱构建**: 构建资产关系图谱，支持关联分析
- **智能威胁分析**: 基于 STRIDE 模型和 WP29 威胁库自动识别威胁
- **风险自动评估**: 自动计算攻击可行性和影响等级
- **报告自动生成**: 生成符合标准格式的 TARA 报告

## 技术栈

### 前端
- React 18 + TypeScript
- Vite 5
- TailwindCSS
- Zustand (状态管理)
- React Query (数据获取)
- Cytoscape.js (图可视化)

### 后端
- Python 3.12 + FastAPI
- SQLAlchemy (ORM)
- Pydantic (数据验证)
- JWT 认证

### 数据库
- MySQL 8.0 (关系数据库)
- Neo4j 5 (图数据库)
- Redis 7 (缓存)
- Milvus (向量数据库)
- Elasticsearch (全文检索)

### AI 服务
- 阿里云百炼 Qwen API

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose

### 安装依赖

```bash
# 安装后端依赖
cd backend
pip install uv
uv sync

# 安装前端依赖
cd frontend
npm install
```

### 启动数据库服务

```bash
make db-up
```

### 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 .env 文件，填入必要的配置
```

### 数据库迁移

```bash
make migrate
```

### 启动开发服务

```bash
# 启动后端服务
make backend-dev

# 新开终端，启动前端服务
make frontend-dev
```

访问 http://localhost:3000 即可使用系统。

## 项目结构

```
intelli-tara/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── components/          # 组件
│   │   ├── pages/               # 页面
│   │   ├── services/            # API服务
│   │   ├── stores/              # 状态管理
│   │   └── ...
│   └── ...
├── backend/                     # 后端项目
│   ├── app/
│   │   ├── api/                 # API路由
│   │   ├── core/                # 核心配置
│   │   ├── models/              # 数据模型
│   │   ├── schemas/             # Pydantic模型
│   │   ├── services/            # 业务逻辑
│   │   └── ...
│   └── ...
├── deploy/                      # 部署配置
│   ├── docker/
│   └── docker-compose.yml
├── docs/                        # 文档
├── specs/                       # 规格说明
├── Makefile                     # 构建脚本
└── README.md
```

## 参考标准

- ISO/SAE 21434:2021 - 道路车辆网络安全工程
- UN R155 - 网络安全和网络安全管理系统
- UN R156 - 软件更新和软件更新管理系统
- ISO 31000 - 风险管理指南

## 许可证

MIT License
