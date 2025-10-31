-- Script de inicialización para PostgreSQL
-- Este script se ejecuta automáticamente cuando se crea la base de datos

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configuraciones adicionales para el rendimiento
ALTER DATABASE agora_db SET timezone = 'America/Mexico_City';

-- Comentario informativo
COMMENT ON DATABASE agora_db IS 'Base de datos del Sistema IPH (Informe Policial Homologado)';