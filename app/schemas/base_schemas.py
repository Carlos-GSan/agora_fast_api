from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List

# Esquemas para crear (sin ID)
class TpoEventoCreate(SQLModel):
    tpo_evento_desc: str

class IntervencionCreate(SQLModel):
    intervencion_desc: str

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
    nombre_oficial: str
    apepat_oficial: str
    apemat_oficial: Optional[str] = None

class DetenidoCreate(SQLModel):
    nombre_det: str
    apepat_det: str
    apemat_det: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None

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

# Esquemas para leer (con ID, heredan del modelo principal)
# Estos esquemas son útiles para respuestas de API sin relaciones completas
class TpoEventoRead(SQLModel):
    id_tpo_evento: int
    tpo_evento_desc: str

class IntervencionRead(SQLModel):
    id_intervencion: int
    intervencion_desc: str

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
    nombre_oficial: str
    apepat_oficial: str
    apemat_oficial: Optional[str] = None

class DetenidoRead(SQLModel):
    id_detenido: int
    nombre_det: str
    apepat_det: str
    apemat_det: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None

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