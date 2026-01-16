# Intelli-TARA Docker 管理命令
# 使用方法: make <command> [SERVICE=xxx]

.PHONY: build rebuild up down restart logs list help

# Docker Compose 配置
COMPOSE_FILE := deploy/docker-compose.dev.yml
COMPOSE_CMD := docker compose -f $(COMPOSE_FILE)

# 服务列表
SERVICES := mysql redis neo4j elasticsearch minio kafka

# 默认目标
.DEFAULT_GOAL := help

help:
	@echo "Intelli-TARA Docker 管理命令"
	@echo ""
	@echo "使用方法: make <command> [SERVICE=xxx]"
	@echo ""
	@echo "命令列表:"
	@echo "  make build   [SERVICE=xxx]  - 构建服务镜像"
	@echo "  make rebuild [SERVICE=xxx]  - 重新构建服务镜像 (不使用缓存)"
	@echo "  make up      [SERVICE=xxx]  - 启动服务"
	@echo "  make down    [SERVICE=xxx]  - 停止并移除服务"
	@echo "  make restart [SERVICE=xxx]  - 重启服务"
	@echo "  make logs    [SERVICE=xxx]  - 查看服务日志"
	@echo "  make list                   - 查看所有服务状态"
	@echo ""
	@echo "可用服务: $(SERVICES)"
	@echo ""
	@echo "示例:"
	@echo "  make up                     - 启动所有服务"
	@echo "  make up SERVICE=mysql       - 仅启动 mysql 服务"
	@echo "  make logs SERVICE=redis     - 查看 redis 日志"
	@echo "  make restart SERVICE=mysql  - 重启 mysql 服务"

# 构建服务镜像
build:
ifdef SERVICE
	$(COMPOSE_CMD) build $(SERVICE)
else
	$(COMPOSE_CMD) build
endif

# 重新构建服务镜像 (不使用缓存)
rebuild:
ifdef SERVICE
	$(COMPOSE_CMD) build --no-cache $(SERVICE)
else
	$(COMPOSE_CMD) build --no-cache
endif

# 启动服务
up:
ifdef SERVICE
	$(COMPOSE_CMD) up -d $(SERVICE)
else
	$(COMPOSE_CMD) up -d
endif

# 停止并移除服务
down:
ifdef SERVICE
	$(COMPOSE_CMD) stop $(SERVICE)
	$(COMPOSE_CMD) rm -f $(SERVICE)
else
	$(COMPOSE_CMD) down
endif

# 重启服务
restart:
ifdef SERVICE
	$(COMPOSE_CMD) restart $(SERVICE)
else
	$(COMPOSE_CMD) restart
endif

# 查看服务日志
logs:
ifdef SERVICE
	$(COMPOSE_CMD) logs -f $(SERVICE)
else
	$(COMPOSE_CMD) logs -f
endif

# 查看所有服务状态 (包括未启动的服务)
list:
	@echo "=========================================="
	@echo "Intelli-TARA 服务状态"
	@echo "=========================================="
	@echo ""
	@echo "已定义的服务:"
	@$(COMPOSE_CMD) config --services | while read service; do \
		echo "  - $$service"; \
	done
	@echo ""
	@echo "服务运行状态:"
	@$(COMPOSE_CMD) ps -a
	@echo ""
	@echo "=========================================="
