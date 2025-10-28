from sqlmodel import create_engine, SQLModel, Session
from .settings import settings

# Crear el motor de SQLAlchemy con configuración para SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Necesario para SQLite con FastAPI
    echo=True  # Para ver las consultas SQL en desarrollo
)

def create_db_and_tables():
    """Crear todas las tablas en la base de datos"""
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener la sesión de base de datos
def get_session():
    with Session(engine) as session:
        yield session