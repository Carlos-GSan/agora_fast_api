-- Migration: Hacer campos obligatorios en tabla evento
-- Date: 2025-10-31
-- Description: Convertir campos principales y geográficos en campos NOT NULL

-- Paso 1: Actualizar registros existentes que tengan valores NULL
UPDATE evento SET 
    colonia = 'No especificada' WHERE colonia IS NULL OR colonia = '';
UPDATE evento SET 
    cuadrante = 'No especificado' WHERE cuadrante IS NULL OR cuadrante = '';
UPDATE evento SET 
    region_geo = 'No especificada' WHERE region_geo IS NULL OR region_geo = '';
UPDATE evento SET 
    delegacion = 'No especificada' WHERE delegacion IS NULL OR delegacion = '';
UPDATE evento SET 
    georreferencia = '0,0' WHERE georreferencia IS NULL OR georreferencia = '';
UPDATE evento SET 
    fecha_evento = NOW() WHERE fecha_evento IS NULL;
UPDATE evento SET 
    narrativa = 'Sin narrativa' WHERE narrativa IS NULL OR narrativa = '';

-- Paso 2: Aplicar restricciones NOT NULL a campos geográficos y narrativa
ALTER TABLE evento ALTER COLUMN colonia SET NOT NULL;
ALTER TABLE evento ALTER COLUMN cuadrante SET NOT NULL;
ALTER TABLE evento ALTER COLUMN region_geo SET NOT NULL;
ALTER TABLE evento ALTER COLUMN delegacion SET NOT NULL;
ALTER TABLE evento ALTER COLUMN georreferencia SET NOT NULL;
ALTER TABLE evento ALTER COLUMN fecha_evento SET NOT NULL;
ALTER TABLE evento ALTER COLUMN narrativa SET NOT NULL;

-- Paso 3: Aplicar restricciones NOT NULL a campos principales
ALTER TABLE evento ALTER COLUMN id_tpo_evento SET NOT NULL;
ALTER TABLE evento ALTER COLUMN intervencion SET NOT NULL;
ALTER TABLE evento ALTER COLUMN id_region SET NOT NULL;
ALTER TABLE evento ALTER COLUMN id_unidad_vehi SET NOT NULL;

-- Verificar cambios
-- \d evento