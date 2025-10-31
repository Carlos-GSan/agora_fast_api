-- Migration: Fix telegram ID to support large values
-- Date: 2025-10-30
-- Issue: ID de Telegram excede el rango de integer en PostgreSQL

-- Cambiar el tipo de dato de id_telegram de integer a bigint
ALTER TABLE oficial ALTER COLUMN id_telegram TYPE BIGINT;

-- Verificar el cambio
-- \d oficial

-- Notas:
-- Los IDs de Telegram pueden ser muy grandes (hasta 64 bits)
-- El tipo integer en PostgreSQL solo soporta hasta 2,147,483,647
-- El tipo bigint soporta hasta 9,223,372,036,854,775,807