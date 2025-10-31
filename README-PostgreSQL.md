# 🐘 Configuración de PostgreSQL

## Campos Agregados al Modelo Evento

Se han agregado dos nuevos campos al modelo `Evento`:

- **`cuadrante`**: `Optional[str]` - Cuadrante del evento
- **`region_geo`**: `Optional[str]` - Región geográfica del evento

## Base de Datos Soportadas

La aplicación ahora soporta tanto **SQLite** como **PostgreSQL**:

### 🗃️ SQLite (por defecto)
- Base de datos ligera y sin configuración adicional
- Ideal para desarrollo y pruebas
- Los datos se almacenan en `./data/iph_database.db`

### 🐘 PostgreSQL 
- Base de datos robusta para producción
- Mejor rendimiento y funcionalidades avanzadas
- Configuración automática con Docker Compose

## 🚀 Despliegue

### SQLite (por defecto)
```bash
# Usar el docker-compose estándar
docker-compose up -d --build

# O con Make
make up
```

### PostgreSQL
```bash
# Usar el docker-compose específico de PostgreSQL
docker-compose -f docker-compose.postgres.yml up -d --build

# O con Make
make postgres-up
```

## ⚙️ Configuración

### Variables de Entorno

Para **SQLite**:
```env
DATABASE_URL=sqlite:///./data/iph_database.db
```

Para **PostgreSQL**:
```env
DATABASE_URL=postgresql://agora_user:agora_password@localhost:5432/agora_db
```

### Configuración Automática

La aplicación detecta automáticamente el tipo de base de datos basándose en la URL de conexión y configura el motor de SQLAlchemy apropiadamente.

## 🛠️ Comandos Útiles

### PostgreSQL con Make

```bash
# Iniciar PostgreSQL
make postgres-up

# Ver logs
make postgres-logs

# Acceder a la consola de PostgreSQL
make postgres-shell

# Crear backup
make postgres-backup

# Parar servicios
make postgres-down

# Ver estado
make postgres-status
```

### PostgreSQL Manual

```bash
# Iniciar servicios
docker-compose -f docker-compose.postgres.yml up -d

# Acceder a PostgreSQL directamente
docker-compose -f docker-compose.postgres.yml exec postgres psql -U agora_user -d agora_db

# Ver logs de PostgreSQL
docker-compose -f docker-compose.postgres.yml logs postgres

# Crear backup
docker-compose -f docker-compose.postgres.yml exec postgres pg_dump -U agora_user agora_db > backup.sql

# Restaurar backup
docker-compose -f docker-compose.postgres.yml exec -T postgres psql -U agora_user -d agora_db < backup.sql
```

## 📊 Estructura de la Base de Datos

### Nuevos Campos en la Tabla `evento`

```sql
-- SQLite
ALTER TABLE evento ADD COLUMN cuadrante TEXT;
ALTER TABLE evento ADD COLUMN region_geo TEXT;

-- PostgreSQL
ALTER TABLE evento ADD COLUMN cuadrante VARCHAR;
ALTER TABLE evento ADD COLUMN region_geo VARCHAR;
```

### Esquemas Actualizados

Los esquemas Pydantic han sido actualizados para incluir los nuevos campos:

- `EventoCreate`
- `EventoUpdate` 
- `EventoRead`

## 🔧 Migración

### De SQLite a PostgreSQL

1. **Crear backup de SQLite**:
   ```bash
   make backup
   ```

2. **Iniciar PostgreSQL**:
   ```bash
   make postgres-up
   ```

3. **Migrar datos** (script personalizado requerido)

### De PostgreSQL a SQLite

1. **Crear backup de PostgreSQL**:
   ```bash
   make postgres-backup
   ```

2. **Cambiar configuración** en `.env`:
   ```env
   DATABASE_URL=sqlite:///./data/iph_database.db
   ```

3. **Reiniciar con SQLite**:
   ```bash
   make up
   ```

## 🔍 Verificación

### Health Checks

Ambas configuraciones incluyen health checks automáticos:

```bash
# Verificar estado de la aplicación
curl http://localhost:8000/health

# Verificar estado con Make
make health
```

### Conectividad de Base de Datos

El script de entrada (`docker-entrypoint.sh`) verifica automáticamente:

1. **Disponibilidad del servidor** de base de datos
2. **Conectividad** desde la aplicación
3. **Inicialización** del esquema si es necesario

## 📝 Notas de Desarrollo

### Configuración del Motor

La configuración del motor SQLAlchemy se adapta automáticamente:

**SQLite**:
- `check_same_thread=False`
- Optimizado para desarrollo

**PostgreSQL**:
- `pool_pre_ping=True`
- `pool_recycle=300`
- Optimizado para producción

### Dependencias

Agregadas al `requirements.txt`:
- `psycopg2-binary==2.9.9` - Driver de PostgreSQL

### Docker

El Dockerfile incluye:
- `libpq-dev` - Librerías de desarrollo de PostgreSQL
- `postgresql-client` - Cliente de PostgreSQL

## 🚨 Consideraciones de Producción

### PostgreSQL en Producción

1. **Configurar variables de entorno** seguras
2. **Usar volúmenes persistentes** para datos
3. **Configurar backups** automáticos
4. **Monitorear rendimiento** y conexiones
5. **Configurar SSL/TLS** para conexiones

### Seguridad

1. Cambiar credenciales por defecto
2. Configurar firewall para el puerto 5432
3. Usar conexiones SSL
4. Implementar rotación de passwords
5. Configurar roles y permisos apropiados

## 📚 Recursos Adicionales

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [FastAPI Database Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Docker Compose PostgreSQL](https://hub.docker.com/_/postgres)