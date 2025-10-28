#!/usr/bin/env python3
"""
Test completo de todas las validaciones
"""
import sys
import os
sys.path.append('/home/dev2/agora_asistente/agora_fast_api')

async def test_todas_las_validaciones():
    from sqlmodel import Session
    from app.config.database import engine
    from app.schemas.evento_schemas import EventoCreate, OficialEventoCreate, DetenidoEventoCreate, MotivosEventoCreate
    from app.routers.eventos import crear_evento
    
    print("=== TEST COMPLETO DE VALIDACIONES ===")
    
    with Session(engine) as session:
        
        # Test 1: Conocimiento SIN detenidos (debe funcionar)
        print("\n1. 🧪 Conocimiento SIN detenidos (debe funcionar):")
        try:
            evento1 = EventoCreate(
                id_tpo_evento=4,  # Conocimiento
                intervencion="recorrido",
                id_region=1,
                turno="A",
                id_unidad_vehi=1,
                folio_cecom="TEST-CONOCIMIENTO-OK",
                narrativa="Test conocimiento sin detenidos",
                oficiales=[OficialEventoCreate(id_oficial=1)],
                detenidos=[],  # SIN detenidos
                motivos=[MotivosEventoCreate(id_mot=1)]
            )
            result = await crear_evento(evento1, session)
            print(f"✅ CORRECTO: Evento creado exitosamente (IPH: {result.iph_id})")
        except Exception as e:
            print(f"❌ ERROR: No debería haber fallado: {e}")
        
        # Test 2: Conocimiento CON detenidos (debe fallar)
        print("\n2. 🧪 Conocimiento CON detenidos (debe fallar):")
        try:
            evento2 = EventoCreate(
                id_tpo_evento=4,  # Conocimiento
                intervencion="recorrido",
                id_region=1,
                turno="A",
                id_unidad_vehi=1,
                folio_cecom="TEST-CONOCIMIENTO-FAIL",
                narrativa="Test conocimiento con detenidos",
                oficiales=[OficialEventoCreate(id_oficial=1)],
                detenidos=[DetenidoEventoCreate(id_detenido=1)],  # CON detenidos
                motivos=[MotivosEventoCreate(id_mot=1)]
            )
            result = await crear_evento(evento2, session)
            print(f"❌ ERROR: Se creó cuando debería haber fallado: {result}")
        except Exception as e:
            print(f"✅ CORRECTO: Falló como esperado: {e}")
        
        # Test 3: Juzgado Cívico con motivo Falta Administrativa (debe funcionar)
        print("\n3. 🧪 Juzgado Cívico con Falta Administrativa (debe funcionar):")
        try:
            evento3 = EventoCreate(
                id_tpo_evento=3,  # Juzgado Cívico
                intervencion="reporte",
                id_region=1,
                turno="B",
                id_unidad_vehi=1,
                folio_cecom="TEST-JUZGADO-OK",
                narrativa="Test juzgado cívico correcto",
                oficiales=[OficialEventoCreate(id_oficial=1)],
                detenidos=[DetenidoEventoCreate(id_detenido=1)],
                motivos=[MotivosEventoCreate(id_mot=3)]  # ID 3 = "Daños a terceros" (Falta Admin)
            )
            result = await crear_evento(evento3, session)
            print(f"✅ CORRECTO: Evento creado exitosamente (IPH: {result.iph_id})")
        except Exception as e:
            print(f"❌ ERROR: No debería haber fallado: {e}")
        
        # Test 4: Juzgado Cívico con motivo Delito (debe fallar)
        print("\n4. 🧪 Juzgado Cívico con Delito (debe fallar):")
        try:
            evento4 = EventoCreate(
                id_tpo_evento=3,  # Juzgado Cívico
                intervencion="reporte",
                id_region=1,
                turno="B",
                id_unidad_vehi=1,
                folio_cecom="TEST-JUZGADO-FAIL",
                narrativa="Test juzgado cívico incorrecto",
                oficiales=[OficialEventoCreate(id_oficial=1)],
                detenidos=[DetenidoEventoCreate(id_detenido=1)],
                motivos=[MotivosEventoCreate(id_mot=1)]  # ID 1 = "Posesión de narcóticos" (Delito)
            )
            result = await crear_evento(evento4, session)
            print(f"❌ ERROR: Se creó cuando debería haber fallado: {result}")
        except Exception as e:
            print(f"✅ CORRECTO: Falló como esperado: {e}")
        
        # Test 5: Detenido inexistente (debe fallar)
        print("\n5. 🧪 Detenido inexistente (debe fallar):")
        try:
            evento5 = EventoCreate(
                id_tpo_evento=1,  # Fiscalía
                intervencion="recorrido",
                id_region=1,
                turno="A",
                id_unidad_vehi=1,
                folio_cecom="TEST-DETENIDO-FAIL",
                narrativa="Test detenido inexistente",
                oficiales=[OficialEventoCreate(id_oficial=1)],
                detenidos=[DetenidoEventoCreate(id_detenido=999)],  # ID 999 no existe
                motivos=[MotivosEventoCreate(id_mot=1)]
            )
            result = await crear_evento(evento5, session)
            print(f"❌ ERROR: Se creó cuando debería haber fallado: {result}")
        except Exception as e:
            print(f"✅ CORRECTO: Falló como esperado: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_todas_las_validaciones())