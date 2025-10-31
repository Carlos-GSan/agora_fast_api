from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.models import TipoIntervencion, TurnoEnum

# Esquemas para relaciones de eventos
class OficialEventoCreate(SQLModel):
    id_oficial: int = Field(..., description="ID del oficial participante")

class DetenidoEventoCreate(SQLModel):
    id_detenido: int = Field(..., description="ID del detenido")
    rnd_detenido: Optional[str] = Field(None, description="Número RND del detenido")

class MotivosEventoCreate(SQLModel):
    id_mot: int = Field(..., description="ID del motivo del evento")

class DrogaDetenidoEventoCreate(SQLModel):
    id_droga: int = Field(..., description="ID del tipo de droga")
    cantidad: Optional[float] = Field(None, description="Cantidad de droga")
    tipo_cantidad: Optional[str] = Field(None, description="Tipo de cantidad (gramos, kilos, etc.)")

class ArmaDetenidoEventoCreate(SQLModel):
    id_arma: int = Field(..., description="ID del tipo de arma")
    cantidad: Optional[int] = Field(None, description="Cantidad de armas")

# Esquemas principales para Evento
class EventoCreate(SQLModel):
    id_tpo_evento: int = Field(..., description="ID del tipo de evento (obligatorio)")
    intervencion: TipoIntervencion = Field(..., description="Tipo de intervención (obligatorio)")
    id_region: int = Field(..., description="ID de la región (obligatorio)")
    turno: Optional[TurnoEnum] = Field(None, description="Turno del evento")
    id_unidad_vehi: int = Field(..., description="ID de la unidad vehicular (obligatorio)")
    folio_cecom: Optional[int] = Field(None, description="Folio CECOM (numérico)")
    colonia: Optional[str] = Field(None, description="Colonia donde ocurrió el evento")
    calle: Optional[str] = Field(None, description="Calle donde ocurrió el evento")
    cuadrante: Optional[str] = Field(None, description="Cuadrante del evento")
    region_geo: Optional[str] = Field(None, description="Región geográfica del evento")
    delegacion: Optional[str] = Field(None, description="Delegación del evento")
    georreferencia: Optional[str] = Field(None, description="Coordenadas GPS del evento")
    fecha_evento: Optional[datetime] = Field(None, description="Fecha y hora del evento")
    narrativa: Optional[str] = Field(None, description="Narrativa del evento")
    
    # Listas de relaciones para crear junto con el evento (obligatorias)
    oficiales: List[OficialEventoCreate] = Field(
        ..., 
        min_items=1, 
        description="Lista de oficiales participantes (obligatorio, al menos 1)"
    )
    detenidos: List[DetenidoEventoCreate] = Field(
        default_factory=list, 
        description="Lista de detenidos"
    )
    motivos: List[MotivosEventoCreate] = Field(
        ..., 
        min_items=1, 
        description="Lista de motivos del evento (obligatorio, al menos 1)"
    )

class EventoUpdate(SQLModel):
    id_tpo_evento: Optional[int] = None
    intervencion: Optional[TipoIntervencion] = None
    id_region: Optional[int] = None
    turno: Optional[TurnoEnum] = None
    id_unidad_vehi: Optional[int] = None
    folio_cecom: Optional[int] = None
    colonia: Optional[str] = None
    calle: Optional[str] = None
    cuadrante: Optional[str] = None
    region_geo: Optional[str] = None
    delegacion: Optional[str] = None
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None

class EventoRead(SQLModel):
    iph_id: int
    id_tpo_evento: Optional[int] = None
    intervencion: Optional[TipoIntervencion] = None
    id_region: Optional[int] = None
    turno: Optional[TurnoEnum] = None
    id_unidad_vehi: Optional[int] = None
    folio_cecom: Optional[int] = None
    colonia: Optional[str] = None
    calle: Optional[str] = None
    cuadrante: Optional[str] = None
    region_geo: Optional[str] = None
    delegacion: Optional[str] = None
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None

# Esquema con relaciones completas (para respuestas detalladas)
class EventoReadWithRelations(EventoRead):
    # Las relaciones se incluirán automáticamente cuando se carguen desde la base de datos
    pass