from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlalchemy import BigInteger

# Enum para tipos de intervención
class TipoIntervencion(str, Enum):
    RECORRIDO = "recorrido"
    REPORTE = "reporte"
    OPERATIVO = "operativo"

# Enum para turnos
class TurnoEnum(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    MIXTO = "Mixto"
    DIARIO = "Diario"

# Enum para roles de oficial
class RolOficial(str, Enum):
    ADMIN = "admin"
    OFICIAL = "oficial"
    COMANDANTE = "comandante"

# Modelos SQLModel (combinan Pydantic y SQLAlchemy)

class TpoEvento(SQLModel, table=True):
    __tablename__ = "tpo_evento"
    
    id_tpo_evento: Optional[int] = Field(default=None, primary_key=True)
    tpo_evento_desc: str
    
    # Relationships
    eventos: List["Evento"] = Relationship(back_populates="tipo_evento")

class Region(SQLModel, table=True):
    __tablename__ = "region"
    
    id_region: Optional[int] = Field(default=None, primary_key=True)
    region_desc: str
    
    # Relationships
    eventos: List["Evento"] = Relationship(back_populates="region")

class Unidades(SQLModel, table=True):
    __tablename__ = "unidades"
    
    id_unidad_vehic: Optional[int] = Field(default=None, primary_key=True)
    vehic: str
    marca: Optional[int] = None
    modelo: Optional[int] = None
    año: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = Field(default=True)
    
    # Relationships
    eventos: List["Evento"] = Relationship(back_populates="unidad")

class Oficial(SQLModel, table=True):
    __tablename__ = "oficial"
    
    id_oficial: Optional[int] = Field(default=None, primary_key=True)
    fullname: str = Field(..., description="Nombre completo del oficial")
    telefono: Optional[str] = Field(None, description="Número de teléfono")
    correo_electronico: str = Field(..., unique=True, description="Correo electrónico único")
    rol: RolOficial = Field(default=RolOficial.OFICIAL, description="Rol del oficial en el sistema")
    id_telegram: Optional[int] = Field(None, sa_column=BigInteger(), description="ID de Telegram del oficial")
    
    # Relationships
    oficial_eventos: List["OficialEvento"] = Relationship(back_populates="oficial")

class Detenido(SQLModel, table=True):
    __tablename__ = "detenido"
    
    id_detenido: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(..., description="Nombre completo del detenido")
    edad: Optional[int] = Field(None, description="Edad del detenido")
    rfc: Optional[str] = Field(None, description="RFC del detenido")
    
    # Relationships
    detenido_eventos: List["DetenidoEvento"] = Relationship(back_populates="detenido")

class TipoMotivo(SQLModel, table=True):
    __tablename__ = "tipo_motivo"
    
    tipo_motivo_id: Optional[int] = Field(default=None, primary_key=True)
    tipo_motivo: str = Field(unique=True)
    
    # Relationships
    motivos: List["Motivos"] = Relationship(back_populates="tipo_motivo")

class Motivos(SQLModel, table=True):
    __tablename__ = "motivos"
    
    id_mot: Optional[int] = Field(default=None, primary_key=True)
    motivo: str = Field(unique=True)
    tipo_motivo_id: Optional[int] = Field(default=None, foreign_key="tipo_motivo.tipo_motivo_id")
    
    # Relationships
    tipo_motivo: Optional[TipoMotivo] = Relationship(back_populates="motivos")
    motivos_eventos: List["MotivosEvento"] = Relationship(back_populates="motivo")

class Droga(SQLModel, table=True):
    __tablename__ = "droga"
    
    id_droga: Optional[int] = Field(default=None, primary_key=True)
    droga_desc: str
    
    # Relationships
    droga_detenidos: List["DrogaDetenidoEvento"] = Relationship(back_populates="droga")

class Arma(SQLModel, table=True):
    __tablename__ = "arma"
    
    id_arma: Optional[int] = Field(default=None, primary_key=True)
    tpo_arma: str
    nombre_arma: str
    
    # Relationships
    arma_detenidos: List["ArmaDetenidoEvento"] = Relationship(back_populates="arma")

class Evento(SQLModel, table=True):
    __tablename__ = "evento"
    
    iph_id: Optional[int] = Field(default=None, primary_key=True)
    id_tpo_evento: Optional[int] = Field(default=None, foreign_key="tpo_evento.id_tpo_evento")
    intervencion: Optional[TipoIntervencion] = Field(None, description="Tipo de intervención")
    id_region: Optional[int] = Field(default=None, foreign_key="region.id_region")
    turno: Optional[TurnoEnum] = Field(None, description="Turno del evento")
    id_unidad_vehi: Optional[int] = Field(default=None, foreign_key="unidades.id_unidad_vehic")
    folio_cecom: Optional[int] = Field(None, description="Folio CECOM (numérico)")
    colonia: Optional[str] = None
    calle: Optional[str] = None
    cuadrante: Optional[str] = Field(None, description="Cuadrante del evento")
    region_geo: Optional[str] = Field(None, description="Región geográfica del evento")
    delegacion: Optional[str] = Field(None, description="Delegación del evento")
    georreferencia: Optional[str] = None
    fecha_evento: Optional[datetime] = None
    narrativa: Optional[str] = None
    
    # Relationships
    tipo_evento: Optional[TpoEvento] = Relationship(back_populates="eventos")
    region: Optional[Region] = Relationship(back_populates="eventos")
    unidad: Optional[Unidades] = Relationship(back_populates="eventos")
    oficial_eventos: List["OficialEvento"] = Relationship(back_populates="evento")
    detenido_eventos: List["DetenidoEvento"] = Relationship(back_populates="evento")
    motivos_eventos: List["MotivosEvento"] = Relationship(back_populates="evento")

class OficialEvento(SQLModel, table=True):
    __tablename__ = "oficial_evento"
    
    iph_id: Optional[int] = Field(default=None, foreign_key="evento.iph_id", primary_key=True)
    id_oficial: Optional[int] = Field(default=None, foreign_key="oficial.id_oficial", primary_key=True)
    
    # Relationships
    evento: Optional[Evento] = Relationship(back_populates="oficial_eventos")
    oficial: Optional[Oficial] = Relationship(back_populates="oficial_eventos")

class DetenidoEvento(SQLModel, table=True):
    __tablename__ = "detenido_evento"
    
    id_detenido_evento: Optional[int] = Field(default=None, primary_key=True)
    iph_id: Optional[int] = Field(default=None, foreign_key="evento.iph_id")
    id_detenido: Optional[int] = Field(default=None, foreign_key="detenido.id_detenido")
    rnd_detenido: Optional[str] = None
    
    # Relationships
    evento: Optional[Evento] = Relationship(back_populates="detenido_eventos")
    detenido: Optional[Detenido] = Relationship(back_populates="detenido_eventos")
    droga_detenidos: List["DrogaDetenidoEvento"] = Relationship(back_populates="detenido_evento")
    arma_detenidos: List["ArmaDetenidoEvento"] = Relationship(back_populates="detenido_evento")

class MotivosEvento(SQLModel, table=True):
    __tablename__ = "motivos_evento"
    
    iph_id: Optional[int] = Field(default=None, foreign_key="evento.iph_id", primary_key=True)
    id_mot: Optional[int] = Field(default=None, foreign_key="motivos.id_mot", primary_key=True)
    
    # Relationships
    evento: Optional[Evento] = Relationship(back_populates="motivos_eventos")
    motivo: Optional[Motivos] = Relationship(back_populates="motivos_eventos")

class DrogaDetenidoEvento(SQLModel, table=True):
    __tablename__ = "droga_detenido_evento"
    
    id_droga: Optional[int] = Field(default=None, foreign_key="droga.id_droga", primary_key=True)
    id_detenido_evento: Optional[int] = Field(default=None, foreign_key="detenido_evento.id_detenido_evento", primary_key=True)
    cantidad: Optional[float] = None
    tipo_cantidad: Optional[str] = None
    
    # Relationships
    droga: Optional[Droga] = Relationship(back_populates="droga_detenidos")
    detenido_evento: Optional[DetenidoEvento] = Relationship(back_populates="droga_detenidos")

class ArmaDetenidoEvento(SQLModel, table=True):
    __tablename__ = "arma_detenido_evento"
    
    id_arma: Optional[int] = Field(default=None, foreign_key="arma.id_arma", primary_key=True)
    id_detenido_evento: Optional[int] = Field(default=None, foreign_key="detenido_evento.id_detenido_evento", primary_key=True)
    cantidad: Optional[int] = None
    
    # Relationships
    arma: Optional[Arma] = Relationship(back_populates="arma_detenidos")
    detenido_evento: Optional[DetenidoEvento] = Relationship(back_populates="arma_detenidos")