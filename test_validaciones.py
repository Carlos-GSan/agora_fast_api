#!/usr/bin/env python3
"""
Script para probar las validaciones directamente
"""
import sys
import os
sys.path.append('/home/dev2/agora_asistente/agora_fast_api')

from app.schemas.evento_schemas import EventoCreate, OficialEventoCreate, DetenidoEventoCreate, MotivosEventoCreate

def test_validaciones():
    print("=== PRUEBAS DE VALIDACIÓN ===")
    
    # Prueba 1: Evento de Conocimiento SIN detenidos (debería funcionar)
    print("\n1. Evento Conocimiento SIN detenidos:")
    try:
        evento_conocimiento_sin_detenidos = EventoCreate(
            id_tpo_evento=4,
            intervencion="recorrido",
            id_region=1,
            turno="A",
            id_unidad_vehi=1,
            folio_cecom="TEST-001",
            narrativa="Test sin detenidos",
            oficiales=[OficialEventoCreate(id_oficial=1)],
            detenidos=[],  # Sin detenidos
            motivos=[MotivosEventoCreate(id_mot=1)]
        )
        print("✅ Validación Pydantic pasó correctamente")
        print(f"Detenidos: {evento_conocimiento_sin_detenidos.detenidos}")
    except Exception as e:
        print(f"❌ Error en validación Pydantic: {e}")
    
    # Prueba 2: Evento de Conocimiento CON detenidos
    print("\n2. Evento Conocimiento CON detenidos:")
    try:
        evento_conocimiento_con_detenidos = EventoCreate(
            id_tpo_evento=4,
            intervencion="recorrido",
            id_region=1,
            turno="A",
            id_unidad_vehi=1,
            folio_cecom="TEST-002",
            narrativa="Test con detenidos",
            oficiales=[OficialEventoCreate(id_oficial=1)],
            detenidos=[DetenidoEventoCreate(id_detenido=1, rnd_detenido="TEST-001")],  # CON detenidos
            motivos=[MotivosEventoCreate(id_mot=1)]
        )
        print("✅ Validación Pydantic pasó (esto está bien, la validación de negocio es en el router)")
        print(f"Detenidos: {len(evento_conocimiento_con_detenidos.detenidos)}")
    except Exception as e:
        print(f"❌ Error en validación Pydantic: {e}")

if __name__ == "__main__":
    test_validaciones()