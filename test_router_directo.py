#!/usr/bin/env python3
"""
Test directo de las validaciones del router
"""
import sys
import os
sys.path.append('/home/dev2/agora_asistente/agora_fast_api')

async def test_validaciones_router():
    from sqlmodel import Session
    from app.config.database import engine
    from app.schemas.evento_schemas import EventoCreate, OficialEventoCreate, DetenidoEventoCreate, MotivosEventoCreate
    from app.routers.eventos import crear_evento
    
    print("=== TEST DIRECTO DE VALIDACIONES ===")
    
    # Evento de Conocimiento CON detenidos (debe fallar)
    evento_data = EventoCreate(
        id_tpo_evento=4,  # Conocimiento
        intervencion="recorrido",
        id_region=1,
        turno="A",
        id_unidad_vehi=1,
        folio_cecom="TEST-DIRECTO",
        narrativa="Test directo",
        oficiales=[OficialEventoCreate(id_oficial=1)],
        detenidos=[DetenidoEventoCreate(id_detenido=1, rnd_detenido="TEST")],  # CON detenidos - DEBE FALLAR
        motivos=[MotivosEventoCreate(id_mot=1)]
    )
    
    with Session(engine) as session:
        try:
            result = await crear_evento(evento_data, session)
            print(f"❌ ERROR: Se creó el evento cuando debería haber fallado: {result}")
        except Exception as e:
            print(f"✅ CORRECTO: El evento falló como esperado: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_validaciones_router())