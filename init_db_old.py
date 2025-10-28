"""
Script para inicializar la base de datos con datos de ejemplo
"""
from sqlmodel import Session, select
from app.config.database import engine, create_db_and_tables
from app.models.models import (
    TpoEvento, Intervencion, Region, Unidades, Oficial, 
    Detenido, TipoMotivo, Motivos, Droga, Arma
)
from datetime import datetime

def init_db():
    # Primero crear las tablas
    print("Creando tablas en la base de datos...")
    create_db_and_tables()
    print("Tablas creadas exitosamente.")
    
    print("Insertando datos de ejemplo...")
    with Session(engine) as session:
        try:
            # Tipos de Evento
            tipos_evento = [
                {"tpo_evento_desc": "Fiscalía"},
                {"tpo_evento_desc": "Denuncia"},
                {"tpo_evento_desc": "Juzgado Cívico"},
                {"tpo_evento_desc": "Conocimiento"},
            ]
            
            for tipo_data in tipos_evento:
                statement = select(TpoEvento).where(TpoEvento.tpo_evento_desc == tipo_data["tpo_evento_desc"])
                existing = session.exec(statement).first()
                if not existing:
                    tipo = TpoEvento(**tipo_data)
                    session.add(tipo)
            
            # Intervenciones
            intervenciones = [
                {"intervencion_desc": "Reporte"},
                {"intervencion_desc": "Recorrido"},
                {"intervencion_desc": "Operativo"},
            ]
            
            for interv_data in intervenciones:
                statement = select(Intervencion).where(Intervencion.intervencion_desc == interv_data["intervencion_desc"])
                existing = session.exec(statement).first()
                if not existing:
                    interv = Intervencion(**interv_data)
                    session.add(interv)
            
            # Regiones
            regiones = [
                {"region_desc": "Región 1"},
                {"region_desc": "Región 2"},
                {"region_desc": "Región 3"},
                {"region_desc": "Región 4"},
                {"region_desc": "Región 5"},
                {"region_desc": "Región 6"},
                {"region_desc": "Región 7"},
                {"region_desc": "Región 8"},
                {"region_desc": "Región 9"}
            ]
            
            for region_data in regiones:
                statement = select(Region).where(Region.region_desc == region_data["region_desc"])
                existing = session.exec(statement).first()
                if not existing:
                    region = Region(**region_data)
                    session.add(region)
            
            # Unidades
            unidades = [
                {"vehic": "D-101", "marca": 1, "modelo": 2023, "año": 2023, "activo": True},
                {"vehic": "D-102", "marca": 2, "modelo": 2022, "año": 2022, "activo": True},
                {"vehic": "M-201", "marca": 3, "modelo": 2023, "año": 2023, "activo": True},
                {"vehic": "M-202", "marca": 1, "modelo": 2021, "año": 2021, "activo": True}
            ]
            
            for unidad_data in unidades:
                statement = select(Unidades).where(Unidades.vehic == unidad_data["vehic"])
                existing = session.exec(statement).first()
                if not existing:
                    unidad_data["fecha_registro"] = datetime.now()
                    unidad = Unidades(**unidad_data)
                    session.add(unidad)
            
            # Oficiales
            oficiales = [
                {"nombre_oficial": "Juan", "apepat_oficial": "Pérez", "apemat_oficial": "García"},
                {"nombre_oficial": "María", "apepat_oficial": "López", "apemat_oficial": "Martínez"},
                {"nombre_oficial": "Carlos", "apepat_oficial": "González", "apemat_oficial": "Rodríguez"},
                {"nombre_oficial": "Ana", "apepat_oficial": "Hernández", "apemat_oficial": "Silva"}
            ]
            
            for oficial_data in oficiales:
                statement = select(Oficial).where(
                    Oficial.nombre_oficial == oficial_data["nombre_oficial"],
                    Oficial.apepat_oficial == oficial_data["apepat_oficial"]
                )
                existing = session.exec(statement).first()
                if not existing:
                    oficial = Oficial(**oficial_data)
                    session.add(oficial)
            
            # Detenidos de ejemplo
            detenidos = [
                {"nombre_det": "Juan", "apepat_det": "Perengano", "apemat_det": "López", "edad": 35, "sexo": "M"},
                {"nombre_det": "María", "apepat_det": "Sánchez", "apemat_det": "Pérez", "edad": 28, "sexo": "F"},
                {"nombre_det": "Carlos", "apepat_det": "García", "apemat_det": "Ramírez", "edad": 42, "sexo": "M"},
                {"nombre_det": "Ana", "apepat_det": "Morales", "apemat_det": "Torres", "edad": 31, "sexo": "F"}
            ]
            
            for detenido_data in detenidos:
                statement = select(Detenido).where(
                    Detenido.nombre_det == detenido_data["nombre_det"],
                    Detenido.apepat_det == detenido_data["apepat_det"]
                )
                existing = session.exec(statement).first()
                if not existing:
                    detenido = Detenido(**detenido_data)
                    session.add(detenido)
            
            # Tipos de Motivo
            tipos_motivo = [
                {"tipo_motivo": "Delito"},
                {"tipo_motivo": "Falta Administrativa"}
            ]
            
            for tipo_motivo_data in tipos_motivo:
                statement = select(TipoMotivo).where(TipoMotivo.tipo_motivo == tipo_motivo_data["tipo_motivo"])
                existing = session.exec(statement).first()
                if not existing:
                    tipo_motivo = TipoMotivo(**tipo_motivo_data)
                    session.add(tipo_motivo)
            
                session.commit()  # Commit para obtener IDs
            
            # Motivos
            motivos = [
                {"motivo": "Posesión de narcóticos", "tipo_motivo_id": 1},
                {"motivo": "Robo con violencia", "tipo_motivo_id": 1},
                {"motivo": "Daños a terceros", "tipo_motivo_id": 2},
                {"motivo": "Escándalo en vía pública", "tipo_motivo_id": 2},
                {"motivo": "Falta de documentación", "tipo_motivo_id": 2}
            ]
            
            for motivo_data in motivos:
                statement = select(Motivos).where(Motivos.motivo == motivo_data["motivo"])
                existing = session.exec(statement).first()
                if not existing:
                    motivo = Motivos(**motivo_data)
                    session.add(motivo)
            
            # Drogas
            drogas = [
                {"droga_desc": "Marihuana"},
                {"droga_desc": "Cocaína"},
                {"droga_desc": "Heroína"},
                {"droga_desc": "Metanfetaminas"},
                {"droga_desc": "Fentanilo"}
            ]
            
            for droga_data in drogas:
                statement = select(Droga).where(Droga.droga_desc == droga_data["droga_desc"])
                existing = session.exec(statement).first()
                if not existing:
                    droga = Droga(**droga_data)
                    session.add(droga)
            
            # Armas
            armas = [
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Pistola calibre .380"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Pistola calibre 9mm"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Pistola calibre .45"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Revólver calibre .38"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Revólver calibre .357 Magnum"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Escopeta calibre 12"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Escopeta calibre 20"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Rifle calibre .22"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Rifle de asalto AK-47"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Rifle AR-15"},
                {"tpo_arma": "Arma de fuego", "nombre_arma": "Subametralladora"},
                {"tpo_arma": "Arma blanca", "nombre_arma": "Cuchillo"},
                {"tpo_arma": "Arma blanca", "nombre_arma": "Navaja"},
                {"tpo_arma": "Arma blanca", "nombre_arma": "Machete"},
                {"tpo_arma": "Arma blanca", "nombre_arma": "Puñal"},
                {"tpo_arma": "Contundente", "nombre_arma": "Bat de béisbol"},
                {"tpo_arma": "Contundente", "nombre_arma": "Tubo de metal"},
                {"tpo_arma": "Contundente", "nombre_arma": "Martillo"}
            ]
            
            for arma_data in armas:
                statement = select(Arma).where(
                    Arma.tpo_arma == arma_data["tpo_arma"],
                    Arma.nombre_arma == arma_data["nombre_arma"]
                )
                existing = session.exec(statement).first()
                if not existing:
                    arma = Arma(**arma_data)
                    session.add(arma)
            
            session.commit()
            print("Base de datos inicializada con datos de ejemplo")
            
        except Exception as e:
            session.rollback()
            print(f"Error al inicializar la base de datos: {e}")

if __name__ == "__main__":
    init_db()