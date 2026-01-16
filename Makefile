.PHONY: help install dev build test deploy clean frontend-install frontend-dev frontend-build backend-install backend-dev backend-test db-up db-down migrate

help:
	@echo "Intelli-TARA 构建命令"
	@echo ""
	@echo "  make install         - 安装所有依赖"
	@echo "  make dev             - 启动开发环境"
	@echo "  make build           - 构建生产版本"
	@echo "  make test            - 运行测试"
	@echo "  make deploy          - 部署服务"
	@echo "  make clean           - 清理构建文件"
	@echo ""
	@echo "  make db-up           - 启动数据库服务"
	@echo "  make db-down         - 停止数据库服务"
	@echo "  make migrate         - 执行数据库迁移"
	@echo ""
	@echo "  make frontend-dev    - 启动前端开发服务"
	@echo "  make backend-dev     - 启动后端开发服务"

# Install dependencies
install: frontend-install backend-install

frontend-install:
	cd frontend && npm install

backend-install:
	cd backend && pip install uv && uv sync

# Development
dev:
	@echo "请分别运行 make backend-dev 和 make frontend-dev"

frontend-dev:
	cd frontend && npm run dev

backend-dev:
	cd backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Build
build: frontend-build

frontend-build:
	cd frontend && npm run build

# Test
test: backend-test

backend-test:
	cd backend && uv run pytest

# Database
db-up:
	docker compose -f deploy/docker-compose.dev.yml up -d

db-down:
	docker compose -f deploy/docker-compose.dev.yml down

migrate:
	cd backend && uv run alembic upgrade head

migrate-create:
	cd backend && uv run alembic revision --autogenerate -m "$(message)"

# Deploy
deploy:
	docker compose -f deploy/docker-compose.yml up -d --build

# Clean
clean:
	rm -rf frontend/dist frontend/node_modules
	rm -rf backend/.venv backend/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
