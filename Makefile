# Makefile para gestión de Docker del proyecto Agora FastAPI

.PHONY: help build up down restart logs clean test health backup

# Variables
COMPOSE_FILE = docker-compose.yml
SERVICE_NAME = agora-api
CONTAINER_NAME = agora-fastapi

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir la imagen Docker
	docker-compose build --no-cache

up: ## Iniciar servicios en background
	docker-compose up -d

down: ## Parar y eliminar contenedores
	docker-compose down

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