# Makefile para gestión de Docker del proyecto Agora FastAPI

.PHONY: help build up down restart logs clean test health backup postgres-up postgres-down

# Variables
COMPOSE_FILE = docker-compose.yml
POSTGRES_COMPOSE_FILE = docker-compose.postgres.yml
SERVICE_NAME = agora-api
CONTAINER_NAME = agora-fastapi
POSTGRES_CONTAINER_NAME = agora-fastapi-postgres

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@echo ""
	@echo "🗃️  SQLite (por defecto):"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -v postgres | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🐘 PostgreSQL:"
	@grep -E '^postgres.*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir la imagen Docker (SQLite)
	docker-compose build --no-cache

up: ## Iniciar servicios en background (SQLite)
	docker-compose up -d

down: ## Parar y eliminar contenedores (SQLite)
	docker-compose down

# Comandos específicos para PostgreSQL
postgres-up: ## Iniciar servicios con PostgreSQL
	docker-compose -f $(POSTGRES_COMPOSE_FILE) up -d --build

postgres-down: ## Parar servicios PostgreSQL
	docker-compose -f $(POSTGRES_COMPOSE_FILE) down

postgres-logs: ## Ver logs de PostgreSQL
	docker-compose -f $(POSTGRES_COMPOSE_FILE) logs -f

postgres-shell: ## Acceder al shell de PostgreSQL
	docker-compose -f $(POSTGRES_COMPOSE_FILE) exec postgres psql -U agora_user -d agora_db

postgres-backup: ## Crear backup de PostgreSQL
	@echo "Creando backup de PostgreSQL..."
	@mkdir -p backups
	@docker-compose -f $(POSTGRES_COMPOSE_FILE) exec postgres pg_dump -U agora_user agora_db > ./backups/postgres_backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup de PostgreSQL creado en ./backups/"

postgres-status: ## Mostrar estado de servicios PostgreSQL
	docker-compose -f $(POSTGRES_COMPOSE_FILE) ps

restart: ## Reiniciar servicios
	docker-compose restart

logs: ## Ver logs en tiempo real
	docker-compose logs -f $(SERVICE_NAME)

clean: ## Limpiar contenedores, imágenes y volúmenes no utilizados
	docker-compose down -v
	docker system prune -af
	docker volume prune -f

test: ## Ejecutar pruebas en el contenedor
	docker-compose exec $(SERVICE_NAME) python -m pytest

health: ## Verificar el estado de salud de la aplicación
	@echo "Verificando health check..."
	@curl -f http://localhost:8000/health || echo "❌ Health check falló"
	@echo "Verificando estado del contenedor..."
	@docker-compose ps $(SERVICE_NAME)

backup: ## Crear backup de la base de datos
	@echo "Creando backup..."
	@mkdir -p backups
	@docker cp $(CONTAINER_NAME):/app/data/iph_database.db ./backups/backup_$(shell date +%Y%m%d_%H%M%S).db
	@echo "✅ Backup creado en ./backups/"

restore: ## Restaurar backup (especificar archivo con BACKUP_FILE=archivo.db)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Especifica el archivo de backup: make restore BACKUP_FILE=backup_file.db"; \
		exit 1; \
	fi
	@echo "Restaurando backup: $(BACKUP_FILE)"
	@docker cp $(BACKUP_FILE) $(CONTAINER_NAME):/app/data/iph_database.db
	@echo "✅ Backup restaurado"

shell: ## Acceder al shell del contenedor
	docker-compose exec $(SERVICE_NAME) bash

init-db: ## Reinicializar la base de datos
	docker-compose exec $(SERVICE_NAME) python init_db.py

dev: ## Iniciar en modo desarrollo (con hot reload)
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

prod: ## Iniciar en modo producción
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

status: ## Mostrar estado de todos los servicios
	@echo "=== Estado de contenedores ==="
	@docker-compose ps
	@echo "\n=== Uso de recursos ==="
	@docker stats --no-stream $(CONTAINER_NAME)

deploy: build up ## Construir y desplegar la aplicación
	@echo "🚀 Aplicación desplegada en http://localhost:8000"
	@echo "📚 Documentación disponible en http://localhost:8000/docs"