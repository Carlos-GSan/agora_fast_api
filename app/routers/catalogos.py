from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.models import (
    TpoEvento,
    Region,
    Unidades,
    Oficial,
    Detenido,
    TipoMotivo,
    Motivos,
    Droga,
    Arma
)
from app.schemas.base_schemas import (
    TpoEventoRead, TpoEventoCreate,
    RegionRead, RegionCreate,
    UnidadesRead, UnidadesCreate,
    OficialRead, OficialCreate, OficialUpdate,
    DetenidoRead, DetenidoCreate, DetenidoUpdate,
    TipoMotivoRead, TipoMotivoCreate,
    MotivosRead, MotivosCreate,
    DrogaRead, DrogaCreate,
    ArmaRead, ArmaCreate
)

router = APIRouter(prefix="/catalogos", tags=["catalogos"])

# Endpoints para Tipos de Evento
@router.post("/tipos-evento/", response_model=TpoEventoRead, status_code=status.HTTP_201_CREATED)
async def crear_tipo_evento(tipo_evento: TpoEventoCreate, session: Session = Depends(get_session)):
    db_tipo = TpoEvento(**tipo_evento.model_dump())
    session.add(db_tipo)
    session.commit()
    session.refresh(db_tipo)
    return db_tipo

@router.get("/tipos-evento/", response_model=List[TpoEventoRead], operation_id="get_tipos_evento")
async def obtener_tipos_evento(session: Session = Depends(get_session)):
    statement = select(TpoEvento)
    tipos = session.exec(statement).all()
    return tipos

# Endpoints para Regiones
@router.post("/regiones/", response_model=RegionRead, status_code=status.HTTP_201_CREATED)
async def crear_region(region: RegionCreate, session: Session = Depends(get_session)):
    db_region = Region(**region.model_dump())
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region

@router.get("/regiones/", response_model=List[RegionRead], operation_id="get_regiones")
async def obtener_regiones(session: Session = Depends(get_session)):
    statement = select(Region)
    regiones = session.exec(statement).all()
    return regiones

# Endpoints para Unidades
@router.post("/unidades/", response_model=UnidadesRead, status_code=status.HTTP_201_CREATED)
async def crear_unidad(unidad: UnidadesCreate, session: Session = Depends(get_session)):
    db_unidad = Unidades(**unidad.model_dump())
    session.add(db_unidad)
    session.commit()
    session.refresh(db_unidad)
    return db_unidad

@router.get("/unidades/", response_model=List[UnidadesRead], operation_id="get_unidades")
async def obtener_unidades(activo: bool = None, session: Session = Depends(get_session)):
    statement = select(Unidades)
    if activo is not None:
        statement = statement.where(Unidades.activo == activo)
    unidades = session.exec(statement).all()
    return unidades

# Endpoints para Oficiales
@router.post("/oficiales/", response_model=OficialRead, status_code=status.HTTP_201_CREATED)
async def crear_oficial(oficial: OficialCreate, session: Session = Depends(get_session)):
    try:
        db_oficial = Oficial(**oficial.model_dump())
        session.add(db_oficial)
        session.commit()
        session.refresh(db_oficial)
        return db_oficial
    except Exception as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear oficial: {str(e)}"
        )

@router.get("/oficiales/", response_model=List[OficialRead], operation_id="get_oficiales")
async def obtener_oficiales(session: Session = Depends(get_session)):
    statement = select(Oficial)
    oficiales = session.exec(statement).all()
    return oficiales

@router.put("/oficiales/{id_oficial}", response_model=OficialRead, operation_id="upd_oficial")
async def actualizar_oficial(
    id_oficial: int,
    oficial_update: OficialUpdate,
    session: Session = Depends(get_session)
):
    db_oficial = session.get(Oficial, id_oficial)
    if not db_oficial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oficial no encontrado"
        )
    
    try:
        update_data = oficial_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_oficial, field, value)
        
        session.add(db_oficial)
        session.commit()
        session.refresh(db_oficial)
        return db_oficial
    except Exception as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar oficial: {str(e)}"
        )

@router.get("/oficiales/telegram/{id_telegram}", response_model=OficialRead, status_code=status.HTTP_202_ACCEPTED)
async def buscar_oficial_por_telegram(id_telegram: int, session: Session = Depends(get_session)):
    """
    Buscar un oficial por su ID de Telegram.
    
    - **id_telegram**: ID de Telegram del oficial a buscar
    
    Retorna 202 ACCEPTED si encuentra el oficial, 404 NOT FOUND si no existe.
    """
    statement = select(Oficial).where(Oficial.id_telegram == id_telegram)
    oficial = session.exec(statement).first()
    
    if not oficial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un oficial con ID de Telegram: {id_telegram}"
        )
    
    return oficial

# Endpoints para Detenidos
@router.post("/detenidos/", response_model=DetenidoRead, status_code=status.HTTP_201_CREATED, operation_id="crear_detenido")
async def crear_detenido(detenido: DetenidoCreate, session: Session = Depends(get_session)):
    db_detenido = Detenido(**detenido.model_dump())
    session.add(db_detenido)
    session.commit()
    session.refresh(db_detenido)
    return db_detenido

@router.get("/detenidos/", response_model=List[DetenidoRead], operation_id="get_detenidos")
async def obtener_detenidos(session: Session = Depends(get_session)):
    statement = select(Detenido)
    detenidos = session.exec(statement).all()
    return detenidos

@router.put("/detenidos/{id_detenido}", response_model=DetenidoRead)
async def actualizar_detenido(
    id_detenido: int,
    detenido_update: DetenidoUpdate,
    session: Session = Depends(get_session)
):
    db_detenido = session.get(Detenido, id_detenido)
    if not db_detenido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detenido no encontrado"
        )
    
    update_data = detenido_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_detenido, field, value)
    
    session.add(db_detenido)
    session.commit()
    session.refresh(db_detenido)
    return db_detenido

# Endpoints para Tipos de Motivo
@router.post("/tipos-motivo/", response_model=TipoMotivoRead, status_code=status.HTTP_201_CREATED)
async def crear_tipo_motivo(tipo_motivo: TipoMotivoCreate, session: Session = Depends(get_session)):
    db_tipo_motivo = TipoMotivo(**tipo_motivo.model_dump())
    session.add(db_tipo_motivo)
    session.commit()
    session.refresh(db_tipo_motivo)
    return db_tipo_motivo

@router.get("/tipos-motivo/", response_model=List[TipoMotivoRead], operation_id="get_tipos_motivo")
async def obtener_tipos_motivo(session: Session = Depends(get_session)):
    statement = select(TipoMotivo)
    tipos_motivo = session.exec(statement).all()
    return tipos_motivo

# Endpoints para Motivos
@router.post("/motivos/", response_model=MotivosRead, status_code=status.HTTP_201_CREATED)
async def crear_motivo(motivo: MotivosCreate, session: Session = Depends(get_session)):
    db_motivo = Motivos(**motivo.model_dump())
    session.add(db_motivo)
    session.commit()
    session.refresh(db_motivo)
    return db_motivo

@router.get("/motivos/", response_model=List[MotivosRead], operation_id="get_motivos_catalogo")
async def obtener_motivos(tipo_motivo_id: int = None, session: Session = Depends(get_session)):
    statement = select(Motivos)
    if tipo_motivo_id:
        statement = statement.where(Motivos.tipo_motivo_id == tipo_motivo_id)
    motivos = session.exec(statement).all()
    return motivos

# Endpoints para Drogas
@router.post("/drogas/", response_model=DrogaRead, status_code=status.HTTP_201_CREATED)
async def crear_droga(droga: DrogaCreate, session: Session = Depends(get_session)):
    db_droga = Droga(**droga.model_dump())
    session.add(db_droga)
    session.commit()
    session.refresh(db_droga)
    return db_droga

@router.get("/drogas/", response_model=List[DrogaRead], operation_id="get_drogas_catalogo")
async def obtener_drogas(session: Session = Depends(get_session)):
    statement = select(Droga)
    drogas = session.exec(statement).all()
    return drogas

# Endpoints para Armas
@router.post("/armas/", response_model=ArmaRead, status_code=status.HTTP_201_CREATED)
async def crear_arma(arma: ArmaCreate, session: Session = Depends(get_session)):
    db_arma = Arma(**arma.model_dump())
    session.add(db_arma)
    session.commit()
    session.refresh(db_arma)
    return db_arma

@router.get("/armas/", response_model=List[ArmaRead], operation_id="get_armas_catalogo")
async def obtener_armas(session: Session = Depends(get_session)):
    statement = select(Arma)
    armas = session.exec(statement).all()
    return armas