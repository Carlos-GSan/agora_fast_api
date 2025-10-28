from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.models import (
    Evento, OficialEvento, DetenidoEvento, MotivosEvento,
    TpoEvento, Region, Unidades, Oficial, Motivos, Detenido, TipoMotivo
)
from app.schemas.evento_schemas import (
    EventoRead, EventoCreate, EventoUpdate, EventoReadWithRelations
)

router = APIRouter(prefix="/eventos", tags=["eventos"])

@router.post("/", response_model=EventoRead, status_code=status.HTTP_201_CREATED)
async def crear_evento(
    evento: EventoCreate,
    session: Session = Depends(get_session)
):
    """
    Crear un nuevo evento con asignación automática de folio IPH
    """
    try:
        # Validar que el tipo de evento existe
        tipo_evento = session.get(TpoEvento, evento.id_tpo_evento)
        if not tipo_evento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de evento con ID {evento.id_tpo_evento} no existe"
            )
        
        # Validar que la región existe
        region = session.get(Region, evento.id_region)
        if not region:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Región con ID {evento.id_region} no existe"
            )
        
        # Validar que la unidad vehicular existe
        unidad = session.get(Unidades, evento.id_unidad_vehi)
        if not unidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unidad vehicular con ID {evento.id_unidad_vehi} no existe"
            )
        
        # Validar que todos los oficiales existen
        oficiales_ids = [oficial.id_oficial for oficial in evento.oficiales]
        statement = select(Oficial).where(Oficial.id_oficial.in_(oficiales_ids))
        oficiales_existentes = session.exec(statement).all()
        if len(oficiales_existentes) != len(oficiales_ids):
            oficiales_existentes_ids = [o.id_oficial for o in oficiales_existentes]
            oficiales_no_encontrados = [id_oficial for id_oficial in oficiales_ids if id_oficial not in oficiales_existentes_ids]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Los siguientes oficiales no existen: {oficiales_no_encontrados}"
            )
        
        # Validar que todos los motivos existen
        motivos_ids = [motivo.id_mot for motivo in evento.motivos]
        statement = select(Motivos).where(Motivos.id_mot.in_(motivos_ids))
        motivos_existentes = session.exec(statement).all()
        if len(motivos_existentes) != len(motivos_ids):
            motivos_existentes_ids = [m.id_mot for m in motivos_existentes]
            motivos_no_encontrados = [id_motivo for id_motivo in motivos_ids if id_motivo not in motivos_existentes_ids]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Los siguientes motivos no existen: {motivos_no_encontrados}"
            )
        
        # Validar que los detenidos existen (si se proporcionan)
        if evento.detenidos:
            detenidos_ids = [detenido.id_detenido for detenido in evento.detenidos]
            statement = select(Detenido).where(Detenido.id_detenido.in_(detenidos_ids))
            detenidos_existentes = session.exec(statement).all()
            if len(detenidos_existentes) != len(detenidos_ids):
                detenidos_existentes_ids = [d.id_detenido for d in detenidos_existentes]
                detenidos_no_encontrados = [id_detenido for id_detenido in detenidos_ids if id_detenido not in detenidos_existentes_ids]
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Los siguientes detenidos no existen: {detenidos_no_encontrados}"
                )
        
        # Validaciones específicas por tipo de evento
        # Regla 1: Eventos tipo "Conocimiento" (ID=4) no pueden tener detenidos
        if evento.id_tpo_evento == 4 and evento.detenidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los eventos de tipo 'Conocimiento' no pueden tener detenidos"
            )
        
        # Regla 2: Eventos tipo "Juzgado Cívico" (ID=3) solo pueden tener motivos de "Falta Administrativa" (tipo_motivo_id=2)
        if evento.id_tpo_evento == 3:
            # Verificar que todos los motivos sean de tipo "Falta Administrativa"
            for motivo in motivos_existentes:
                if motivo.tipo_motivo_id != 2:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Los eventos de tipo 'Juzgado Cívico' solo pueden tener motivos de tipo 'Falta Administrativa'. El motivo '{motivo.motivo}' es de tipo 'Delito'"
                    )
        
        # Regla 3: Eventos tipo Fiscalía (ID=1), Denuncia (ID=2) y Conocimiento (ID=4) NO pueden tener motivos de "Falta Administrativa"
        if evento.id_tpo_evento in [1, 2, 4]:
            tipo_evento_nombres = {1: "Fiscalía", 2: "Denuncia", 4: "Conocimiento"}
            tipo_evento_nombre = tipo_evento_nombres[evento.id_tpo_evento]
            
            # Verificar que ningún motivo sea de tipo "Falta Administrativa"
            for motivo in motivos_existentes:
                if motivo.tipo_motivo_id == 2:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Los eventos de tipo '{tipo_evento_nombre}' no pueden tener motivos de tipo 'Falta Administrativa'. El motivo '{motivo.motivo}' debe ser de tipo 'Delito'"
                    )
        
        # Crear el evento principal
        evento_data = evento.model_dump(exclude={"oficiales", "detenidos", "motivos"})
        db_evento = Evento(**evento_data)
        session.add(db_evento)
        session.flush()  # Para obtener el iph_id generado
        
        # Agregar oficiales al evento
        for oficial_data in evento.oficiales:
            oficial_evento = OficialEvento(
                iph_id=db_evento.iph_id,
                id_oficial=oficial_data.id_oficial
            )
            session.add(oficial_evento)
        
        # Agregar detenidos al evento (opcional)
        if evento.detenidos:
            for detenido_data in evento.detenidos:
                detenido_evento = DetenidoEvento(
                    iph_id=db_evento.iph_id,
                    id_detenido=detenido_data.id_detenido,
                    rnd_detenido=detenido_data.rnd_detenido
                )
                session.add(detenido_evento)
        
        # Agregar motivos al evento
        for motivo_data in evento.motivos:
            motivo_evento = MotivosEvento(
                iph_id=db_evento.iph_id,
                id_mot=motivo_data.id_mot
            )
            session.add(motivo_evento)
        
        session.commit()
        session.refresh(db_evento)
        
        return db_evento
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el evento: {str(e)}"
        )

@router.get("/", response_model=List[EventoRead])
async def obtener_eventos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    Obtener lista de eventos con paginación
    """
    statement = select(Evento).offset(skip).limit(limit)
    eventos = session.exec(statement).all()
    return eventos

@router.get("/{iph_id}", response_model=EventoReadWithRelations)
async def obtener_evento(
    iph_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtener un evento específico por su IPH ID con todas las relaciones
    """
    evento = session.get(Evento, iph_id)
    
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con IPH ID {iph_id} no encontrado"
        )
    
    return evento

@router.put("/{iph_id}", response_model=EventoRead)
async def actualizar_evento(
    iph_id: int,
    evento_update: EventoUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualizar un evento existente
    """
    db_evento = session.get(Evento, iph_id)
    
    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con IPH ID {iph_id} no encontrado"
        )
    
    # Actualizar campos proporcionados
    update_data = evento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_evento, field, value)
    
    try:
        session.add(db_evento)
        session.commit()
        session.refresh(db_evento)
        return db_evento
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar el evento: {str(e)}"
        )

@router.delete("/{iph_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(
    iph_id: int,
    session: Session = Depends(get_session)
):
    """
    Eliminar un evento
    """
    db_evento = session.get(Evento, iph_id)
    
    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con IPH ID {iph_id} no encontrado"
        )
    
    try:
        session.delete(db_evento)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar el evento: {str(e)}"
        )

@router.get("/folio/{folio_cecom}", response_model=List[EventoRead])
async def buscar_por_folio_cecom(
    folio_cecom: str,
    session: Session = Depends(get_session)
):
    """
    Buscar eventos por folio CECOM
    """
    statement = select(Evento).where(Evento.folio_cecom.like(f"%{folio_cecom}%"))
    eventos = session.exec(statement).all()
    return eventos

@router.get("/region/{id_region}", response_model=List[EventoRead])
async def obtener_eventos_por_region(
    id_region: int,
    session: Session = Depends(get_session)
):
    """
    Obtener eventos por región
    """
    statement = select(Evento).where(Evento.id_region == id_region)
    eventos = session.exec(statement).all()
    return eventos