# 🐳 Despliegue con Docker

Este archivo contiene las instrucciones para desplegar la aplicación Sistema IPH usando Docker.

## 📋 Prerrequisitos

- Docker Engine 20.x o superior
- Docker Compose 2.x o superior

## 🚀 Despliegue Rápido

### 1. Construir y ejecutar con Docker Compose

```bash
# Clonar el repositorio (si no lo tienes)
git clone <tu-repositorio>
cd agora_fast_api

# Construir y ejecutar
docker-compose up -d --build
```

### 2. Verificar que la aplicación está funcionando

```bash
# Verificar el estado de los contenedores
docker-compose ps

# Verificar logs
docker-compose logs -f agora-api

# Probar la API
curl http://localhost:8000/health
```

## 🔧 Comandos Útiles

### Gestión de contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Parar servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f agora-api

# Acceder al contenedor
docker-compose exec agora-api bash
```

### Gestión de base de datos

```bash
# Reinicializar la base de datos
docker-compose exec agora-api python init_db.py

# Backup de la base de datos
docker cp agora-fastapi:/app/data/iph_database.db ./backup_$(date +%Y%m%d_%H%M%S).db
```

## 🗂️ Estructura de archivos Docker

```
.
├── Dockerfile              # Imagen de la aplicación
├── docker-compose.yml      # Orquestación de servicios
├── docker-entrypoint.sh    # Script de inicialización
├── .dockerignore           # Archivos a ignorar en build
└── data/                   # Volumen persistente para BD
    └── iph_database.db     # Base de datos SQLite
```

## ⚙️ Variables de Entorno

Las siguientes variables pueden configurarse en el archivo `.env`:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./data/iph_database.db` |
| `SECRET_KEY` | Clave secreta para JWT | `your-secret-key-here` |
| `ALGORITHM` | Algoritmo de encriptación | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token | `30` |
| `DEBUG` | Modo debug | `False` |

## 🔄 Actualización de la aplicación

```bash
# Parar contenedores
docker-compose down

# Reconstruir imagen con cambios
docker-compose build --no-cache

# Reiniciar servicios
docker-compose up -d
```

## 📊 Monitoreo y Salud

La aplicación incluye un endpoint de health check en `/health` que se usa para:

- Health checks de Docker
- Monitoreo del estado de la aplicación
- Load balancer health checks

```bash
# Verificar health check
curl http://localhost:8000/health
```

## 🔒 Consideraciones de Seguridad

### Para Producción:

1. **Cambiar SECRET_KEY**: Generar una clave segura
2. **Configurar HTTPS**: Usar un proxy reverso (nginx, traefik)
3. **Limitar puertos**: No exponer puertos innecesarios
4. **Variables de entorno**: Usar Docker secrets o archivos .env seguros
5. **Base de datos**: Considerar PostgreSQL para producción

### Generar SECRET_KEY segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🗄️ Base de Datos PostgreSQL (Opcional)

Para usar PostgreSQL en lugar de SQLite, descomenta la sección de PostgreSQL en `docker-compose.yml` y actualiza la variable `DATABASE_URL`:

```env
DATABASE_URL=postgresql://agora_user:agora_password@postgres:5432/agora_db
```

## 🐛 Troubleshooting

### Problemas comunes:

1. **Puerto ocupado**:
   ```bash
   # Cambiar puerto en docker-compose.yml
   ports:
     - "8001:8000"  # Usar puerto 8001 en lugar de 8000
   ```

2. **Permisos de archivos**:
   ```bash
   # Dar permisos al script
   chmod +x docker-entrypoint.sh
   ```

3. **Base de datos corrupta**:
   ```bash
   # Eliminar y recrear
   docker-compose down
   rm -rf data/
   docker-compose up -d
   ```

## 📞 Soporte

Para problemas específicos de Docker, revisar:
- Logs del contenedor: `docker-compose logs agora-api`
- Estado de salud: `docker-compose ps`
- Recursos del sistema: `docker stats`