#!/bin/bash

# Script de inicialización para el contenedor Docker

echo "=== Iniciando Sistema IPH ==="

# Crear directorio de datos si no existe
mkdir -p /app/data

# Verificar si la base de datos existe, si no, inicializarla
if [ ! -f "/app/data/iph_database.db" ]; then
    echo "🔧 Base de datos no encontrada. Inicializando..."
    python init_db.py
    echo "✅ Base de datos inicializada correctamente"
else
    echo "📄 Base de datos existente encontrada"
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