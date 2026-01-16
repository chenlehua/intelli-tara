# Intelli-TARA 部署指南

## 目录

1. [系统要求](#系统要求)
2. [快速开始](#快速开始)
3. [开发环境](#开发环境)
4. [生产环境](#生产环境)
5. [配置说明](#配置说明)
6. [故障排除](#故障排除)

## 系统要求

### 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|-----|---------|---------|
| CPU | 4核 | 8核+ |
| 内存 | 16GB | 32GB+ |
| 磁盘 | 100GB SSD | 500GB SSD |

### 软件要求

- Docker 24.0+
- Docker Compose 2.0+
- Node.js 20+ (开发环境)
- Python 3.12+ (开发环境)

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/your-org/intelli-tara.git
cd intelli-tara
```

### 2. 配置环境变量

```bash
cd deploy
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量
```

### 3. 启动服务

```bash
docker-compose up -d
```

### 4. 访问应用

- 前端: http://localhost
- API文档: http://localhost/docs
- 默认管理员账号: admin / admin123

## 开发环境

### Make 命令列表

```bash
# 查看所有可用命令
make help

# 命令格式: make <command> [SERVICE=xxx]
# 可用命令:
#   make build   [SERVICE=xxx]  - 构建服务镜像
#   make rebuild [SERVICE=xxx]  - 重新构建服务镜像 (不使用缓存)
#   make up      [SERVICE=xxx]  - 启动服务
#   make down    [SERVICE=xxx]  - 停止并移除服务
#   make restart [SERVICE=xxx]  - 重启服务
#   make logs    [SERVICE=xxx]  - 查看服务日志
#   make list                   - 查看所有服务状态
```

### 启动开发数据库

```bash
# 启动所有服务
make up

# 或仅启动特定服务
make up SERVICE=mysql
make up SERVICE=redis
```

### 查看服务状态

```bash
# 查看所有服务状态 (包括未启动的服务)
make list
```

### 查看服务日志

```bash
# 查看所有服务日志
make logs

# 查看特定服务日志
make logs SERVICE=mysql
```

### 重启服务

```bash
# 重启所有服务
make restart

# 重启特定服务
make restart SERVICE=redis
```

### 停止服务

```bash
# 停止所有服务
make down

# 停止特定服务
make down SERVICE=mysql
```

### 启动后端

```bash
cd backend
uv sync
uv run python main.py
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 数据库迁移

```bash
cd backend
uv run alembic upgrade head
```

### 初始化数据

```bash
cd scripts
python init_db.py
python seed_knowledge.py
```

## 生产环境

### 1. 配置 HTTPS

将 SSL 证书放置在 `deploy/certs/` 目录:

```
deploy/certs/
├── fullchain.pem
└── privkey.pem
```

### 2. 更新 Nginx 配置

编辑 `deploy/docker/nginx.conf` 启用 HTTPS。

### 3. 配置环境变量

确保生产环境变量正确配置:

- `JWT_SECRET_KEY`: 使用强随机密钥
- `DATABASE_URL`: 配置生产数据库连接
- `QWEN_API_KEY`: 配置阿里云 Qwen API 密钥

### 4. 启动生产服务

```bash
cd deploy
docker-compose up -d --build
```

### 5. 监控日志

```bash
docker-compose logs -f backend
```

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|-----|------|--------|
| DATABASE_URL | MySQL 连接字符串 | - |
| REDIS_HOST | Redis 主机 | localhost |
| REDIS_PORT | Redis 端口 | 6380 |
| NEO4J_URI | Neo4j 连接 URI | bolt://localhost:7687 |
| QWEN_API_KEY | 阿里云 Qwen API 密钥 | - |
| JWT_SECRET_KEY | JWT 签名密钥 | - |
| DEBUG | 调试模式 | false |

### 服务端口

| 服务 | 端口 |
|-----|------|
| Nginx (HTTP) | 80 |
| Nginx (HTTPS) | 443 |
| Backend API | 8000 |
| MySQL | 3307 |
| Redis | 6380 |
| Neo4j | 7687 |
| Elasticsearch | 9200 |
| MinIO | 9000 |

## 故障排除

### 常见问题

#### 1. 数据库连接失败

```bash
# 检查 MySQL 容器状态
docker-compose ps mysql
docker-compose logs mysql
```

#### 2. Redis 连接失败

```bash
# 检查 Redis 容器
docker-compose exec redis redis-cli ping
```

#### 3. API 请求超时

检查后端日志:

```bash
docker-compose logs -f backend
```

#### 4. 前端构建失败

```bash
cd frontend
rm -rf node_modules
npm install
npm run build
```

### 日志位置

- Backend: `docker-compose logs backend`
- Nginx: `docker-compose logs nginx`
- MySQL: `docker-compose logs mysql`

### 健康检查

```bash
# 检查 API 健康状态
curl http://localhost/health

# 检查所有服务状态
docker-compose ps
```

## 备份与恢复

### 备份数据库

```bash
docker-compose exec mysql mysqldump -u root -p intelli_tara > backup.sql
```

### 恢复数据库

```bash
cat backup.sql | docker-compose exec -T mysql mysql -u root -p intelli_tara
```

### 备份文件存储

```bash
docker cp intelli-tara-minio:/data ./minio-backup
```

## 更新升级

### 1. 拉取最新代码

```bash
git pull origin main
```

### 2. 重新构建并启动

```bash
docker-compose down
docker-compose up -d --build
```

### 3. 执行数据库迁移

```bash
docker-compose exec backend alembic upgrade head
```
