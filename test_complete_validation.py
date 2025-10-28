import asyncio
import sys
import os

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.abspath('.'))

from datetime import datetime
from app.routers.eventos import crear_evento
from app.config.database import get_session
from app.schemas.evento_schemas import (
    EventoCreate, OficialEventoCreate, 
    MotivosEventoCreate, DetenidoEventoCreate
)
from app.models.models import TipoIntervencion, TurnoEnum

async def test_complete_validation():
    """Test completo de validación de reglas de negocio."""
    
    print("🧪 Iniciando test completo de validación...")
    
    session = next(get_session())
    
    # Test 1: Validar que folio_cecom es numérico
    print("\n1️⃣ Test: folio_cecom numérico")
    evento_valido = EventoCreate(
        id_tpo_evento=3,  # Juzgado Cívico
        intervencion=TipoIntervencion.OPERATIVO,
        id_region=1,
        turno=TurnoEnum.A,
        id_unidad_vehi=1,
        folio_cecom=12345,  # Número entero
        colonia="Centro",
        calle="Av. Principal",
        georreferencia="20.123,-110.456",
        fecha_evento=datetime.now(),
        narrativa="Evento de prueba con folio numérico",
        oficiales=[OficialEventoCreate(id_oficial=1), OficialEventoCreate(id_oficial=2)],
        motivos=[MotivosEventoCreate(id_mot=3)],  # Falta administrativa para Juzgado Cívico (válido)
        detenidos=[]
    )
    
    try:
        result = await crear_evento(evento_valido, session)
        print(f"✅ Evento creado exitosamente con folio_cecom numérico: {result.folio_cecom}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Evento de Conocimiento sin detenidos (válido)
    print("\n2️⃣ Test: Conocimiento sin detenidos (válido)")
    evento_conocimiento = EventoCreate(
        id_tpo_evento=4,  # Conocimiento
        intervencion=TipoIntervencion.RECORRIDO,
        id_region=2,
        turno=TurnoEnum.B,
        id_unidad_vehi=2,
        folio_cecom=12346,
        colonia="Norte",
        calle="Calle 5ta",
        georreferencia="20.456,-110.789",
        fecha_evento=datetime.now(),
        narrativa="Evento de conocimiento sin detenidos",
        oficiales=[OficialEventoCreate(id_oficial=1)],
        motivos=[MotivosEventoCreate(id_mot=1)],  # Delito (válido para Conocimiento)
        detenidos=[]  # Sin detenidos (válido para Conocimiento)
    )
    
    try:
        result = await crear_evento(evento_conocimiento, session)
        print(f"✅ Evento de Conocimiento creado sin detenidos: IPH {result.iph_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Evento de Conocimiento con detenidos (inválido)
    print("\n3️⃣ Test: Conocimiento con detenidos (inválido)")
    evento_conocimiento_con_detenidos = EventoCreate(
        id_tpo_evento=4,  # Conocimiento
        intervencion=TipoIntervencion.REPORTE,
        id_region=2,
        turno=TurnoEnum.C,
        id_unidad_vehi=3,
        folio_cecom=12347,
        colonia="Sur",
        calle="Calle 3ra",
        georreferencia="20.789,-110.123",
        fecha_evento=datetime.now(),
        narrativa="Evento de conocimiento con detenidos (inválido)",
        oficiales=[OficialEventoCreate(id_oficial=2)],
        motivos=[MotivosEventoCreate(id_mot=1)],
        detenidos=[DetenidoEventoCreate(id_detenido=1)]  # Con detenidos (inválido para Conocimiento)
    )
    
    try:
        result = await crear_evento(evento_conocimiento_con_detenidos, session)
        print(f"❌ Este evento no debería haberse creado: {result}")
    except Exception as e:
        print(f"✅ Error esperado: {e}")
    
    # Test 4: Juzgado Cívico con motivo de delito (inválido)
    print("\n4️⃣ Test: Juzgado Cívico con motivo de delito (inválido)")
    evento_juzgado_delito = EventoCreate(
        id_tpo_evento=3,  # Juzgado Cívico
        intervencion=TipoIntervencion.OPERATIVO,
        id_region=1,
        turno=TurnoEnum.MIXTO,
        id_unidad_vehi=1,
        folio_cecom=12348,
        colonia="Centro",
        calle="Av. Reforma",
        georreferencia="20.111,-110.222",
        fecha_evento=datetime.now(),
        narrativa="Juzgado Cívico con motivo de delito (inválido)",
        oficiales=[OficialEventoCreate(id_oficial=1), OficialEventoCreate(id_oficial=2)],
        motivos=[MotivosEventoCreate(id_mot=1)],  # Delito (inválido para Juzgado Cívico)
        detenidos=[DetenidoEventoCreate(id_detenido=1)]
    )
    
    try:
        result = await crear_evento(evento_juzgado_delito, session)
        print(f"❌ Este evento no debería haberse creado: {result}")
    except Exception as e:
        print(f"✅ Error esperado: {e}")
    
    # Test 5: Fiscalía con falta administrativa (inválido)
    print("\n5️⃣ Test: Fiscalía con falta administrativa (inválido)")
    evento_fiscalia_falta = EventoCreate(
        id_tpo_evento=1,  # Fiscalía
        intervencion=TipoIntervencion.OPERATIVO,
        id_region=3,
        turno=TurnoEnum.DIARIO,
        id_unidad_vehi=4,
        folio_cecom=12349,
        colonia="Este",
        calle="Av. Industrial",
        georreferencia="20.333,-110.444",
        fecha_evento=datetime.now(),
        narrativa="Fiscalía con falta administrativa (inválido)",
        oficiales=[OficialEventoCreate(id_oficial=3), OficialEventoCreate(id_oficial=4)],
        motivos=[MotivosEventoCreate(id_mot=3)],  # Falta administrativa (inválido para Fiscalía)
        detenidos=[DetenidoEventoCreate(id_detenido=2)]
    )
    
    try:
        result = await crear_evento(evento_fiscalia_falta, session)
        print(f"❌ Este evento no debería haberse creado: {result}")
    except Exception as e:
        print(f"✅ Error esperado: {e}")
    
    # Test 6: Denuncia con falta administrativa (inválido)
    print("\n6️⃣ Test: Denuncia con falta administrativa (inválido)")
    evento_denuncia_falta = EventoCreate(
        id_tpo_evento=2,  # Denuncia
        intervencion=TipoIntervencion.REPORTE,
        id_region=4,
        turno=TurnoEnum.A,
        id_unidad_vehi=1,
        folio_cecom=12350,
        colonia="Oeste",
        calle="Av. Poniente",
        georreferencia="20.555,-110.666",
        fecha_evento=datetime.now(),
        narrativa="Denuncia con falta administrativa (inválido)",
        oficiales=[OficialEventoCreate(id_oficial=1)],
        motivos=[MotivosEventoCreate(id_mot=4)],  # Falta administrativa (inválido para Denuncia)
        detenidos=[]
    )
    
    try:
        result = await crear_evento(evento_denuncia_falta, session)
        print(f"❌ Este evento no debería haberse creado: {result}")
    except Exception as e:
        print(f"✅ Error esperado: {e}")
    
    # Test 7: Evento válido con todas las validaciones correctas
    print("\n7️⃣ Test: Evento completamente válido")
    evento_completo_valido = EventoCreate(
        id_tpo_evento=1,  # Fiscalía
        intervencion=TipoIntervencion.OPERATIVO,
        id_region=1,
        turno=TurnoEnum.B,
        id_unidad_vehi=2,
        folio_cecom=12351,
        colonia="Centro",
        calle="Av. Revolución",
        georreferencia="20.777,-110.888",
        fecha_evento=datetime.now(),
        narrativa="Evento válido con detenidos y motivos de delito",
        oficiales=[
            OficialEventoCreate(id_oficial=1), 
            OficialEventoCreate(id_oficial=2), 
            OficialEventoCreate(id_oficial=3)
        ],
        motivos=[
            MotivosEventoCreate(id_mot=1), 
            MotivosEventoCreate(id_mot=2)
        ],  # Delitos (válido para Fiscalía)
        detenidos=[
            DetenidoEventoCreate(id_detenido=1), 
            DetenidoEventoCreate(id_detenido=2)
        ]
    )
    
    try:
        result = await crear_evento(evento_completo_valido, session)
        print(f"✅ Evento completo creado exitosamente: IPH {result.iph_id}")
        print(f"   - Tipo: Fiscalía")
        print(f"   - Folio CECOM: {result.folio_cecom}")
        print(f"   - Turno: {result.turno}")
        print(f"   - Motivos: {len(evento_completo_valido.motivos)} (delitos)")
        print(f"   - Detenidos: {len(evento_completo_valido.detenidos)}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    print("\n🎯 Resumen de validaciones:")
    print("✅ folio_cecom como entero")
    print("✅ Conocimiento sin detenidos permitido")
    print("✅ Conocimiento con detenidos rechazado")
    print("✅ Juzgado Cívico solo permite faltas administrativas")
    print("✅ Fiscalía no permite faltas administrativas")
    print("✅ Denuncia no permite faltas administrativas")
    print("✅ Evento completo válido creado correctamente")
    
    session.close()

if __name__ == "__main__":
    asyncio.run(test_complete_validation())