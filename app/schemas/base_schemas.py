from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.models import RolOficial

# Esquemas para crear (sin ID)
class TpoEventoCreate(SQLModel):
    tpo_evento_desc: str

class RegionCreate(SQLModel):
    region_desc: str

class UnidadesCreate(SQLModel):
    vehic: str
    marca: Optional[int] = None
    modelo: Optional[int] = None
    año: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = True

class OficialCreate(SQLModel):
    fullname: str = Field(..., description="Nombre completo del oficial")
    telefono: Optional[str] = Field(None, description="Número de teléfono")
    correo_electronico: str = Field(..., description="Correo electrónico único")
    rol: RolOficial = Field(default=RolOficial.OFICIAL, description="Rol del oficial en el sistema")
    id_telegram: Optional[int] = Field(None, description="ID de Telegram del oficial")

class DetenidoCreate(SQLModel):
    full_name: str = Field(..., description="Nombre completo del detenido")
    edad: Optional[int] = Field(None, description="Edad del detenido")
    rfc: Optional[str] = Field(None, description="RFC del detenido")

class TipoMotivoCreate(SQLModel):
    tipo_motivo: str

class MotivosCreate(SQLModel):
    motivo: str
    tipo_motivo_id: int

class DrogaCreate(SQLModel):
    droga_desc: str

class ArmaCreate(SQLModel):
    tpo_arma: str
    nombre_arma: str

# Esquemas para actualizar
class OficialUpdate(SQLModel):
    fullname: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    rol: Optional[RolOficial] = None
    id_telegram: Optional[int] = None

class DetenidoUpdate(SQLModel):
    full_name: Optional[str] = None
    edad: Optional[int] = None
    rfc: Optional[str] = None

# Esquemas para leer (con ID, heredan del modelo principal)
class TpoEventoRead(SQLModel):
    id_tpo_evento: int
    tpo_evento_desc: str

class RegionRead(SQLModel):
    id_region: int
    region_desc: str

class UnidadesRead(SQLModel):
    id_unidad_vehic: int
    vehic: str
    marca: Optional[int] = None
    modelo: Optional[int] = None
    año: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    activo: bool

class OficialRead(SQLModel):
    id_oficial: int
    fullname: str
    telefono: Optional[str] = None
    correo_electronico: str
    rol: RolOficial
    id_telegram: Optional[int] = None

class DetenidoRead(SQLModel):
    id_detenido: int
    full_name: str
    edad: Optional[int] = None
    rfc: Optional[str] = None

class TipoMotivoRead(SQLModel):
    tipo_motivo_id: int
    tipo_motivo: str

class MotivosRead(SQLModel):
    id_mot: int
    motivo: str
    tipo_motivo_id: int

class DrogaRead(SQLModel):
    id_droga: int
    droga_desc: str

class ArmaRead(SQLModel):
    id_arma: int
    tpo_arma: str
    nombre_arma: str