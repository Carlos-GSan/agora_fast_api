from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.config.database import get_session
from app.models.models import (
    TpoEvento,
    Intervencion,
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
    IntervencionRead, IntervencionCreate,
    RegionRead, RegionCreate,
    UnidadesRead, UnidadesCreate,
    OficialRead, OficialCreate,
    DetenidoRead, DetenidoCreate,
    TipoMotivoRead, TipoMotivoCreate,
    MotivosRead, MotivosCreate,
    DrogaRead, DrogaCreate,
    ArmaRead, ArmaCreate
)

router = APIRouter(prefix="/catalogos", tags=["catalogos"])

# Endpoints para Tipos de Evento
@router.post("/tipos-evento/", response_model=TpoEventoRead, status_code=status.HTTP_201_CREATED)
async def crear_tipo_evento(tipo_evento: TpoEventoCreate, session: Session = Depends(get_session)):
    db_tipo = TpoEvento(**tipo_evento.dict())
    session.add(db_tipo)
    session.commit()
    session.refresh(db_tipo)
    return db_tipo

@router.get("/tipos-evento/", response_model=List[TpoEventoRead])
async def obtener_tipos_evento(session: Session = Depends(get_session)):
    statement = select(TpoEvento)
    tipos = session.exec(statement).all()
    return tipos

# Endpoints para Intervenciones
@router.post("/intervenciones/", response_model=IntervencionRead, status_code=status.HTTP_201_CREATED)
async def crear_intervencion(intervencion: IntervencionCreate, session: Session = Depends(get_session)):
    db_intervencion = Intervencion(**intervencion.dict())
    session.add(db_intervencion)
    session.commit()
    session.refresh(db_intervencion)
    return db_intervencion

@router.get("/intervenciones/", response_model=List[IntervencionRead])
async def obtener_intervenciones(session: Session = Depends(get_session)):
    statement = select(Intervencion)
    intervenciones = session.exec(statement).all()
    return intervenciones

# Endpoints para Regiones
@router.post("/regiones/", response_model=RegionRead, status_code=status.HTTP_201_CREATED)
async def crear_region(region: RegionCreate, session: Session = Depends(get_session)):
    db_region = Region(**region.dict())
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region

@router.get("/regiones/", response_model=List[RegionRead])
async def obtener_regiones(session: Session = Depends(get_session)):
    statement = select(Region)
    regiones = session.exec(statement).all()
    return regiones

# Endpoints para Unidades
@router.post("/unidades/", response_model=UnidadesRead, status_code=status.HTTP_201_CREATED)
async def crear_unidad(unidad: UnidadesCreate, session: Session = Depends(get_session)):
    db_unidad = Unidades(**unidad.dict())
    session.add(db_unidad)
    session.commit()
    session.refresh(db_unidad)
    return db_unidad

@router.get("/unidades/", response_model=List[UnidadesRead])
async def obtener_unidades(activo: bool = None, session: Session = Depends(get_session)):
    statement = select(Unidades)
    if activo is not None:
        statement = statement.where(Unidades.activo == activo)
    unidades = session.exec(statement).all()
    return unidades

# Endpoints para Oficiales
@router.post("/oficiales/", response_model=OficialRead, status_code=status.HTTP_201_CREATED)
async def crear_oficial(oficial: OficialCreate, session: Session = Depends(get_session)):
    db_oficial = Oficial(**oficial.dict())
    session.add(db_oficial)
    session.commit()
    session.refresh(db_oficial)
    return db_oficial

@router.get("/oficiales/", response_model=List[OficialRead])
async def obtener_oficiales(session: Session = Depends(get_session)):
    statement = select(Oficial)
    oficiales = session.exec(statement).all()
    return oficiales

# Endpoints para Detenidos
@router.post("/detenidos/", response_model=DetenidoRead, status_code=status.HTTP_201_CREATED)
async def crear_detenido(detenido: DetenidoCreate, session: Session = Depends(get_session)):
    db_detenido = Detenido(**detenido.dict())
    session.add(db_detenido)
    session.commit()
    session.refresh(db_detenido)
    return db_detenido

@router.get("/detenidos/", response_model=List[DetenidoRead])
async def obtener_detenidos(session: Session = Depends(get_session)):
    statement = select(Detenido)
    detenidos = session.exec(statement).all()
    return detenidos

# Endpoints para Tipos de Motivo
@router.post("/tipos-motivo/", response_model=TipoMotivoRead, status_code=status.HTTP_201_CREATED)
async def crear_tipo_motivo(tipo_motivo: TipoMotivoCreate, session: Session = Depends(get_session)):
    db_tipo_motivo = TipoMotivo(**tipo_motivo.dict())
    session.add(db_tipo_motivo)
    session.commit()
    session.refresh(db_tipo_motivo)
    return db_tipo_motivo

@router.get("/tipos-motivo/", response_model=List[TipoMotivoRead])
async def obtener_tipos_motivo(session: Session = Depends(get_session)):
    statement = select(TipoMotivo)
    tipos_motivo = session.exec(statement).all()
    return tipos_motivo

# Endpoints para Motivos
@router.post("/motivos/", response_model=MotivosRead, status_code=status.HTTP_201_CREATED)
async def crear_motivo(motivo: MotivosCreate, session: Session = Depends(get_session)):
    db_motivo = Motivos(**motivo.dict())
    session.add(db_motivo)
    session.commit()
    session.refresh(db_motivo)
    return db_motivo

@router.get("/motivos/", response_model=List[MotivosRead])
async def obtener_motivos(tipo_motivo_id: int = None, session: Session = Depends(get_session)):
    statement = select(Motivos)
    if tipo_motivo_id:
        statement = statement.where(Motivos.tipo_motivo_id == tipo_motivo_id)
    motivos = session.exec(statement).all()
    return motivos

# Endpoints para Drogas
@router.post("/drogas/", response_model=DrogaRead, status_code=status.HTTP_201_CREATED)
async def crear_droga(droga: DrogaCreate, session: Session = Depends(get_session)):
    db_droga = Droga(**droga.dict())
    session.add(db_droga)
    session.commit()
    session.refresh(db_droga)
    return db_droga

@router.get("/drogas/", response_model=List[DrogaRead])
async def obtener_drogas(session: Session = Depends(get_session)):
    statement = select(Droga)
    drogas = session.exec(statement).all()
    return drogas

# Endpoints para Armas
@router.post("/armas/", response_model=ArmaRead, status_code=status.HTTP_201_CREATED)
async def crear_arma(arma: ArmaCreate, session: Session = Depends(get_session)):
    db_arma = Arma(**arma.dict())
    session.add(db_arma)
    session.commit()
    session.refresh(db_arma)
    return db_arma

@router.get("/armas/", response_model=List[ArmaRead])
async def obtener_armas(session: Session = Depends(get_session)):
    statement = select(Arma)
    armas = session.exec(statement).all()
    return armas