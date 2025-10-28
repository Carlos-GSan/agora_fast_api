from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List

# Esquemas para relaciones de eventos
class OficialEventoCreate(SQLModel):
    id_oficial: int

class DetenidoEventoCreate(SQLModel):
    id_detenido: int
    rnd_detenido: Optional[str] = None

class MotivosEventoCreate(SQLModel):
    id_mot: int

class DrogaDetenidoEventoCreate(SQLModel):
    id_droga: int
    cantidad: Optional[float] = None
    tipo_cantidad: Optional[str] = None

class ArmaDetenidoEventoCreate(SQLModel):
    id_arma: int
    cantidad: Optional[int] = None

# Esquemas principales para Evento
class EventoCreate(SQLModel):
    id_tpo_evento: int
    id_intervencion: int
    id_region: int
    turno: Optional[str] = None
    id_unidad_vehi: Optional[int] = None
    folio_cecom: Optional[str] = None
    colonia: Optional[str] = None
    calle: Optional[str] = None
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None
    
    # Listas de relaciones para crear junto con el evento
    oficiales: Optional[List[OficialEventoCreate]] = []
    detenidos: Optional[List[DetenidoEventoCreate]] = []
    motivos: Optional[List[MotivosEventoCreate]] = []

class EventoUpdate(SQLModel):
    id_tpo_evento: Optional[int] = None
    id_intervencion: Optional[int] = None
    id_region: Optional[int] = None
    turno: Optional[str] = None
    id_unidad_vehi: Optional[int] = None
    folio_cecom: Optional[str] = None
    colonia: Optional[str] = None
    calle: Optional[str] = None
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None

class EventoRead(SQLModel):
    iph_id: int
    id_tpo_evento: Optional[int] = None
    id_intervencion: Optional[int] = None
    id_region: Optional[int] = None
    turno: Optional[str] = None
    id_unidad_vehi: Optional[int] = None
    folio_cecom: Optional[str] = None
    colonia: Optional[str] = None
    calle: Optional[str] = None
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None

# Esquema con relaciones completas (para respuestas detalladas)
class EventoReadWithRelations(EventoRead):
    # Las relaciones se incluirán automáticamente cuando se carguen desde la base de datos
    pass