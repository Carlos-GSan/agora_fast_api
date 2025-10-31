-- Migration: Agregar delitos como motivos
-- Date: 2025-10-30
-- Description: Insertar delitos específicos en la tabla motivos con tipo_motivo_id = 1 (Delito)

-- Insertar los delitos como motivos
INSERT INTO motivos (motivo, tipo_motivo_id) VALUES 
('Robo de vehículo', 1),
('Robo a comercio', 1),
('Robo en lugar cerrado', 1),
('Robo a casa habitación', 1),
('Homicidio', 1),
('Delitos contra la salud', 1),
('Delitos contra la seguridad pública', 1)
ON CONFLICT (motivo) DO NOTHING;

-- Verificar la inserción
-- SELECT m.id_mot, m.motivo, tm.tipo_motivo 
-- FROM motivos m 
-- JOIN tipo_motivo tm ON m.tipo_motivo_id = tm.tipo_motivo_id 
-- WHERE tm.tipo_motivo = 'Delito' 
-- ORDER BY m.id_mot;