from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.models import Evento, OficialEvento, DetenidoEvento, MotivosEvento
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
        # Crear el evento principal
        evento_data = evento.model_dump(exclude={"oficiales", "detenidos", "motivos"})
        db_evento = Evento(**evento_data)
        session.add(db_evento)
        session.flush()  # Para obtener el iph_id generado
        
        # Agregar oficiales al evento
        if evento.oficiales:
            for oficial_data in evento.oficiales:
                oficial_evento = OficialEvento(
                    iph_id=db_evento.iph_id,
                    id_oficial=oficial_data.id_oficial
                )
                session.add(oficial_evento)
        
        # Agregar detenidos al evento
        if evento.detenidos:
            for detenido_data in evento.detenidos:
                detenido_evento = DetenidoEvento(
                    iph_id=db_evento.iph_id,
                    id_detenido=detenido_data.id_detenido,
                    rnd_detenido=detenido_data.rnd_detenido
                )
                session.add(detenido_evento)
        
        # Agregar motivos al evento
        if evento.motivos:
            for motivo_data in evento.motivos:
                motivo_evento = MotivosEvento(
                    iph_id=db_evento.iph_id,
                    id_mot=motivo_data.id_mot
                )
                session.add(motivo_evento)
        
        session.commit()
        session.refresh(db_evento)
        
        return db_evento
        
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