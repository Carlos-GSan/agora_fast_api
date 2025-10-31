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
    turno: TurnoEnum = Field(..., description="Turno del evento (obligatorio)")
    id_unidad_vehi: int = Field(..., description="ID de la unidad vehicular (obligatorio)")
    folio_cecom: int = Field(..., description="Folio CECOM (numérico, obligatorio)")
    colonia: str = Field(..., description="Colonia donde ocurrió el evento (obligatorio)")
    calle: Optional[str] = Field(None, description="Calle donde ocurrió el evento")
    cuadrante: str = Field(..., description="Cuadrante del evento (obligatorio)")
    region_geo: str = Field(..., description="Región geográfica del evento (obligatorio)")
    delegacion: str = Field(..., description="Delegación del evento (obligatorio)")
    georreferencia: str = Field(..., description="Coordenadas GPS del evento (obligatorio)")
    fecha_evento: datetime = Field(..., description="Fecha y hora del evento (obligatorio)")
    narrativa: str = Field(..., description="Narrativa del evento (obligatorio)")
    
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
    id_tpo_evento: int
    intervencion: TipoIntervencion
    id_region: int
    turno: TurnoEnum
    id_unidad_vehi: int
    folio_cecom: int
    colonia: str
    calle: Optional[str] = None
    cuadrante: str
    region_geo: str
    delegacion: str
    georreferencia: str
    fecha_evento: datetime
    narrativa: str

# Esquema con relaciones completas (para respuestas detalladas)
class EventoReadWithRelations(EventoRead):
    # Las relaciones se incluirán automáticamente cuando se carguen desde la base de datos
    pass