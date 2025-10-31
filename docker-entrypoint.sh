#!/bin/bash

# Script de inicialización para el contenedor Docker

echo "=== Iniciando Sistema IPH ==="

# Determinar el tipo de base de datos
if [[ "$DATABASE_URL" == postgresql* ]]; then
    echo "🐘 Configuración detectada: PostgreSQL"
    DB_TYPE="postgresql"
elif [[ "$DATABASE_URL" == sqlite* ]]; then
    echo "🗃️ Configuración detectada: SQLite"
    DB_TYPE="sqlite"
else
    echo "❓ Tipo de base de datos no reconocido, asumiendo SQLite"
    DB_TYPE="sqlite"
fi

# Configuración específica para SQLite
if [ "$DB_TYPE" = "sqlite" ]; then
    # Crear directorio de datos si no existe
    mkdir -p /app/data
    
    # Verificar si la base de datos SQLite existe, si no, inicializarla
    if [ ! -f "/app/data/iph_database.db" ]; then
        echo "🔧 Base de datos SQLite no encontrada. Inicializando..."
        python init_db.py
        echo "✅ Base de datos SQLite inicializada correctamente"
    else
        echo "📄 Base de datos SQLite existente encontrada"
    fi
fi

# Configuración específica para PostgreSQL
if [ "$DB_TYPE" = "postgresql" ]; then
    echo "⏳ Esperando a que PostgreSQL esté disponible..."
    
    # Esperar a que PostgreSQL esté disponible
    while ! python -c "
import psycopg2
import os
import time
from urllib.parse import urlparse

def wait_for_postgres():
    url = os.getenv('DATABASE_URL')
    parsed = urlparse(url)
    
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:]  # Remove leading slash
            )
            conn.close()
            print('✅ PostgreSQL está disponible')
            return True
        except psycopg2.OperationalError as e:
            print(f'⏳ Esperando PostgreSQL... intento {retry_count + 1}/{max_retries}')
            time.sleep(2)
            retry_count += 1
    
    print('❌ No se pudo conectar a PostgreSQL después de varios intentos')
    return False

wait_for_postgres()
"; do
        echo "⏳ PostgreSQL no está listo aún, esperando..."
        sleep 2
    done
    
    echo "🔧 Inicializando esquema de base de datos PostgreSQL..."
    python init_db.py
    echo "✅ Base de datos PostgreSQL inicializada correctamente"
fi

# Verificar la conectividad de la base de datos
echo "🔍 Verificando conectividad de la base de datos..."
python -c "
from app.config.database import engine
from sqlmodel import text

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Conexión a la base de datos exitosa')
except Exception as e:
    print(f'❌ Error de conexión a la base de datos: {e}')
    exit(1)
"

echo "🚀 Iniciando servidor FastAPI..."

# Ejecutar la aplicación
exec python main.py